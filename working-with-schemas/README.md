To run an example yourself follow the instructions in Demo. To understand the code better, see the supporting description of the contents of the directory.  

Note a slightly different docker-compose stack as the root, to use the Confluent schema registry as it supports JSON schema unlike the inbuilt one in Redpanda broker.

# Demo

Produce and consume messages about fake customers using the Avro schema provided. Instructions below to follow along on the CLI.

1. Activate virtual environment and install the `../requirements.txt` file
   1. `python3 -m venv ./venv/schema-demo`
   1. `source ./venv/schema-demo/bin/activate`
   1. `pip install -r ../requirements.txt`
1. Spin up the local environment, `docker compose up -d`
   1. Give it time to finish, should take around 20 seconds
1. Run `producer.py` using your ide or `python3 producer.py` . Ctrl+c to cancel the script and stop producing when you wish
1. Run `consumer.py` to consume
1. Interact with the Kafka stack and it's data using Conduktor on [localhost:8080](http://localhost:8080).
1. Tear down the environment, `docker compose down -v`

# Example schemas
Example schemas for different types of message.  

Avro schemas are `.avsc` , JSON are `.json`.

# Consumers
* consumer.py is easier to read with a lot of the reusable functions left in consumer_tools.py
* consumer_all_in_one.py has all the code, including the functions, in one file
* consumer_tools.py is the functions for reuse removed from main consumer code

# Producers
producer.py is the main producer script, it pulls in a class Person from person.py, and tools from both producer_tools.py and `/admin_tools`
You can either paste them into the script to get an all-in-one, or include both the admin and producer tools files so they can be imported.

# Schema-functions
Function to register a local schema with the schema registry, useful if want to do this without having to produce messages.
Function to fetche the latest schema and schema ID for a given subject from the Schema Registry.
