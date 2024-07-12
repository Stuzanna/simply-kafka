import json
import sys

from confluent_kafka import DeserializingConsumer, KafkaError, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer

# -- Config --

bootstrap_servers = "localhost:19092"
topics = ["stu-json"]
client_id = "myClientId"
consumer_group = "stu-consumer-group"
schema_registry_url = "http://localhost:18081"
offset_config = "earliest"

# -- Schema Registry Client ---
schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# --- Creating the Consumer ---
#   --- Serializers ---
def json_deserializer(msg, s_obj=None):
    # return json.loads(msg.decode('ascii'))
    return json.loads(msg)

avro_deserializer = AvroDeserializer(schema_registry_client)

#  --- Config ---
conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': client_id,
    'group.id': consumer_group,
    # 'security.protocol': 'SSL',
    # 'ssl.ca.location': '../sslcerts/ca.pem',
    # 'ssl.certificate.location': '../sslcerts/service.cert',
    # 'ssl.key.location': '../sslcerts/service.key', 
    # 'key.deserializer': json_deserializer, # if key in JSON use these two
    'value.deserializer': json_deserializer,
    # 'key.deserializer': avro_deserializer, # if key in avro use these two
    # 'value.deserializer': avro_deserializer,
    # 'schema.registry.url': schema_registry_url,
    'auto.offset.reset': offset_config,
    }

consumer = DeserializingConsumer(conf)


# --- Running the consumer ---

running = True

try:
    consumer.subscribe(topics)
    print(f"Subscribed to topics: {topics}")

    while running:
        try:
            msg = consumer.poll(timeout=1.0)
            if msg is None: 
                print("Waiting for message...")
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                    (msg.topic(), msg.partition(), msg.offset()))
                else:
                    raise KafkaException(msg.error())

            else:
                try:
                    key = msg.key()
                    if key is None:
                        key_str = "None"
                    elif key is "N/A":
                        key_str = "None"
                    else:
                        key_str = key

                    value = msg.value()
                    print(f"{msg.partition()}:{msg.offset()}: "
                        f"k={key_str} "
                        f"v={value}")
                except Exception as e:
                    print(f"Message deserialization failed: {e}")
                    continue
        except Exception as e:
            # Handle the case where deserialization fails
            print(f"Message polling/deserialization failed: {e}")
finally:
    # Close down consumer to commit final offsets.
    consumer.close()    