import hashlib


def hash_string(string, method="sha256"):

    hash_object = hashlib.new(method)
    hash_object.update(string.encode("utf-8"))
    hash_value = hash_object.hexdigest()

    return hash_value