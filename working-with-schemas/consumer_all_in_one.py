import json
import time
import requests

from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

# -- Consumer Config --
bootstrap_servers = "localhost:19095"
topics = ["customers"]
sleep_time = 1 # Sleep between each message
client_id = "my-python-consumer-fast"
consumer_group_id = "my-slow-pythonic-consumer-group"
offset_config = "earliest"
conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': client_id,
    'group.id': consumer_group_id,
    # 'security.protocol': 'SSL',
    # 'ssl.ca.location': '../sslcerts/ca.pem',
    # 'ssl.certificate.location': '../sslcerts/service.cert',
    # 'ssl.key.location': '../sslcerts/service.key', 
    'auto.offset.reset': offset_config,
    }

# SR config, constructor, schema definition, serialization type
schema_registry_url = "http://localhost:18081"
schema_registry_conf = {'url': schema_registry_url, 'basic.auth.user.info': '<SR_UserName:SR_Password>'}

schema_registry_client = SchemaRegistryClient(schema_registry_conf)

schema_loc = 'local' # local or remote
# schema_file = 'customer-1.avsc' # or .json
schema_file = 'customer-1.json' # or .json

schema_loc = 'remote' # local or remote
schema_id = 1
subject = 'customers-value'

# serialization = "json"
serialization = "avro"
# serialization = "none"

# Create deserializer based on serialization format and schema location
def load_schema(schema_loc: str, schema_file = None, schema_id = None, schema_registry_url = None) -> str:
    """
    Load a schema based on the provided schema location (local or remote).

    This function loads a schema either from a local file or by fetching it 
    from a remote schema registry, depending on the specified `schema_loc`.

    Parameters:
    ----------
    schema_loc : str
        The location of the schema. Must be either 'local' or 'remote'.
    schema_file : str, optional
        Path to the local schema file (required if `schema_loc` is 'local').
    schema_id : int, optional
        The ID of the schema to fetch from the schema registry (required if `schema_loc` is 'remote').
    schema_registry_url : str, optional
        The base URL of the schema registry (required if `schema_loc` is 'remote').

    Returns:
    -------
    str
        The schema as a JSON-formatted string.

    Raises:
    ------
    ValueError
        If required arguments are missing or an invalid schema location is provided.
    """
    if schema_loc == 'local':
        if schema_file is None:
            raise ValueError("Schema file must be provided for local schemas.")
        print(f'Loading schema from local file: {schema_file}')
        with open(schema_file, 'r') as schema_file:
            return json.dumps(json.load(schema_file))
    elif schema_loc == 'remote':
        if schema_id is None:
            raise ValueError("Schema ID must be provided for remote schemas.")
        if schema_registry_url is None:
            raise ValueError("Schema registry URL must be provided for remote schemas.")
        print(f"Fetching schema from remote: {schema_registry_url}")
        response = requests.get(f"{schema_registry_url}/schemas/ids/{schema_id}")
        return response.json()["schema"]
    else:
        raise ValueError(f"Invalid schema location: {schema_loc}. Expected 'local' or 'remote'.")

def create_deserializer(serialization, schema_str, schema_registry_client):
    """
    Create a deserializer based on the specified serialization format.

    Depending on the `serialization` parameter, this function creates and returns a 
    JSON or Avro serializer using the provided schema string and Schema Registry client.
    If 'none' is specified, no serializer is created.

    Parameters:
    ----------
    serialization : str
        The serialization format to use. Expected values are 'json', 'avro', or 'none'.
    schema_str : str
        The schema in JSON format to use for serialization.
    schema_registry_client : SchemaRegistryClient
        The client instance for interacting with the Schema Registry.

    Returns:
    -------
    JSONSerializer, AvroSerializer, or None
        A serializer for JSON or Avro based on the `serialization` type, or None if no serialization is selected.

    Raises:
    ------
    ValueError
        If an invalid serialization type is provided.
    """
    if serialization == 'json':
        print("Creating JSON deserializer...")
        return JSONDeserializer(schema_str)
    elif serialization == 'avro':
        print("Creating Avro deserializer...")
        return AvroDeserializer(schema_registry_client, schema_str)
    elif serialization == 'none':
        print('No serialization selected, skipping deserializer creation.')
        return None
    else:
        raise ValueError(f"Invalid serialization: {serialization}. Expected 'avro', 'json' or 'none'.")

if serialization in ['json', 'avro']:
    if schema_loc == 'local':
        schema_str = load_schema(schema_loc, schema_file)
    elif schema_loc == 'remote':
        schema_str = load_schema(schema_loc, None, schema_id, schema_registry_url)
    else:
        raise ValueError(f"Invalid schema location: {schema_loc}. Expected 'local' or 'remote'.")
    
    deserializer = create_deserializer(serialization, schema_str, schema_registry_client)
    print(f"Success: Created {serialization.upper()} serializer.")
else:
    create_deserializer(serialization, None, None)

# --- Creating the Consumer ---
consumer = Consumer(conf)

# --- Running the consumer ---
try:
    consumer.subscribe(topics)
    print(f"Subscribed to topics: {topics}")

    while True:
        try:
            msg = consumer.poll(timeout = 3.5)
            if msg is None: 
                print("Waiting for message...")
                continue

            else:
                    key = msg.key().decode('utf-8')
                    if serialization in ['json', 'avro']:
                          value = deserializer(msg.value(), SerializationContext(topics[0], MessageField.VALUE))
                    elif serialization == 'none':
                        value = msg.value().decode('utf-8')
                    else:
                        raise ValueError(f"Invalid serialization type: {serialization}. Expected 'avro', 'json' or 'none'.")
                    
                    print(f"{msg.partition()}:{msg.offset()}: "
                        f"k={key} "
                        f"v={value}")
                    time.sleep(sleep_time)  

        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Stopping the consumer...")
            break
        except Exception as e:
            print(f"Error reading message at {msg.partition()}:{msg.offset()}. Error =  {e}")
finally:
    # Close down consumer to commit final offsets.
    print("Attempting to close the consumer...")
    consumer.close()
    print("Consumer closed.")    