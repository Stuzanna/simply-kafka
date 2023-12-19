
1. `stream-producer`
    1. Most developed, adjust configuration for what you need. Also available as a [Docker image](https://hub.docker.com/repository/docker/stuzanne/python-kafka-data-generator/general).
    1. Credit to Credit to [Aiven tutorial](https://aiven.io/developer/teach-yourself-apache-kafka-and-python-with-a-jupyter-notebook) for the structure to copy off for pizza generator.
1. `cli-commands`
    1. The most basic commands to produce, requires Kafka installed.
1. Remaining files.
    1. Simple Python producer examples for localhost and a remote cluster on Upstash. Ideally need to archive but moving folders requires more fiddling with the Python package management than I care for at this time. Go with `stream-producer`.
        1. If really want, or just looking for a quick way to product to Upstash, then fill in the details in `../upstashPackage/upstashCreds`. Then (assuming running in VS Code), use the `launch.json` info to run this within VS Code using the Run & Debug feature. Probably easier ways to do this but Comments can show you how it works.