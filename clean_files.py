"""This script cleans the files in the dirty folder and outputs them \
    to the clean folder, creating a sql database in the process."""

import re
from glob import glob

import modules.constants as constants
from modules.database import MK8Deluxe


def open_file(path: str) -> list[str]:
    """Open a file and return a list of lines.

    Args:
        path (str): path to the file

    Returns:
        list[str]: list of lines
    """
    with open(path) as f:
        lines = [
            line.strip()
            for line in f.readlines()
            if line.strip() and "icon" not in line.lower()
        ]

    return lines


def clean_file(lines: list) -> list[str]:
    """Clean the lines of the file.

    Args:
        lines (list[str]): list of lines

    Returns:
        list[str]: list of cleaned lines
    """
    clean_lines = []

    lines = [line for line in lines if "Mario Kart 8" not in line]
    for x in range(len(lines)):
        if not re.match(r".+\s+\d+", lines[x]):
            continue

        clean_lines.append(re.sub(r"(\S+)(\s{2,})", r"\1,", lines[x]))
    return clean_lines


def clean_drivers(lines: list) -> list[str]:
    """Clean the lines of the drivers file.

    Args:
        lines (list)

    Returns:
        list[str]
    """

    def find_number(s: str) -> int:
        for i, c in enumerate(s):
            if c.isdigit():
                return i

        return -1

    clean_lines = []

    max_attributes = len(constants.CSV_ATTRIBUTES.keys()) - 2
    x = 0
    while x < len(lines):
        if "head icon" in lines[x].lower():
            continue

        first_digit = find_number(lines[x])
        if first_digit == -1:
            name = lines[x]
            fist_stat = find_number(lines[x + 1])
            stats_line = lines[x + 1][fist_stat:]
            x += 2
        else:
            name = lines[x][:first_digit].strip()
            stats_line = lines[x][first_digit:]
            x += 1

        raw_stats = re.findall(r"\d+", stats_line)
        if len(raw_stats) > max_attributes:
            stats = ",".join(raw_stats[len(raw_stats) - max_attributes :])
        else:
            stats = ",".join(raw_stats)

        clean_lines.append(f"{name},{stats}")

    return clean_lines


def extract_stats(line: str) -> tuple[str, ...]:
    """Extract the stats from a line.

    Args:
        line (str)

    Returns:
        tuple[str, ...]
    """
    name, *stats = line.split(",")
    return name, ",".join(stats)


def merge_lines(lines: list[str]) -> tuple[list[str], list[str]]:
    """Merge the lines with the same stats.

    Args:
        lines (list[str])

    Returns:
        list[str], list[str]: merged lines, ids
    """
    merged = dict()

    for line in lines[1:]:
        name, stats = extract_stats(line)

        if stats in merged:
            merged[stats].append(name)
        else:
            merged[stats] = [name]

    ids = ["name,id"]
    merged_lines = []
    current_id = 0
    for stats, names in merged.items():
        merged_lines.append(f"{current_id},{stats}")
        for name in names:
            ids.append(f"{name},{current_id}")
        current_id += 1

    merged_lines.sort()
    new_header = f"id,{','.join(lines[0].split(',')[1:])}"
    merged_lines.insert(0, new_header)

    return merged_lines, ids


def write_file(path: str, lines: list[str]) -> None:
    """Write the lines to a file.

    Args:
        path (str): path to the file
        lines (list[str]): list of lines

    Returns:
        None
    """
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def create_path(path: str, folder: str, suffix: str = None) -> str:
    """Create a path to a file.

    Args:
        path (str): path to the file
        folder (str): folder to put the file in
        suffix (str, optional): suffix to add to the file name. Defaults to None.

    Returns:
        str: path to the file
    """
    folders = path.split("/")[:-1]
    filename = path.split("/")[-1]

    if suffix:
        return (
            f"{'/'.join(folders[:-1])}/{folder}/{filename.split('.')[0]}_{suffix}.csv"
        )

    return f"{'/'.join(folders[:-1])}/{folder}/{filename.split('.')[0]}.csv"


def add_to_database(lines: list[str], table: str) -> None:
    """Add the lines to the database.

    Args:
        lines[str] (list)
        table (str)

    Returns:
        None
    """
    d = MK8Deluxe()
    # if the table exists, delete it
    if d.tableExists(table):
        d.deleteTable(table)

    # create the table
    cols = [constants.CSV_ATTRIBUTES[x] for x in lines[0].split(",")]
    types = ["STRING" if x == "name" else "INTEGER" for x in cols]
    d.createTable(table, cols, types)

    # add the data
    for line in lines[1:]:
        values = [x.strip() for x in line.split(",")]
        d.insert(table, cols, values)

    d.commitChanges()


def clean(path: str) -> str:
    """Clean the file.

    Args:
        path (str): path to the file

    Returns:
        str: path to the cleaned file
    """
    lines = open_file(path)
    clean_lines = []

    # replace multiple spaces with a comma
    header = re.sub(r"(\S+)(\s{2,})", r"\1,", lines[0])
    clean_lines.append(header)

    if "driver" in path.lower():
        clean_lines.extend(clean_drivers(lines[1:]))
    else:
        clean_lines.extend(clean_file(lines[1:]))

    out_path = create_path(path, "clean")
    write_file(out_path, clean_lines)

    merged, ids = merge_lines(clean_lines)
    merged_path = create_path(path, "merged")
    write_file(merged_path, merged)
    ids_path = create_path(path, "merged", "names")
    write_file(ids_path, ids)

    filename = path.split("/")[-1].split(".")[0]
    add_to_database(merged, filename)
    add_to_database(ids, f"{filename}_names")

    return out_path


def main() -> None:
    """Clean all the files in the dirty folder."""
    dirty_path = "data/dirty/*.csv"
    for path in glob(dirty_path):
        clean(path)
        print(f"Cleaned {path}")


if __name__ == "__main__":
    main()
