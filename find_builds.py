from database import MK8DeluxeBuilds


def main():
    m = MK8DeluxeBuilds()
    for b in m.builds:
        print(b)


if __name__ == "__main__":
    main()
