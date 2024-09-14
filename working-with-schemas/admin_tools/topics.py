import sys
from confluent_kafka.admin import NewTopic

def topic_exists(admin_client, topic):
    '''
    return True if topic exists, and False if not.
    
    The AdminClient is a standard Kafka protocol client, 
    supporting the standard librdkafka configuration properties
    as specified at https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    '''
    metadata = admin_client.list_topics()
    for t in iter(metadata.topics.values()):
        if t.topic == topic:
            return True
    return False

def create_topic(admin_client, topic, num_partitions=6, replication_factor=3):
    '''
    Create a new topic and return results dictionary.

    Takes in an admin client where, the AdminClient is a standard Kafka protocol client, 
    supporting the standard librdkafka configuration properties 
    as specified at https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

    The topic name to create. 
    The number of partitions and the replication factor. Both with defaults.
    '''
    new_topic = NewTopic(topic, num_partitions, replication_factor) 
    result_dict = admin_client.create_topics([new_topic])
    for topic, future in result_dict.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print(f"Failed to create topic {topic}: {e} Exiting...")
            sys.exit(1) # Causes errors
