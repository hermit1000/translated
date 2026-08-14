import json
from rich.console import Console
from rich.table import Table
from rich.text import Text


possible_platforms = ["dos", "msx", "megadrive", "nes", "pc98"]


def get_target_keys(data: dict, developer_selection: list) -> list:
    out_list = list()
    for k, v in data.items():
        developer = v.get("developer", "N/A").lower()
        if len(developer_selection) and developer not in developer_selection:
            continue
        out_list.append(k)
    return out_list


def data_read(file_name: str, developer_selection: list) -> tuple[list, dict]:
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        target_keys = get_target_keys(data, developer_selection)

    return target_keys, data


def put_data_to_table(
    key: str, data: dict, table: Table, developer_selection: list, stat: dict
):
    v = data[key]
    developer = v.get("developer", "N/A").lower()
    if len(developer_selection) and developer not in developer_selection:
        pass
    else:
        localization = v.get("localization", "N/A")

        persons = localization.replace("*", "").split(",")
        for p in persons:
            if p not in stat:
                stat[p] = 1
            else:
                stat[p] += 1

        if "*" in localization:
            localization = Text(localization.replace("*", ""), style="bright_green")

        table.add_row(
            key,
            v.get("developer", "N/A"),
            v.get("release", "N/A").split("-")[0],
            v.get("platform", "N/A"),
            localization,
            v.get("loc_url", ""),
        )


def main():
    platform_selection = ["dos", "pc98", "msx"]
    developer_selection = ["koei"]  # lower case

    platform_selection = ["pc98"]
    developer_selection = []  # lower case

    database = dict()
    stat = dict()
    target_set = set()

    if len(platform_selection) == 0:
        print("Please select platform")
        return

    for platform in platform_selection:
        if platform not in possible_platforms:
            print(f"Invalid platform: {platform}")
            return

        target_list, data = data_read(f"./data/{platform}.json", developer_selection)
        database[platform] = data
        target_set.update(target_list)

    target_list = list(target_set)
    target_list.sort()

    console = Console()
    table = Table(title="List of games")
    table.add_column("타이틀", justify="left", style="bright_white")
    table.add_column("제작", justify="left", style="cyan")
    table.add_column("릴리즈", justify="left", style="blue")
    table.add_column("플랫폼", justify="left", style="bright_red")
    table.add_column("한글화", justify="left", style="yellow")
    table.add_column("패치 주소", justify="left", style="bright_white")

    for k in target_list:
        for platform in platform_selection:
            if k in database[platform]:
                put_data_to_table(
                    k, database[platform], table, developer_selection, stat
                )

    console.print(table)

    # To check contribution
    stat = dict(sorted(stat.items(), key=lambda item: item[1], reverse=True))
    for i, (k, v) in enumerate(stat.items(), start=1):
        print(f"{i:02d}: {k} ({v})")


if __name__ == "__main__":
    main()
