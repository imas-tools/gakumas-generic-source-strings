import os, json, warnings
from typing import Dict, List, cast, Tuple, Generator

SPLIT_STRING_PREFIX = "[split]"

# yield (string, is_split)
def yield_string(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")

        if isinstance(content, dict):
            for k, v in content.items():
                if k == v:
                    if v.startswith(SPLIT_STRING_PREFIX):
                        # warnings.warn(
                        #     "Key and value are the same and start with [split], this might be a mistake"
                        # )
                        raise ValueError(
                            "Key and value are the same and start with [split], this might be a mistake"
                        )
                    yield (cast(str, v), False)
                else:
                    if not isinstance(v, str) or not v.startswith(SPLIT_STRING_PREFIX):
                        raise ValueError(
                            f"Invalid split string: {v}, should start with {SPLIT_STRING_PREFIX}"
                        )
                    yield (cast(str, v), True)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    yield (cast(str, item), (not item.startswith(SPLIT_STRING_PREFIX)))
                else:
                    raise ValueError("Invalid list item, should be a string")
        else:
            raise TypeError("Unsupported JSON content type")

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
