from app.enrich.utils_decode import decode_base64
from app.enrich.enrich_data import TextProcessor
import nltk
import os
nltk.data.path.append("./nltk_data")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re

hostile = """R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFua
                XRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"""

less_hostile = """RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="""


hostile_list = decode_base64(hostile).lower().split(",")
less_hostile_list = decode_base64(less_hostile).lower().split(",")

pro = TextProcessor(hostile_list,less_hostile_list)
text ="""do you remember the freedom flotilla civilians risking everything to break the blockade with Aid yes that Spirit still inspires activist today it showed resistance doesn't always wear uniforms it can sail with food and medicine and even though governments tried to silence it the message was clear Gaza is not alone that's the essence of global solidarity Ordinary People refusing to accept war crimes as normal Liberation is a journey but every flotilla every protests adds to it exactly justice sales forward no matter the Waze"""


def removing_stopwords(tet):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(tet)
    filtered_words = [w for w in tokens if w.lower() not in stop_words]
    clean_text = ' '.join(filtered_words)
    return clean_text

t =(removing_stopwords(text))
print (t)


print(pro.score_bds(t))


