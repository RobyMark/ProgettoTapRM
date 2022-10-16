docker stop kafkaZookeeper
docker container rm kafkaZookeeper
#docker build ../kafka/ --tag tap:kafka
docker run -e KAFKA_ACTION=start-zk --network tap --ip 10.0.100.22  -p 2181:2181 --name kafkaZookeeper -it tap:kafka