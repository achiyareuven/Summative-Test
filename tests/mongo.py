# path =r"C:\Users\achiy\Downloads\audio-data\cv-corpus-19.0-delta-2024-09-13\en\clips\common_voice_en_41227191.mp3"
# a = MongoDAL()
# a.insert_audio_file(path,1)
# print(a.list_all())
import os
from app.convert_to_text.utils_delete_file import remove_tmp_file
from app.dal.mongo_dal import MongoDAL
from app.convert_to_text.audio_processor import SpeachToText

a = MongoDAL("mongodb://localhost:27017/","appdb","docs")
b= SpeachToText()
s =a.get_temp_audio_file("b7e9f668b2b832c6c185694b9472588d6d8e2bb2e157d638bc6b79e26c1c47db","download (33).wav")

# print(b.audio_to_text(s))
print(s)
p = s
remove_tmp_file(p)


# myfile = s
# # If file exists, delete it.
# if os.path.isfile(myfile):
#     os.remove(myfile)
# else:
#     # If it fails, inform the user.
#     print("Error: %s file not found" % myfile)

#









# def get_temp(self,id_f):
#     file_data = self.fs.find_one({"_id": id_f})
#     if file_data:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
#             temp_audio_file.write(file_data.read())
#             temp_file_path = temp_audio_file.name
#
#             print(f"Audio file saved to temporary location: {temp_file_path}")

