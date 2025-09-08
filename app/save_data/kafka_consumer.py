from kafka import KafkaConsumer
from dotenv import load_dotenv
from utils import generate_file_identifier
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
            enable_auto_commit = False,
            auto_offset_reset='earliest',
            group_id=self.group_name
        )
        def commit():
            consumer.commit()

        for record in consumer:
            msg = record.value
            msg["id"] =generate_file_identifier(msg["absolute_path"],msg["size"])

            yield msg , commit





