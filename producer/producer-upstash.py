from kafka import KafkaProducer
import time
from upstashPackage.upstashCreds import password, username, bs_server # local file with credentials
# if issues, add this to the your vs code worksapce settings: "python.analysis.extraPaths": ["${workspaceFolder}/upstashPackage/"]

producer = KafkaProducer(
  bootstrap_servers=[bs_server],
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
# for i in range(100):
#   time.sleep(0.25) # If need a pause within the loop
#   producer.send('my-dev-upstash', key=b'truck%d' % i, value=b'message from truck')
#   # could use f-strings but as byte code have to do a bit different with the %d
# ...

producer.close()