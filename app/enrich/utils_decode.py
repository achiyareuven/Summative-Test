import base64
from app.logger import Logger

logger = Logger.get_logger()



def decode_base64(strint_to_decode):
    try:
        decoded_bytes = base64.b64decode(strint_to_decode)
        decoded_string = decoded_bytes.decode("utf-8")
        logger.info("Decoding was successful")

        return decoded_string
    except Exception as e:
        logger.error("Decoding failed.")