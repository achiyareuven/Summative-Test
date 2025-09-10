import logging
import os
from elasticsearch import Elasticsearch
from datetime import datetime





class Logger:
    ES_URI = os.getenv("ES_URI", "http://localhost:9200")
    ES_INDEX_LOGGER = os.getenv("ES_INDEX_LOGGER", "logs")
    LOGGER_NAME = os.getenv("LOGGER_NAME", "app_logs")


    _logger = None
    @classmethod
    def get_logger(cls, name=LOGGER_NAME, es_host=ES_URI,index=ES_INDEX_LOGGER, level=logging.DEBUG):
        if cls._logger:
            return cls._logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            es = Elasticsearch(es_host)
            class ESHandler(logging.Handler):
                def emit(self, record):
                    try:
                        es.index(index=index, document={
                        "timestamp": datetime.utcnow().isoformat(),
                        "level": record.levelname,
                        "logger": record.name,
                        "message": record.getMessage()

                        })
                    except Exception as e:
                        print(f"ES log failed: {e}")
            logger.addHandler(ESHandler())
            logger.addHandler(logging.StreamHandler())
            cls._logger = logger
            return logger