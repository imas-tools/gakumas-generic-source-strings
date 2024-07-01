from typing import Dict, List
from utils import append_strings

data_dir = "./data"
new_string_dir = "./working/new"


def check_duplicate(strings: Dict[str, List[str]]):
    found = False
    for string in strings:
        if len(strings[string]) > 1:
            found = True
            print(f"Duplicate string: {repr(string)}")
            for file_name in strings[string]:
                print(f"\t{file_name}")
    if found:
        raise Exception("Duplicate strings found!")


def main():
    strings: Dict[str, List[str]] = {}
    append_strings(strings, data_dir)
    check_duplicate(strings)
    append_strings(strings, new_string_dir)
    check_duplicate(strings)
    
    print("No duplicate strings found!")


if __name__ == "__main__":
    main()
