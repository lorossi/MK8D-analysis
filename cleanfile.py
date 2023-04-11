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

    lines = [line for line in lines if "from Mario Kart 8" not in line]
    for x in range(len(lines)):
        if not re.match(r".+\s+\d+", lines[x]):
            continue

        clean_lines.append(re.sub(r"(\S+)(\s{2,})", r"\1, ", lines[x]))
    return clean_lines


def clean_drivers(lines: list) -> list:
    clean_lines = []

    for x in range(0, len(lines), 2):
        name = lines[x]
        stats = re.sub(r"(\w+)(.*)", r"\2", lines[x + 1])
        new_line = f"{name} {stats}"
        csv_line = re.sub(r"(\S+)(\s{2,})", r"\1, ", new_line)
        clean_lines.append(csv_line)

    return clean_lines


def write_file(path: str, lines: list) -> None:
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def clean(path: str, out_path: str) -> str:
    lines = open_file(path)
    clean_lines = []

    # replace multiple spaces with a comma
    header = re.sub(r"(\S+)(\s{2,})", r"\1, ", lines[0])
    clean_lines.append(header)

    if "driver" in path.lower():
        clean_lines.extend(clean_drivers(lines[1:]))
    else:
        clean_lines.extend(clean_file(lines[1:]))

    filename = path.split("/")[-1]
    out_path = f"{out_path}/{filename.split('.')[0]}.csv"
    write_file(out_path, clean_lines)

    return out_path


def main() -> None:
    dirty_path = "data/dirty/*.csv"
    out_path = "data/clean"
    for path in glob(dirty_path):
        clean_path = clean(path, out_path)
        print(f"Cleaned {path} to {clean_path}")


if __name__ == "__main__":
    main()
