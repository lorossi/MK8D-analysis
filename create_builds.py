from database import MK8Deluxe
from entities import Entity


def build() -> list[Entity]:
    m = MK8Deluxe()
    builds = []

    for d in m.drivers:
        for v in m.vehicles:
            for t in m.tyres:
                for g in m.gliders:
                    builds.append(d + v + t + g)

    return builds


def write_to_file(builds: list[Entity], path: str):
    with open(path, "w") as f:
        f.write(builds[0].getCSVCols() + "\n")
        f.writelines(b.toCSV() + "\n" for b in builds)


def main():
    builds = build()
    write_to_file(builds, "builds.csv")


if __name__ == "__main__":
    main()
