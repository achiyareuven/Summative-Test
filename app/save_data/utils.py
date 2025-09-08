import hashlib


def generate_file_identifier(file_path ,size):
    try:
        identifier_string = f"{file_path}-{size}"
        unique_id = hashlib.sha256(identifier_string.encode('utf-8')).hexdigest()
        return unique_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None