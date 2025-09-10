a = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"

import base64

decoded_bytes = base64.b64decode(a)


decoded_string = decoded_bytes.decode("utf-8")

print(f"Original Base64: {a}")
print(f"Decoded String: {decoded_string}")

b = """
RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="""

decoded_byte = base64.b64decode(b)

decoded_strin = decoded_byte.decode("utf-8").lower().split(",")
print(f"Decoded String: {decoded_strin}")
tex ="""welcome back today I can't stop thinking about Gaza the blockade
 has turned daily life into a humanitarian crisis families can't even get 
 clean water and the reports of war crimes it's overwhelming some call it 
 genocide and honestly it feels that way when you see the destruction that's 
 why groups like BTS keep pushing boycotts divestments protests their non-violent
  ways to demand accountability exactly and the ICC investigations they give hope
   but people on the ground need relief now food medicine safety Liberation isn't just 
   a slogan it's about dignity ending
 apartheid and giving refugees a chance to live freely and will
  keep amplifying their voices here free Palestine"""

clean = tex.lower().split()


def to_list_pairs_words(text):
    pairs_words = []
    for i in range(len(text) - 1):
        pairs_words.append(f"{text[i]} {text[i + 1]}")

    return pairs_words


print(to_list_pairs_words(clean))

# twoo=[]
# for i in range(len(clean )-1):
#     twoo.append(f"{clean[i]} {clean[i + 1]}")

# print(twoo)
#
# cou = 0
# for tw in twoo:
#     if tw in decoded_strin:
#         cou +=1
# print(cou)



