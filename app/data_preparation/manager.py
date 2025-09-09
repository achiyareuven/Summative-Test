
from pathlib import Path
from app.data_preparation.initial_processing import Processing
from app.data_preparation.kafka_producer import Producer
from app.logger import Logger
import os
from dotenv import load_dotenv
import time

logger = Logger.get_logger()

load_dotenv()

AUDIO_DIRECTORY= os.getenv("AUDIO_DIRECTORY",r"C:\Users\achiy\PycharmProjects\Summative-Test\podcasts")
BOOTSTRAP_SERVERS= os.getenv("BOOTSTRAP_SERVERS","localhost:9092")
KAFKA_TOPIC =os.getenv("KAFKA_TOPIC","audio_meta")


class Manager:
    def __init__(self,audio_directory:str ):
        self.audio_directory =Path(audio_directory)
        self.processor = Processing()
        self.producer =Producer(BOOTSTRAP_SERVERS)


    def get_meta_data(self):
        try:
            list_meta_data=[]
            for audio_file in self.audio_directory.iterdir():
                dict_neta_data = self.processor.meta_data_to_dict(audio_file)
                list_meta_data.append(dict_neta_data)
            logger.info("Successfully received metadata into list")
            return list_meta_data
        except FileNotFoundError:
            logger.error(f"Error: Audio file not found at {self.audio_directory}")
        except Exception as e:
            logger.error(f"Error receiving metadata {e}")



    def send_to_kafka(self,list_msg,kafka_topic):
        try:
            for i, msg_data in enumerate(list_msg):
                self.producer.send_message(kafka_topic, msg_data)

            self.producer.flush_producer()
            logger.info("All files were sent successfully.")
        except Exception as e:
            logger.error(f"Error sending files in Kafka producer {e}")

if __name__ == "__main__":
    try:
        logger.info("The program has started")
        manager = Manager(AUDIO_DIRECTORY)
        list_data = manager.get_meta_data()
        manager.send_to_kafka(list_data, KAFKA_TOPIC)
    finally:
        manager.producer.flush_producer()

