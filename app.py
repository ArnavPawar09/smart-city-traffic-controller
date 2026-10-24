
from flask import Flask, render_template, request

from controller import find_correlated_equilibrium
from correlated_equilibrium import get_total_cost
from random_routing import simulate_random_routing
from traffic_model import route_a_time, route_b_time

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    initial_a = 6
    initial_b = 2
    num_drivers = 4
    trials = 1000

    if request.method == "POST":
        initial_a = int(request.form["initial_a"])
        initial_b = int(request.form["initial_b"])
        num_drivers = int(request.form["num_drivers"])
        trials = int(request.form["trials"])

        if initial_a < 0 or initial_b < 0:
            return render_template(
                "index.html",
                error="Existing traffic cannot be negative.",
                initial_a=initial_a,
                initial_b=initial_b,
                num_drivers=num_drivers,
                trials=trials
            )

        try:
            # Correlated-equilibrium controller
            _, _, selected, expected_cost = (
                find_correlated_equilibrium(
                    initial_a,
                    initial_b,
                    num_drivers
                )
            )

            new_a = selected.count("A")
            new_b = selected.count("B")

            final_a = initial_a + new_a
            final_b = initial_b + new_b

            selected_cost = get_total_cost(
                selected,
                initial_a,
                initial_b
            )

            # Random route selection baseline
            (
                random_average,
                random_minimum,
                random_maximum,
                random_costs,
                random_assignments
            ) = simulate_random_routing(
                initial_a,
                initial_b,
                num_drivers,
                trials
            )

            reduction = (
                (random_average - expected_cost)
                / random_average * 100
                if random_average > 0 else 0
            )

            result = {
                "selected": selected,
                "expected_cost": expected_cost,
                "selected_cost": selected_cost,
                "new_a": new_a,
                "new_b": new_b,
                "final_a": final_a,
                "final_b": final_b,
                "route_a_time": route_a_time(final_a),
                "route_b_time": route_b_time(final_b),
                "random_average": random_average,
                "random_minimum": random_minimum,
                "random_maximum": random_maximum,
                "reduction": reduction,
                "trials": trials
            }

        except Exception as e:
            return render_template(
                "index.html",
                error=str(e),
                initial_a=initial_a,
                initial_b=initial_b,
                num_drivers=num_drivers,
                trials=trials
            )

    return render_template(
        "index.html",
        result=result,
        initial_a=initial_a,
        initial_b=initial_b,
        num_drivers=num_drivers,
        trials=trials
    )


if __name__ == "__main__":
    app.run(debug=True)
