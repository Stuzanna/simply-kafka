
My project building a Kafka app for learning Kafka.

## Current Architecture
What the app looks like today.  

![Simple Local Streamer](./diagrams/Simple%20Local%20Streamer.drawio.png)  


Optionally may use the simple producers for producing to Upstash.
The streamer is published as a Kafka data generator on [Github](https://github.com/Stuzanna/kafka-data-generator) and [Dockerhub](https://hub.docker.com/r/stuzanne/kafka-data-generator).

![Original Starting Architecture](./diagrams/Original%20Starting%20Architecture.drawio.png)

## Target Architecture
Where I would like to get to with the app.
![Target architecture](./diagrams/Target%20Architecture.drawio.png)

## Experimental Architecture
What could be...
![Experimental architecture](./diagrams/Experimental%20Architecture.drawio.png)

## Consider
- [X] Setup a more useful stream
- [X] Dockerise
- [ ] Check against a schema registry
- [ ] Connectors
- [ ] Postgres or Aiven connection
- [ ] Pandas conneciton

