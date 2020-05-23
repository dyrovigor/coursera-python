import os
import tempfile
import argparse
import json


def read_json_from_file(file_path):
    with open(file_path, 'r') as f:
        try:
            dump = json.load(f)
            f.close()
            return dump
        except json.decoder.JSONDecodeError:
            return {}


def write_json_to_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.close()


if __name__ == '__main__':
    storage_file_name = "storage.data"
    
    parser = argparse.ArgumentParser(description="key, value? for insertion/reading")
    parser.add_argument("-k", "--key", type=str, help="key name")
    parser.add_argument("-v", "--value", required=False, type=str, help="which value you'd like to insert")
    args = parser.parse_args()
    
    key = args.key
    value = args.value
    
    storage_path = os.path.join(tempfile.gettempdir(), storage_file_name)
    
    data_to_save = {}
    value_from_dict = None

    if os.path.exists(storage_path):
        data_to_save = read_json_from_file(storage_path)
        value_from_dict = data_to_save.get(key)

    if value is None:
        print(value_from_dict)
    else:
        data_to_save[key] = value if value_from_dict is None else '{}, {}'.format(value_from_dict, value)
        write_json_to_file(storage_path, data_to_save)
