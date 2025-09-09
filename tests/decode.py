a = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"

import base64

decoded_bytes = base64.b64decode(a)


decoded_string = decoded_bytes.decode("utf-8")

print(f"Original Base64: {a}")
print(f"Decoded String: {decoded_string}")

b = """
RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=="""

decoded_byte = base64.b64decode(b)

decoded_strin = decoded_byte.decode("utf-8")
print(f"Decoded String: {decoded_strin}")


