docker stop twitterProducer
docker container rm twitterProducer
#docker build ../python/ --tag tap:python
docker run --network tap -e PYTHON_APP=TwitterProducer.py --name twitterProducer -it tap:python