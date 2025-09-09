from kafka import KafkaProducer
import json
from app.logger import Logger
from kafka.errors import NoBrokersAvailable

logger = Logger.get_logger()


class Producer:
    def __init__(self, bootstrap_servers):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info(f"KafkaProducer initialized for brokers: {bootstrap_servers}")
        except NoBrokersAvailable:
            logger.error(f"No Brokers Available to kafka{bootstrap_servers}")

    def send_message(self, topic, value):
        try:
            future = self.producer.send(topic, value=value)
            record_metadata = future.get()
            logger.info(f"Message sent to topic: {record_metadata.topic}, "
                  f"partition: {record_metadata.partition}, "
                  f"offset: {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Error sending message kafka producer {e}")

    def flush_producer(self):
        self.producer.flush()
        self.producer.close()






