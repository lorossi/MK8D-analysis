"""This module contains the code to create the builds and save them \
    to the SQLite database."""
from modules.database import Database, MK8Deluxe
from modules.entities import Entity


def build() -> list[Entity]:
    """Create and return the builds.

    Returns:
        list[Entity]: list of builds
    """
    m = MK8Deluxe()
    builds = []

    for d in m.driver:
        for v in m.vehicle:
            for t in m.tyre:
                for g in m.glider:
                    builds.append(d + v + t + g)

    return builds


def write_to_file(builds: list[Entity], path: str):
    """Write the builds to a csv file.

    Args:
        builds (list[Entity]): The builds to write.
        path (str): The path to the file.
    """
    with open(path, "w") as f:
        f.write(builds[0].csv_cols + "\n")
        f.writelines(b.csv + "\n" for b in builds)


def write_to_sql(builds: list[Entity], path: str):
    """Write the builds to a SQL file.

    Args:
        builds (list[Entity]): The builds to write.
        path (str): The path to the file.
    """
    d = Database(path)

    # empty the old table and create a new one
    d.deleteTable("builds")

    cols = ["id"]
    cols.extend(builds[0].cols)

    types = ["INTEGER" for _ in range(len(cols))]
    d.createTable("builds", cols, types, cols[0])

    # insert the new builds
    for x, b in enumerate(builds):
        row = [x]
        row.extend(b.rows)
        d.insert("builds", cols, row)

    d.commitChanges()


def main():
    """Run the main function for the create builds script."""
    builds = build()
    write_to_file(builds, "builds.csv")
    write_to_sql(builds, "MK8D")


if __name__ == "__main__":
    main()
