from database import MK8DeluxeBuilds


def main():
    m = MK8DeluxeBuilds()
    m.sort_score = -1
    m.sort_std_dev = 1
    m.sort_miniturbo = -1

    m.limit = 30
    m.min_speed = 12
    m.min_acceleration = 12

    # print(m.available_filters)
    # print(m.available_sorts)

    for b in m.named_builds:
        print(b)


if __name__ == "__main__":
    main()
