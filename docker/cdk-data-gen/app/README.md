Credit to [Aiven tutorial](https://aiven.io/developer/teach-yourself-apache-kafka-and-python-with-a-jupyter-notebook) for the structure to copy off for pizza generator.

# Docker Build Help

docker build -t stu-py-data-gen:0.x -f ./Dockerfile ./

docker build -t stuzanne/python-kafka-data-generator:0.x -f ./Dockerfile ./
docker build -t stuzanne/python-kafka-data-generator:latest -f ./Dockerfile ./

docker tag stuzanne/python-kafka-data-generator:0.1 stuzanne/python-kafka-data-generator:latest

docker push stuzanne/python-kafka-data-generator:tagname
