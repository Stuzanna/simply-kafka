
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import json
import sys

bs = "localhost:19092"
topics = ["weather_data_demo"]
client_id = "myClientId"
consumer_group = "stuCG"
offset_config = "earliest"

# --- Blend of Aiven and Quix's demos ---

# -- Creating A Consumer ---

from confluent_kafka import DeserializingConsumer
import json
import sys

def json_serializer(msg, s_obj=None):
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
    'value.deserializer': json_serializer,
    # 'key.deserializer': json_serializer, # if key in JSON
    'auto.offset.reset': offset_config,
    }

consumer = DeserializingConsumer(conf)


# --- Running the consumer ---

running = True

try:
    consumer.subscribe(topics)
    print(f"Subscribed to topics: {topics}")

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None: 
            print("Waiting for message...")
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
             print(f"{msg.partition()}:{msg.offset()}: "
                  f"k={msg.key()} "
                  f"v={msg.value()}")
finally:
    # Close down consumer to commit final offsets.
    consumer.close()    