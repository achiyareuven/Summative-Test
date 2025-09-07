from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json

load_dotenv()



class Consumer:
    def __init__(self,topic,group,bootstrap_servers=None):
        self.topic = topic
        self.group_name = group
        self.bootstrap_servers = bootstrap_servers or os.getenv("BOOTSTRAP_SERVERS")


    def get_consumer_events(self):
        consumer = KafkaConsumer(
            self.topic,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers=[self.bootstrap_servers],
            consumer_timeout_ms=10000,
            auto_offset_reset='earliest',
            group_id=self.group_name
        )

        for msg in consumer:
            yield msg.value


p = Consumer("jjj","ds")
o = p.get_consumer_events()

for msg in o:
    print(msg["id"])

    # print(type(msg.values),f"value={msg.values}")