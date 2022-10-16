import os
from kafka import KafkaConsumer
from json import loads

topic = os.getenv("KAFKA_TOPIC", "tap")
group_id = os.getenv("GROUP_ID", "my-group")
consumer = KafkaConsumer(
     topic,
     bootstrap_servers=['kafkaServer:9092'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
     group_id=group_id,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    print(message)
    message = message.value
    print(message)
    #print('{} read'.format(message))


