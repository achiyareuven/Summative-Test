from pathlib import Path
from app.data_preparation.initial_processing import Processing
from app.data_preparation.kafka_producer import Producer
import os
from dotenv import load_dotenv
import time

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
        list_meta_data=[]
        for audio_file in self.audio_directory.iterdir():
            dict_neta_data = self.processor.meta_data_to_dict(audio_file)
            list_meta_data.append(dict_neta_data)
        return list_meta_data

    def send_to_kafka(self,list_msg,kafka_topic):
        for i, msg_data in enumerate(list_msg):
            self.producer.send_message(kafka_topic, msg_data)
            time.sleep(0.1)
        self.producer.flush_producer()

if __name__ == "__main__":
    manager = Manager(AUDIO_DIRECTORY)
    list_data = manager.get_meta_data()
    manager.send_to_kafka(list_data, KAFKA_TOPIC)

