from database import MK8Deluxe, SlimMK8Deluxe
from entities import Entity


def build(instance: object) -> list[Entity]:
    m = instance()
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
    to_run = [
        {"instance": MK8Deluxe, "destination": "builds.csv"},
        {"instance": SlimMK8Deluxe, "destination": "builds_slim.csv"},
    ]

    for execution in to_run:
        builds = build(execution["instance"])
        write_to_file(builds, execution["destination"])


if __name__ == "__main__":
    main()
