from database import MK8DeluxeBuilds


def main():
    m = MK8DeluxeBuilds()
    # use m.available_filters to get a list of available filters
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    m.min_ground_speed = 12
    m.min_acceleration = 12
    m.min_miniturbo = 5

    # use m.available_sort to get a list of available sort options
    # assign the value to the corresponding attribute of the MK8DeluxeBuilds object
    # -1 to sort descending, 1 to sort ascending
    m.sort_score = -1
    m.sort_score_dev = 1
    m.sort_miniturbo = -1

    # use m.limit to set the maximum number of results to return
    m.limit = 5

    for b in m.named_builds:
        print(b)


if __name__ == "__main__":
    main()
