import os
from app.dal.es_client import Elastic
from app.dal.mongo_dal import MongoDAL
from app.save_data.kafka_consumer import Consumer
from app.save_data.producer_to_stt import Producer
from dotenv import load_dotenv
from app.logger import Logger


logger = Logger.get_logger()
load_dotenv()

MONGO_URL=os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "appdb")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "docs")

ES_URI = os.getenv("ES_URI","http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX","audio_docs")

BOOTSTRAP_SERVERS= os.getenv("BOOTSTRAP_SERVERS","localhost:9092")
KAFKA_TOPIC =os.getenv("KAFKA_TOPIC","audio_meta")
KAFKA_GROUP = os.getenv("KAFKA_GROUP","read_meta")

KAFKA_TOPIC_STT = os.getenv("KAFKA_TOPIC_STT","stt")




class Manager:
    def __init__(self, elastic: Elastic):
        self.elastic  = elastic
        self.consumer = Consumer(KAFKA_TOPIC,KAFKA_GROUP)
        self.mongo= MongoDAL(MONGO_URL,MONGO_DB,MONGO_COLLECTION)
        self.producer = Producer(BOOTSTRAP_SERVERS)


    def run(self):
        try:
            for msg, commit in self.consumer.get_consumer_events():
                try:
                    if not msg["id"] or not msg["absolute_path"]:
                        logger.info(f"No path or id found Skip message{msg}")
                        continue
                    self.mongo.insert_audio_file(msg["absolute_path"],msg["id"])


                    if self.elastic.es.exists(index=self.elastic.index_name, id=msg["id"]):
                        logger.info(f"Document with ID '{msg["id"]}'already exists in index '{self.elastic.index_name}'.")
                    else:
                        self.elastic.index_doc(msg,msg["id"])
                        logger.info(f"save doc with ID {msg["id"]} to elastic ")

                    self.producer.send_message(KAFKA_TOPIC_STT,msg)

                except Exception as e:
                    logger.error(f"some error update doc with id {msg["id"]} {e}")
                    continue

                commit()
        except Exception as e:
            logger.error(f"error save data {e}")

if __name__ == "__main__":
    try:
        my_elastic = Elastic(ES_URI, ES_INDEX)
        manager = Manager(my_elastic)
        manager.run()
    finally:
        manager.elastic.close()
        manager.mongo.close()
        manager.producer.flush_producer()












