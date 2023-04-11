import re
from glob import glob


def open_file(path: str) -> list:
    with open(path) as f:
        lines = [
            line.strip()
            for line in f.readlines()
            if line.strip() and "icon" not in line.lower()
        ]

    return lines


def clean_file(lines: list) -> list:
    clean_lines = []

    lines = [line for line in lines if "Mario Kart 8" not in line]
    for x in range(len(lines)):
        if not re.match(r".+\s+\d+", lines[x]):
            continue

        clean_lines.append(re.sub(r"(\S+)(\s{2,})", r"\1,", lines[x]))
    return clean_lines


def clean_drivers(lines: list) -> list:
    clean_lines = []

    for x in range(0, len(lines), 2):
        name = lines[x]
        stats = re.sub(r"(\w+)(.*)", r"\2", lines[x + 1])
        new_line = f"{name} {stats}"
        csv_line = re.sub(r"(\S+)(\s{2,})", r"\1,", new_line)
        clean_lines.append(csv_line)

    return clean_lines


def extract_stats(line: str) -> tuple:
    name, *stats = line.split(",")
    return name, ",".join(stats)


def merge_lines(lines: list) -> list:
    merged = dict()

    for line in lines[1:]:
        name, stats = extract_stats(line)

        if stats in merged:
            merged[stats].append(name)
        else:
            merged[stats] = [name]

    ids = []
    merged_lines = []
    current_id = 0
    for stats, names in merged.items():
        current_id += 1
        merged_lines.append(f"{current_id},{stats}")

        for name in names:
            ids.append(f"{name},{current_id}")

    merged_lines.sort()
    new_header = f"id, {','.join(lines[0].split(',')[1:])}"
    merged_lines.insert(0, new_header)

    return merged_lines, ids


def write_file(path: str, lines: list) -> None:
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def create_path(path: str, folder: str, suffix: str = None) -> str:
    folders = path.split("/")[:-1]
    filename = path.split("/")[-1]

    if suffix:
        return (
            f"{'/'.join(folders[:-1])}/{folder}/{filename.split('.')[0]}_{suffix}.csv"
        )

    return f"{'/'.join(folders[:-1])}/{folder}/{filename.split('.')[0]}.csv"


def clean(path: str) -> str:
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
    ids_path = create_path(path, "merged", "ids")
    write_file(ids_path, ids)

    return out_path


def main() -> None:
    dirty_path = "data/dirty/*.csv"
    for path in glob(dirty_path):
        clean(path)
        print(f"Cleaned {path}")


if __name__ == "__main__":
    main()
