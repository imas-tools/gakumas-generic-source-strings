import os, json, warnings
from typing import Dict, List, cast
from utils import yield_string, append_strings

data_dir = "./data"
default_string_file = "./data/default.json"
default_string_split_file = "./data/dafault.split.json"
new_string_dir = "./working/new"


def main():
    strings: Dict[str, List[str]] = {}
    append_strings(strings, data_dir)
    default_strings: List[str] = []
    default_split_strings: List[str] = []
    if os.path.exists(default_string_file):
        with open(default_string_file, "r", encoding="utf-8") as f:
            default_strings = json.load(f)

    for root_path, _, files in os.walk(new_string_dir):
        for file in files:
            file_name = os.path.join(root_path, file)
            if not file_name.endswith(".json"):
                continue
            for string, is_split in yield_string(file_name):
                if string not in strings:
                    if not is_split:
                        default_strings.append(string)
                    else:
                        default_split_strings.append(string)
                    print(f"Added string: {string}")
                else:
                    warnings.warn(f"Duplicate string ignored: {string} in {file_name}")

    with open(default_string_file, "w", encoding="utf-8") as f:
        json.dump(sorted(default_strings), f, ensure_ascii=False, indent=4)
    with open(default_string_split_file, "w", encoding="utf-8") as f:
        json.dump(sorted(default_split_strings), f, ensure_ascii=False, indent=4)
    print("Done")

if __name__ == "__main__":
    main()
