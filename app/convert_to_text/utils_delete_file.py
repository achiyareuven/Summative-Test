import os
from app.logger import Logger

logger = Logger.get_logger()



def remove_tmp_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"File deleted successfully {file_path} ")
        else:
            logger.info(f"{file_path} is not valid for deletion ")
    except FileNotFoundError:
        logger.error(f"{file_path} not found to delete")
    except Exception as e:
        logger.error(f"error in deleting the file {file_path} ")
