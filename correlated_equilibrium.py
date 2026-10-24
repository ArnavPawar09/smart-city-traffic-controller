from itertools import product
from traffic_model import route_a_time, route_b_time


def generate_assignments(num_drivers):
    return list(product(["A", "B"], repeat=num_drivers))


def get_driver_cost(assignment, driver, initial_a, initial_b):
    total_a = initial_a + assignment.count("A")
    total_b = initial_b + assignment.count("B")

    if assignment[driver] == "A":
        return route_a_time(total_a)

    return route_b_time(total_b)


def get_total_cost(assignment, initial_a, initial_b):
    total_a = initial_a + assignment.count("A")
    total_b = initial_b + assignment.count("B")

    return (
        total_a * route_a_time(total_a)
        + total_b * route_b_time(total_b)
    )


def build_incentive_constraints(
    assignments,
    initial_a,
    initial_b,
    num_drivers
):
    constraints = []

    for driver in range(num_drivers):
        for recommended_route in ["A", "B"]:
            coefficients = []

            for assignment in assignments:
                if assignment[driver] == recommended_route:
                    current_cost = get_driver_cost(
                        assignment,
                        driver,
                        initial_a,
                        initial_b
                    )

                    changed_assignment = list(assignment)

                    if recommended_route == "A":
                        changed_assignment[driver] = "B"
                    else:
                        changed_assignment[driver] = "A"

                    changed_assignment = tuple(changed_assignment)

                    changed_cost = get_driver_cost(
                        changed_assignment,
                        driver,
                        initial_a,
                        initial_b
                    )

                    coefficients.append(current_cost - changed_cost)

                else:
                    coefficients.append(0)

            constraints.append(coefficients)

    return constraints
