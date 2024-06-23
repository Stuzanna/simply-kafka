from kafka import KafkaConsumer

import json

# json consumer

# -- Kafka config ---
bootstrap_servers='redpanda-0:9092',
 # security_protocol="SSL",
 # ssl_cafile="./ca.pem",
 # ssl_certfile="./service.cert",
 # ssl_keyfile="./service.key",
value_deserializer = lambda value: json.loads(value.decode('ascii')), # decode bytes array(string?) into a json structure
auto_offset_reset='earliest' # default when joins is latest

# -- Data config --
topic= 'topic-of-interest'
group_id = 'id-of-group'



# --- Initialise consumer ---
consumer = KafkaConsumer(topic, group_id)


# for msg in consumer:
#     print (msg)

consumer.subscribe(topics=topic)
for message in consumer:
  print ("%d:%d: value=%s" % (message.partition,
                          message.offset,
                          message.value))