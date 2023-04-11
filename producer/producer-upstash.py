from kafka import KafkaProducer
from config import password, username # local file with credentials

producer = KafkaProducer(
  bootstrap_servers=['prompt-horse-11315-eu1-kafka.upstash.io:9092'],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username = username,
  sasl_plain_password = password,
)

producer.send('my-dev-upstash-topic', key=b'truck0', value=b'message from truck0') # use the key for the same partition, e.g. for same truck


# loop producing
# for _ in range(100):
#   producer.send('my-upstash-topic', b'some_message_bytes')

producer.close()