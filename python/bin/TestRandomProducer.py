import os
import random
from time import sleep
from json import dumps
from kafka import KafkaProducer

topic = os.getenv("KAFKA_TOPIC", "tap")
producer = KafkaProducer(bootstrap_servers=['kafkaServer:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


dictList=["hi", "I", "good", "bad", "terrible", "beautiful", "wonderful", "nice", "ugly", "hate", "love", "game", "review", "this", "rage", "quit", "countless", "fun", "hidden", "great", "indie", "death", "died", "boss", "hard", "easy", "balance", "unplayable", "lag"]
random.seed()
for i in range(65536):
    wordCount = random.randint(1, 64)
    message=""
    for j in range(wordCount):
        index = random.randint(0, len(dictList)-1)
        message =  message + dictList[index]+" "
    data = {'text' : message}
    producer.send(topic, value=data)
    timeout=float(random.randrange(3,30))/10
    sleep(timeout)
