docker stop consoleConsumer
docker container rm consoleConsumer
#docker build ../python/ --tag tap:python
docker run --network tap -e PYTHON_APP=ConsoleConsumer.py --name consoleConsumer -it tap:python
