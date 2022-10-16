docker stop kibana
docker container rm kibana
#docker build ../kibana/ --tag tap:kibana
docker run -p 5601:5601 --ip 10.0.100.52 --network tap --name kibana tap:kibana
