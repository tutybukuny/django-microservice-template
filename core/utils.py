import json
from types import SimpleNamespace


def load_json_file(file_path):
    with open(file_path) as json_file:
        obj = json.loads(json_file.read(), object_hook=lambda d: SimpleNamespace(**d))
    return obj
