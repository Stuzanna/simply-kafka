from kafka import KafkaConsumer
from upstashPackage.upstashCreds import username, password, bs_server # from local file with credentials
 
consumer = KafkaConsumer(
  'my-dev-upstash',
  bootstrap_servers=[bs_server],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username = username,
  sasl_plain_password = password,
  group_id='$GROUP_NAME',
  auto_offset_reset='earliest',
  value_deserializer=lambda x: x.decode('utf-8'),  # decode message value as utf-8 string
  key_deserializer=lambda x: x.decode('utf-8')
  # The value_deserializer option is used to decode the message value from bytes to a utf-8 string. 
  # You can use a different decoder if your messages are encoded in a different format.
  # Look in the KafkaConsumer class to see the definitions.
)
# ...
# consume messages from the topic
for message in consumer:
    print(message.key, message.value)

consumer.close()
