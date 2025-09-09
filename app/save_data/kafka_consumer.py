from kafka import KafkaConsumer
from dotenv import load_dotenv
from utils import generate_file_identifier
from kafka.errors import NoBrokersAvailable
from app.logger import Logger
import os
import json

load_dotenv()
logger = Logger.get_logger()



class Consumer:
    def __init__(self,topic,group,bootstrap_servers=None):
        self.topic = topic
        self.group_name = group
        self.bootstrap_servers = bootstrap_servers or os.getenv("BOOTSTRAP_SERVERS")
        self.consumer= None


    def get_consumer_events(self):
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                bootstrap_servers=[self.bootstrap_servers],
                enable_auto_commit = False,
                auto_offset_reset='earliest',
                group_id=self.group_name
            )
            def commit():
                self.consumer.commit()

            for record in self.consumer:
                msg = record.value
                msg["id"] =generate_file_identifier(msg["absolute_path"],msg["size"])

                yield msg , commit

        except NoBrokersAvailable:
            logger.error(f"No Brokers Available to kafka  {self.bootstrap_servers} failed")
            raise

        except Exception as e:
            logger.error(f"error {e}")

        finally:
            self.consumer.close()





