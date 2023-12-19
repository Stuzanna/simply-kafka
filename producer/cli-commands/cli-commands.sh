kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first_topic < <path-to-file>.txt

kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first_topic --from-beginning