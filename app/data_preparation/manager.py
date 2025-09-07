from pathlib import Path
from app.data_preparation.initial_processing import Processing
from app.data_preparation.kafka_producer import Producer
import os
from dotenv import load_dotenv
import time

load_dotenv()


class Manager:
    def __init__(self,audio_directory:str = None):
        self.audio_directory =Path (audio_directory or os.getenv("AUDIO_DIRECTORY",r"C:\Users\achiy\PycharmProjects\Summative-Test\podcasts"))
        self.processor = Processing()
        self.producer =Producer()


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




m = Manager()
listi =m.get_meta_data()
m.send_to_kafka(listi,"jjj")
