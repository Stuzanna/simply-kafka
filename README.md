# simply-kafka
Some simple explorations, providing easy to understand reusable examples to get to grips when starting with Kafka.

Examples include;

* A getting started stack to have a simple example running locally
* A TFL stream of live tube data from their public API
* Consumer gives some example consumers, using confluent_kafka library, or Quix's library

# Getting Started
`docker compose up -d`  
Will start the local Kafka cluster, a [data generator](https://github.com/Stuzanna/kafka-data-generator), Conduktor UI for interacting with Kafka on [localhost:8080](http://localhost:8080).

# TFL Tube Stream
Data generator, live stream of data from the next tube approaching the Stockwell underground station from the Transport for London API.

This can be used as a Kafka producer for the local stack when an internet connection is available.

Steps involved in it's creation included:
1. Navigating the TFL [documentation](https://api-portal.tfl.gov.uk/api-details#api=Line&operation=Line_ArrivalsByPathIds&definition=Tfl-41) site to find what endpoints held the data I wanted, how frequently it's updated and how to auth to the API
1. Query the TFL API to grab the station codes depending which station I wanted to watch
1. Query another part of the API to get the tube data, in this case incoming Victoria line tubes to Stockwell station
1. Improve the reliability by building in back-offs and what to do with empty responses
1. Capture and transform the API response into a usable JSON message 
1. Produce the JSON message into Kafka


*Screenshot of my app polling the TFL API.*
![screenshot of polling the API](tfl/img/tfl-api-poll.png)
*Screenshot from Conduktor's UI of the message in Kafka.*
![message in Kafka](tfl/img/message-in-kafka.png)

This leverages an adjusted [Conduktor](https://www.conduktor.io) Docker compose stack for local development, containing a Kafka cluster and tooling.

To run this yourself:

1. Install `requirements.txt`
1. Get an API key from TFL by signing-up for an account on [their website](https://api-portal.tfl.gov.uk/signup) and generating one
1. Create a file `.env` within `tfl` directory, setting your API key as `TFL_API_KEY`
1. Run `tfl/main.py`
1. View results using Conduktor if you run the Docker compose, or run the consumer script in `consumer/`

# working-with-schemas
The other examples don't include schemas to keep the boilerplate more minimal.
Read through this folder to see examples using local schemas, remote schemas on the Confluent schema registry, for both Avro and JSON schema types.

# Acknowledgements
[Aiven](https://github.com/Aiven-Labs/python-fake-data-producer-for-apache-kafka), [Quix](simple-kafka-python) and [Confluent](https://developer.confluent.io/courses/kafka-python/intro/) content for producer & consumer examples to model my own around.
