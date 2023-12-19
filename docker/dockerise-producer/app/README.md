docker build -t stu-py-data-gen:0.x -f ./Dockerfile ./

docker build -t stuzanne/python-kafka-data-generator:0.x -f ./Dockerfile ./
docker build -t stuzanne/python-kafka-data-generator:latest -f ./Dockerfile ./

docker tag stuzanne/python-kafka-data-generator:0.1 stuzanne/python-kafka-data-generator:latest

docker push stuzanne/python-kafka-data-generator:tagname
