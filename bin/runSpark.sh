docker stop spark
docker container rm spark
#docker build ../spark/ --tag tap:spark
docker run -e SPARK_ACTION=spark-submit-python -p 4040:4040 --network tap --add-host=host.docker.internal:host-gateway --name spark -v $PWD/../.dataset:/opt/tap/.dataset -it tap:spark TESTkafka_structuredstream.py "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1"