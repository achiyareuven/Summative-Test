from app.dal.mongo_dal import MongoDAL

path =r"C:\Users\achiy\Downloads\audio-data\cv-corpus-19.0-delta-2024-09-13\en\clips\common_voice_en_41227191.mp3"
a = MongoDAL()
a.insert_audio_file(path,1)
print(a.list_all())