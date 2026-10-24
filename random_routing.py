
import random

from traffic_model import total_travel_time


def simulate_random_routing(
    initial_a,
    initial_b,
    num_drivers,
    trials=1000
):
    costs = []
    assignments = []

    for _ in range(trials):
        assignment = tuple(
            random.choice(["A", "B"])
            for _ in range(num_drivers)
        )

        total_a = initial_a + assignment.count("A")
        total_b = initial_b + assignment.count("B")

        cost = total_travel_time(total_a, total_b)

        costs.append(cost)
        assignments.append(assignment)

    average_cost = sum(costs) / trials

    return (
        average_cost,
        min(costs),
        max(costs),
        costs,
        assignments
    )
