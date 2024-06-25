import os, json
from typing import Dict, List, cast


def yield_string(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        f = json.load(f)
        for k in f:
            yield cast(str, k)

def append_strings(strings: Dict[str, List[str]], dir_path: str):
    for root_path, _, files in os.walk(dir_path):
        for file in files:
            file_name = os.path.join(root_path, file)
            if not file_name.endswith(".json"):
                continue
            for string in yield_string(file_name):
                if string not in strings:
                    strings[string] = []
                strings[string].append(file_name)
