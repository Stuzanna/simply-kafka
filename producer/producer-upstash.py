from kafka import KafkaProducer
from ..upstashPackage.upstashCreds import password, username # local file with credentials

producer = KafkaProducer(
  bootstrap_servers=['prompt-horse-11315-eu1-kafka.upstash.io:9092'],
  sasl_mechanism='SCRAM-SHA-256',
  security_protocol='SASL_SSL',
  sasl_plain_username = username,
  sasl_plain_password = password,
)

# example will be for a truck sending gps info, a message
truckValue = 0
producer.send('my-dev-upstash', key=b'truck%d' % truckValue, value=b'message from truck') # use the key for the same partition, e.g. for same truck
# could use f-strings but as byte code have to do a bit different with the %d


# ...
# # loop producing
# for i in range(10):
#   producer.send('my-dev-upstash', key=b'truck%d' % i, value=b'message from truck')
#   # could use f-strings but as byte code have to do a bit different with the %d
# ...

producer.close()