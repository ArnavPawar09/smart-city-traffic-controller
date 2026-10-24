import random
from scipy.optimize import linprog
from correlated_equilibrium import (
    generate_assignments,
    get_total_cost,
    build_incentive_constraints
)


def find_correlated_equilibrium(
    initial_a,
    initial_b,
    num_drivers
):
    assignments = generate_assignments(num_drivers)

    costs = [
        get_total_cost(assignment, initial_a, initial_b)
        for assignment in assignments
    ]

    constraints = build_incentive_constraints(
        assignments,
        initial_a,
        initial_b,
        num_drivers
    )

    result = linprog(
        c=costs,
        A_ub=constraints,
        b_ub=[0] * len(constraints),
        A_eq=[[1] * len(assignments)],
        b_eq=[1],
        bounds=[(0, 1)] * len(assignments),
        method="highs"
    )

    if not result.success:
        raise RuntimeError(
            "Could not find a correlated equilibrium: "
            + result.message
        )

    probabilities = result.x

    selected_index = random.choices(
        range(len(assignments)),
        weights=probabilities,
        k=1
    )[0]

    selected_assignment = assignments[selected_index]

    return (
        assignments,
        probabilities,
        selected_assignment,
        result.fun
    )
