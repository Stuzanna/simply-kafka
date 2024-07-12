import json
import sys

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# -- Config --
bootstrap_servers = "localhost:19092"
topics = ["stu-json"]
timeout = 1.0 # Maximum time to block waiting for message(Seconds)
client_id = "my-client-id"
consumer_group = "my-consumer-group"
schema_registry_url = "http://localhost:18081"
schema_registry_conf = {'url': schema_registry_url}
offset_config = "earliest"

#  --- Construction ---
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_deserializer = AvroDeserializer(schema_registry_client)

def json_deserializer(msg, s_obj=None):
    # return json.loads(msg.decode('ascii'))
    return json.loads(msg)

conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': client_id,
    'group.id': consumer_group,
    # 'security.protocol': 'SSL',
    # 'ssl.ca.location': '../sslcerts/ca.pem',
    # 'ssl.certificate.location': '../sslcerts/service.cert',
    # 'ssl.key.location': '../sslcerts/service.key', 
    'value.deserializer': json_deserializer, #comment me in for JSON
    # 'value.deserializer': avro_deserializer, #comment me in for Avro
    'auto.offset.reset': offset_config,
    }

# --- Creating the Consumer ---
consumer = DeserializingConsumer(conf)

# --- Running the consumer ---

running = True

try:
    consumer.subscribe(topics)
    print(f"Subscribed to topics: {topics}")
    print(f"Timeout set for every {timeout} seconds")

    while running:
        try:
            msg = consumer.poll(timeout)
            if msg is None: 
                print("Waiting for message...")
                continue

            else:
                    key = msg.key()
                    value = msg.value()
                    print(f"{msg.partition()}:{msg.offset()}: "
                        f"k={key} "
                        f"v={value}")
        except Exception as e:
            print(f"Error reading message: {e}")
finally:
    # Close down consumer to commit final offsets.
    consumer.close()    