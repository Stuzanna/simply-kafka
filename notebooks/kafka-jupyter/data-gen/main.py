import json
from kafka import KafkaProducer
from faker import Faker


producer = KafkaProducer(
    # bootstrap_servers="redpanda-0:9092", # inside container
    bootstrap_servers="localhost:19092", # outside container
    # security_protocol="SSL",
    # ssl_cafile=folderName+"ca.pem",
    # ssl_certfile=folderName+"service.cert",
    # ssl_keyfile=folderName+"service.key",
    value_serializer=lambda v: json.dumps(v).encode('ascii'),
    key_serializer=lambda v: json.dumps(v).encode('ascii')

)


# test message

# producer.send("test-topic",
#                 key={"key": 1},
#                 value={"message": "hello world"}
#             )
# producer.flush()



# faker generator

fake = Faker()

# # message is a tuple
# message = {
#     'name': fake.name(),
#     'address': fake.address(),
#     'phone': fake.phone_number()
# }
# print(message)

from pizzaProducer import PizzaProvider

fake.add_provider(PizzaProvider)

for i in range(0,10):
    print(fake.pizzaName())
