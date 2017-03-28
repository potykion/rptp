import json
import os


def save_as_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)


def load_json_list(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return []


def update_json_list(objects, path):
    loaded_objects = load_json_list(path)
    loaded_objects.extend(objects)
    save_as_json(loaded_objects, path)


def load_json_dict(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return {}


def update_json_dict(dict_, path):
    loaded_dict = load_json_dict(path)
    loaded_dict.update(dict_)
    save_as_json(loaded_dict, path)


