import json

def pretty_print(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))
