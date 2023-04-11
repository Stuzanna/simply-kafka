from kafka import KafkaProducer
 
producer = KafkaProducer(
  bootstrap_servers=['localhost:9092']
)


# the 'b' prefix in the below code indicates that the string is a bytes object, rather than a regular string.
# The b prefix is used to create a bytes object from a string literal.

producer.send('topic0', key=b'mykey', value=b'myMessageValue') # sends 1 message with a key


# ...
# for _ in range(10000):
#   producer.send('topic0', key=b'', value=b'my many messages') # sends 1 message with a key

producer.close()