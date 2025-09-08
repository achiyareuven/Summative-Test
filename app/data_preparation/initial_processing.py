from pathlib import Path
import os
from tinytag import TinyTag
import datetime
from app.logger import Logger
import uuid

logger = Logger.get_logger()

class Processing:

    @staticmethod
    def meta_data_to_dict(audio_file):
        try:
            file_stats = audio_file.stat()
            creation_timestamp = file_stats.st_ctime
            dict_resulte = {}
            if audio_file.is_file() and audio_file.suffix in [".mp3", ".wav", ".flac"]:
                tag = TinyTag.get(str(audio_file))
                dict_resulte["absolute_path"] = tag.filename
                dict_resulte["name"] = audio_file.name
                dict_resulte["creation_timestamp"] =datetime.datetime.fromtimestamp(creation_timestamp).isoformat()
                dict_resulte["size"] = file_stats.st_size
                dict_resulte["duration"] =tag.duration
                logger.info(f"Successfully extracted metadata into a dictionary for {audio_file}")
                return dict_resulte
            else:
                logger.error(f"File not found: {audio_file}")
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")














