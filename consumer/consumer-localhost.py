from kafka import KafkaConsumer
 

consumer = KafkaConsumer(
  'my-topic',
  bootstrap_servers=['localhost:9092'],
  group_id='my_group_id',
  auto_offset_reset='earliest',  # read messages from the beginning of the topic
  enable_auto_commit=True,  # commit offsets automatically after consuming messages
  value_deserializer=lambda x: x.decode('utf-8')  # decode message value as utf-8 string
  # The value_deserializer option is used to decode the message value from bytes to a utf-8 string
  # You can use a different decoder if your messages are encoded in a different format
)

# consume messages from the topic
for message in consumer:
    print(message.value)

consumer.close()
