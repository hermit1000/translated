import os
import json
from pathlib import Path


def main():
    with open("list_pc98.json", "r", encoding="utf-8") as f:
        pc98_list = json.load(f)

    with open("list.txt", "r", encoding="utf-8") as f:
        candidate = f.read().splitlines()

    for candidate in candidate:
        if candidate == "":
            continue

        if candidate not in pc98_list.keys():
            print(candidate)


if __name__ == "__main__":
    main()
