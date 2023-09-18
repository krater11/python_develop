import base64


def encode_to_base64(text):
    encoded_bytes = base64.b64encode(str(text).encode('utf-8'))
    encoded_text = encoded_bytes.decode('utf-8')
    return encoded_text


def decode_from_base64(encoded_text):
    decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text


def is_base64(string):
    try:
        base64.b64decode(string, validate=True)
        return True
    except (base64.binascii.Error, ValueError):
        return False
