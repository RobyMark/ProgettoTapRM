docker stop kafkaServer
docker container rm kafkaServer
#docker build ../kafka/ --tag tap:kafka
docker run -e KAFKA_ACTION=start-kafka --network tap --ip 10.0.100.23  -p 9092:9092 --name kafkaServer -it tap:kafka