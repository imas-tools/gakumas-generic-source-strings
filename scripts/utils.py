import os, json, warnings
from typing import Dict, List, cast, Tuple, Generator

SPLIT_STRING_PREFIX = "[__split__]"

# yield (string, is_split)
def yield_string(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")

        for k in content:
            yield (cast(str, k), (cast(str, k).startswith(SPLIT_STRING_PREFIX)))


def append_strings(strings: Dict[str, List[str]], dir_path: str):
    for root_path, _, files in os.walk(dir_path):
        for file in files:
            file_name = os.path.join(root_path, file)
            if not file_name.endswith(".json"):
                continue
            for string, is_split in yield_string(file_name):
                if string not in strings:
                    strings[string] = []
                strings[string].append(file_name)
