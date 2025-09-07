from app.dal.es_client import Elastic
from app.save_data.kafka_consumer import Consumer



class Manager:
    def __init__(self, elastic: Elastic,mapping:dict=None,):
        self.elastic  = elastic
        self.consumer = Consumer("jjj","dds")

    def reset_index(self):
        self.elastic.create_index()

    def index_doc(self, doc: dict, doc_id=None):
        return self.elastic.es.index(index=self.elastic.index_name, id=doc_id, document=doc)


    def




