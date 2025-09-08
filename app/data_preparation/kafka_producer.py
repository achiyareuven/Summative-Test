from kafka import KafkaProducer
import json
from app.logger import Logger
from kafka.errors import NoBrokersAvailable

logger = Logger.get_logger()


class Producer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info(f"KafkaProducer initialized for brokers: {bootstrap_servers}")

    def send_message(self, topic, value,key=None):
        try:
            future = self.producer.send(topic, key=key.encode('utf-8')if key else None, value=value)
            record_metadata = future.get(timeout=10)
            logger.info(f"Message sent to topic: {record_metadata.topic}, "
                  f"partition: {record_metadata.partition}, "
                  f"offset: {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Error sending message kafka producer {e}")

    def flush_producer(self):
        self.producer.flush()






