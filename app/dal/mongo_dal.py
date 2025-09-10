from pymongo import MongoClient
from gridfs import GridFS
from app.logger import Logger
import os
import tempfile

logger = Logger.get_logger()

class MongoDAL:
    def __init__(self, url, db_name, collection):
        self.url = url or os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        self.db_name = db_name or os.getenv("MONGO_DB", "appdb")
        self.collection_name = collection or os.getenv("MONGO_COLLECTION", "docs")

        self.client = MongoClient(self.url)
        self.db = self.client[self.db_name]
        self.fs =GridFS(database=self.db,collection=self.collection_name)

    def insert_audio_file(self,audio_file_path,id_file):
        try:
            with open(audio_file_path, 'rb') as audio_data:
                file_id = self.fs.put(audio_data, _id=id_file)
                logger.info(f"Audio file saved with ID: {file_id}")
        except FileNotFoundError:
            logger.error(f"Error: Audio file not found at {audio_file_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    def get_audio_file(self,id_file,file_name):
        try:
            file_data = self.fs.find_one({"_id": id_file})
            if file_data:
                with open(rf'..\{file_name}', 'wb') as output_file:
                    output_file.write(file_data.read())
                logger.info("File downloaded successfully")
                return output_file.name
            else:
                logger.info("File not found")
        except FileNotFoundError:
            logger.error(f"File not found with id {id_file}")
        except Exception as e:
            logger.error(f"error to get file from mongo with id {id_file}")

    def get_temp_audio_file(self,id_file,file_name):
            file_data = self.fs.get(id_file)
            fd, temp_path =tempfile.mkstemp()
            os.close(fd)
            with open(temp_path,"wb") as output_file:
                output_file.write(file_data.read())
                logger.info("File downloaded successfully")
            return output_file.name




    def close(self):
        self.client.close()
