import os
from app.dal.es_client import Elastic
from app.dal.mongo_dal import MongoDAL
from app.enrich.consumer_enrich import Consumer
from app.enrich.enrich_data import TextProcessor
from app.enrich.utils_clear_text import *
from app.enrich.utils_decode import decode_base64
from dotenv import load_dotenv
from app.logger import Logger
from app.convert_to_text.utils_delete_file import remove_tmp_file


logger = Logger.get_logger()
load_dotenv()

ES_URI = os.getenv("ES_URI","http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX","audio_docs")

KAFKA_TOPIC_ENRICH = os.getenv("KAFKA_TOPIC_ENRICH","enrich")
KAFKA_GROUP_ENRICH = os.getenv("KAFKA_GROUP_ENRICH","enrich_data")

HOSTILE = os.getenv("HOSTILE")
HOSTILE_LESS = os.getenv("HOSTILE_LESS")



class Manager:
    def __init__(self, elastic: Elastic):
        self.elastic  = elastic
        self.consumer = Consumer(KAFKA_TOPIC_ENRICH,KAFKA_GROUP_ENRICH)
        self.text_process= TextProcessor(decode_base64(HOSTILE),decode_base64(HOSTILE_LESS))


    def get_new_fields(self,text):
        dict_new_fields = self.get_new_fields(text)
        return dict_new_fields



    def run(self):
        try:
            for msg, commit in self.consumer.get_consumer_events():
                try:
                    if not msg["id"] or not msg["text"]:
                        logger.info(f"No text or id found Skip message{msg}")
                        continue
                    if not self.elastic.check_field_exists_in_document(msg["id"],"is_bds"):

                        new_values = self.get_new_fields(msg["text"])
                        self.elastic.update_doc(msg["id"],new_values)
                        logger.info(f"Document with ID {msg["id"]}  updated successfully for enrich")

                    else:
                        logger.info(f"Document with ID {msg["id"]} already updated for enrich")

                except Exception as e:
                    logger.error(f"some error update doc with id {msg["id"]} {e}")
                    continue

                commit()
        except Exception as e:
            logger.error(f"error data read message {e}")


if __name__ == "__main__":
    try:
        my_elastic = Elastic(ES_URI, ES_INDEX)
        manager = Manager(my_elastic)
        manager.run()
    finally:
        manager.elastic.close()



