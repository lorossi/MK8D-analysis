from database import Database, MK8Deluxe
from entities import Entity


def build() -> list[Entity]:
    m = MK8Deluxe()
    builds = []

    for d in m.driver:
        for v in m.vehicle:
            for t in m.tyre:
                for g in m.glider:
                    builds.append(d + v + t + g)

    return builds


def write_to_file(builds: list[Entity], path: str):
    with open(path, "w") as f:
        f.write(builds[0].csv_cols + "\n")
        f.writelines(b.csv + "\n" for b in builds)


def write_to_sql(builds: list[Entity], path: str):
    d = Database("MK8D")

    d.deleteTable("builds")
    d.createTable("builds", builds[0].cols)

    for b in builds:
        d.insert("builds", b.cols, b.rows)

    d.applyChanges()


def main():
    builds = build()
    write_to_file(builds, "builds.csv")
    write_to_sql(builds, "builds.sql")


if __name__ == "__main__":
    main()
