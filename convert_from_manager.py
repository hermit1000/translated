import json
from pathlib import Path
from datetime import datetime


def main():
    platform = "msx2"
    source_path = Path(f"c:/work/rom-manager/roms/{platform}/gamelist.json")
    if not source_path.exists():
        print(f"Source file not found: {source_path}")
        return

    with open(source_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert
    target_data = dict()

    for k, v in data.items():
        if "(kr)" not in k.lower():
            continue

        # Original name
        v_original = data[k.replace(" translated (KR)", "")]

        key = v["name"]

        date_str = v["releasedate"].split("T")[0]
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")

        value = {
            "developer": v["developer"],
            "genre": v["genre"],
            "loc_url": v.get("loc_url", "Unknown"),
            "localization": v.get("localization", "Unknown"),
            "platform": platform,
            "release": formatted_date,
            "title": {
                "eng": v_original["name"],
                # "jpn": original,
                "kor": key,
            },
        }

        target_data[key] = value

    with open(f"./data/{platform}.json", "w", encoding="utf-8") as f:
        json.dump(target_data, f, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
