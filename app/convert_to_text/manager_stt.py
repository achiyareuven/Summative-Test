import os
from app.dal.es_client import Elastic
from app.dal.mongo_dal import MongoDAL
from app.convert_to_text.consumer_stt import Consumer
from app.convert_to_text.audio_processor import SpeachToText
from dotenv import load_dotenv
from app.logger import Logger
from app.convert_to_text.utils_delete_file import remove_tmp_file
from app.convert_to_text.producer_to_enrich import Producer


logger = Logger.get_logger()
load_dotenv()

MONGO_URL=os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "appdb")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "docs")

ES_URI = os.getenv("ES_URI","http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX","audio_docs")

BOOTSTRAP_SERVERS= os.getenv("BOOTSTRAP_SERVERS","localhost:9092")
KAFKA_TOPIC_STT = os.getenv("KAFKA_TOPIC_STT","stt")
KAFKA_GROUP_STT = os.getenv("KAFKA_GROUP_STT","convert_to_text")

KAFKA_TOPIC_ENRICH = os.getenv("KAFKA_TOPIC_ENRICH","enrich")



class Manager:
    def __init__(self, elastic: Elastic):
        self.elastic  = elastic
        self.consumer = Consumer(KAFKA_TOPIC_STT,KAFKA_GROUP_STT)
        self.mongo= MongoDAL(MONGO_URL,MONGO_DB,MONGO_COLLECTION)
        self.sst = SpeachToText()
        self.producer = Producer(BOOTSTRAP_SERVERS)


    def get_text(self,path_audio_file):
        text = self.sst.audio_to_text(path_audio_file)
        return text

    def run(self):
        try:
            for msg, commit in self.consumer.get_consumer_events():
                try:
                    if not msg["id"] or not msg["name"]:
                        logger.info(f"No name or id found Skip message{msg}")
                        continue
                    if not self.elastic.check_field_exists_in_document(msg["id"],"text"):

                        path_audio_file= self.mongo.get_temp_audio_file(msg["id"],msg["name"])
                        text = self.get_text(path_audio_file)
                        self.elastic.update_doc(msg["id"],{"text":text})

                        remove_tmp_file(path_audio_file)

                        self.producer.send_message(KAFKA_TOPIC_ENRICH,{"id":msg["id"],"text":text})

                    else:
                        logger.info(f"Document with ID '{msg["id"]}'already updated'")

                except Exception as e:
                    logger.error(f"some error update doc with id {msg["id"]} {e}")
                    continue

                commit()
        except Exception as e:
            logger.error(f"error  data {e}")

if __name__ == "__main__":
    try:
        my_elastic = Elastic(ES_URI, ES_INDEX)
        manager = Manager(my_elastic)
        manager.run()
    finally:
        manager.elastic.close()
        manager.mongo.close()


