from pathlib import Path
import os
from tinytag import TinyTag
import time
import datetime

audio_file_path = Path(r"C:\Users\achiy\PycharmProjects\Summative-Test\podcasts\download.wav")
file_stats = audio_file_path.stat()
# Extract creation timestamp (st_ctime)
# creation_timestamp = file_stats.st_ctime
# creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
# print(f"The creation date of '{audio_file_path.name}' is: {creation_datetime}")
# timew = st.st_ctime()
# print(timew)

# print(audio_file_path.resolve())
# if audio_file_path.is_file():
#     print(f"{audio_file_path.name} is a file.")
#     print(type(audio_file_path.name))
#
# if audio_file_path.exists():
#     print(f"{audio_file_path} exists.")

audio_directory = Path(r"C:\Users\achiy\PycharmProjects\Summative-Test\podcasts")
for audio_file in audio_directory.iterdir():
    if audio_file.is_file() and audio_file.suffix in [".mp3", ".wav", ".flac"]:
        print(audio_file.name)
        print(f"Found audio file: {audio_file.match}")
        creation_timestamp = os.path.getctime(audio_file)
        creation_date = time.ctime(creation_timestamp)
        print(f"File system creation date: {creation_date}")


        try:
            # Extract metadata using TinyTag, passing the path as a string
            tag = TinyTag.get(str(audio_file))
            print(tag.as_dict())
            print(tag.comment)
            print(tag.filename)
            print(audio_file.match)
            # # Access and print desired metadata attributes
            # print(f"Title: {tag.title}")
            # print(f"Artist: {tag.artist}")
            # print(f"Album: {tag.album}")
            # print(f"Duration (seconds): {tag.duration}")
            # print(f"Genre: {tag.genre}")
            # print(f"Year: {tag.year}")
        except Exception as e:
            print(f"Error extracting metadata: {e}")
    else:
        print(f"File not found: {audio_file}")