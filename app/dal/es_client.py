from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class Elastic:
    def __init__(self, url: str, index_name: str, timeout: int = 30):
        self.url = url
        self.index_name = index_name
        self.timeout = timeout
        self.es = Elasticsearch(self.url, request_timeout=self.timeout)
        if not self.es.ping():
            raise ValueError("Connection failed")

    def create_index(self,):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(
                    index=self.index_name,

                )
        except Exception as e:
            print(f"error creating index: {e}")


    def bulk_insert(self, docs: list,doc_id):
        try:
            actions = (
                {"_index": self.index_name, "_id": doc_id, "_source": doc}
                for i, doc in enumerate(docs)
            )
            bulk(self.es, actions)
            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"error inserting documents: {e}")

    def ensure_field_mapping(self, field: str, field_mapping: dict):
        mapping = self.es.indices.get_mapping(index=self.index_name)
        properties = mapping[self.index_name]["mappings"].get("properties", {})
        if field in properties:
            return
        self.es.indices.put_mapping(
            index=self.index_name,
            properties={field: field_mapping}
        )

    def delete_documents_by_id(self, ids: list):
        try:
            actions = (
                {"_op_type": "delete", "_index": self.index_name, "_id": doc_id}
                for doc_id in ids
            )
            bulk(self.es, actions)
            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"error deleting documents: {e}")

    def update_docs(self,docs_to_update:list):
        try:
            actions= [
                {"_op_type": "update",
                    "_index": self.index_name,
                    "_id": doc_id,
                    "doc": doc_fields}
                for doc_id, doc_fields in docs_to_update
            ]
            bulk(self.es,actions)
            self.es.indices.refresh(index=self.index_name)
        except Exception as e :
            print(f"error update docs {e}")

    def count(self):
        return self.es.count(index=self.index_name)["count"]

    def search(self, query: dict, size: int = 10):
        return self.es.search(index=self.index_name, body=query)

    def close(self):
        self.es.transport.close()
