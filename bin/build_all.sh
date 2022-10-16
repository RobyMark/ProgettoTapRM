docker build ../python/ --tag tap:python
docker build ../logstash/ --tag tap:logstash
docker build ../kafka/ --tag tap:kafka
docker build ../spark/ --tag tap:spark
docker build ../elasticsearch/ --tag tap:elasticsearch
docker build ../kibana/ --tag tap:kibana