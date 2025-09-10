from elasticsearch import Elasticsearch, exceptions
from elasticsearch.helpers import bulk
from app.logger import Logger

logger = Logger.get_logger()


class Elastic:
    def __init__(self, url: str, index_name: str, timeout: int = 30):
        self.url = url
        self.index_name = index_name
        self.timeout = timeout

        try:
            self.es = Elasticsearch(self.url, request_timeout=self.timeout)
            if not self.es.ping():
                logger.error("Elasticsearch is not responding")
                raise exceptions.ConnectionError("Elasticsearch is not responding")
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name)
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise


    def index_doc(self, doc: dict, doc_id=None):
        try:
            result = self.es.index(index=self.index_name, id=doc_id, document=doc)
            logger.info("Document indexing successfully ")
            return result
        except Exception as e:
            logger.error(f"Indexing doc failed: {e}")

    def check_field_exists_in_document(self, doc_id: str, field_name: str) -> bool:
        try:
            logger.info("Checking if a field exists in doc")
            response = self.es.get(index=self.index_name, id=doc_id, _source_includes=[field_name])
            if response.get('found') and field_name in response['_source']:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f"Error checking field existence: {e}")
            return False

    def update_doc(self, doc_id: str, new_values: dict):
        try:
            result = self.es.update(index=self.index_name, id=doc_id, body={"doc": new_values})
            logger.info(f"Updated doc id with{doc_id}")
            return result
        except Exception as e:
            logger.error(f"Update failed: {e}")


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
