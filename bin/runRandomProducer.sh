docker stop randomProducer
docker container rm randomProducer
#docker build ../python/ --tag tap:python
docker run --network tap -e PYTHON_APP=TestRandomProducer.py --name randomProducer -it tap:python