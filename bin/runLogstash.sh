docker stop logstash
docker container rm logstash
#docker build ../logstash/ --tag tap:logstash
docker run --network tap --ip 10.0.100.10  -it --name logstash tap:logstash