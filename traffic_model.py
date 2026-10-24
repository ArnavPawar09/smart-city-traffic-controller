def route_a_time(n_a):
    if n_a == 0:
        return 0

    extra_cars = n_a - 1
    return 8 + 2 * extra_cars + 1.5 * (extra_cars ** 2)


def route_b_time(n_b):
    if n_b == 0:
        return 0

    extra_cars = n_b - 1
    return 11 + extra_cars + 0.5 * (extra_cars ** 2)


def total_travel_time(n_a, n_b):
    time_a = route_a_time(n_a)
    time_b = route_b_time(n_b)

    return n_a * time_a + n_b * time_b
