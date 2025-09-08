import speech_recognition as sr
from app.logger import Logger

logger = Logger.get_logger()

class SpeachToText:

    @staticmethod
    def audio_to_text(file_path:str, language="en-US"):
        try:
            rec = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio_data =  rec.record(source)
            text = rec.recognize_google(audio_data, language=language)
            logger.info("The audio transcription was successful.")
            return text
        except sr.UnknownValueError:
            logger.error("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        except FileNotFoundError:
            logger.error(f"Error: Audio file not found at {file_path}")

