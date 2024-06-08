from matplotlib import pyplot as plt

from car_arrival import run_car_arrival
from workshop import (
    run_simulation,
    AVERAGE_REPAIR_TIME,
    SIMULATION_TIME,
    MAINTENANCE_COST,
    NEW_AVERAGE_REPAIR_TIME,
    TOTAL_DAYS,
)

plot: bool


def plot_costs(initial_costs, new_costs):
    """
    Plot the costs of the initial and new system
    :param initial_costs: The costs of the initial system
    :param new_costs: The costs of the new system
    """

    fig, ax = plt.subplots()
    ax.plot(initial_costs, label="Sistema inicial")
    ax.plot(new_costs, label="Nuevo sistema")
    ax.set_xlabel("Número de Simulación")
    ax.set_ylabel("Costo")
    ax.legend()

    # save the image to img dir
    fig.savefig(f"img/costs.png")


def plot_system_cost(costs, plot_name: str, plot_label: str):

    fig, ax = plt.subplots()
    ax.plot(costs, label=plot_label)
    ax.set_xlabel("Numero de Simulacion")
    ax.set_ylabel("Costo")
    ax.legend()

    # save the image to img dir
    fig.savefig(f"img/{plot_name}.png")


def plot_stop_hours(initial_stop_hours, new_stop_hours):
    """
    Plot the total stop hours of the initial and new system
    :param initial_stop_hours: The total stop hours of the initial system
    :param new_stop_hours: The total stop hours of the new system
    :return:
    """

    fig, ax = plt.subplots()
    ax.plot(
        initial_stop_hours, label="Sistema inicial con media de reparación de 7 horas"
    )
    ax.plot(new_stop_hours, label="Nuevo sistema con media de reparación de 5 horas")
    ax.set_xlabel("Numero de simulación")
    ax.set_ylabel("Horas de parada")

    ax.legend()

    # save the image to img dir
    fig.savefig(f"img/stop_hours.png")


def plot_max_allowed_cost_increase(mean: float, results: list):
    """
    Plot the max allowed daily cost increase for the new system
    and the mean
    :param mean:  Average of the max allowed daily cost increase
    :param results: The results of the simulations
    """

    fig, ax = plt.subplots()
    ax.plot(results)
    ax.set_xlabel("Número de simulación")
    ax.set_ylabel("Incremento máximo de coste permisible")
    ax.axhline(
        y=mean,
        color="r",
        linestyle="-",
        label="Mean",
    )

    # save the image to img dir
    fig.savefig(f"img/max_allowed_cost_increase.png")


def run_sims(simulations: int):
    """
    Run simulation for a number of times and return the results
    :param simulations: The number of simulations to run
    """
    results = []
    initial_stop_hours = []
    new_stop_hours = []
    initial_total_costs = []
    new_total_costs = []
    new_total_costs_with_price_increase = []
    for i in range(simulations):

        car_arrivals_delay = run_car_arrival()

        initial_cost, logs = run_simulation(
            AVERAGE_REPAIR_TIME, SIMULATION_TIME, car_arrivals_delay
        )

        # Calculate the total stop hours
        stop_hours = sum(i["time_stopped"] for i in logs)
        initial_stop_hours.append(stop_hours)

        # Calculate the initial total cost
        total_initial_cost = initial_cost + TOTAL_DAYS * MAINTENANCE_COST
        initial_total_costs.append(total_initial_cost)

        new_cost, new_logs = run_simulation(
            NEW_AVERAGE_REPAIR_TIME, SIMULATION_TIME, car_arrivals_delay
        )

        # Calculate the new total stop hours
        stop_hours = sum(i["time_stopped"] for i in new_logs)
        new_stop_hours.append(stop_hours)

        # Calculate the max allowed daily cost increase
        max_allowed_daily_cost_increase = (total_initial_cost - new_cost) / TOTAL_DAYS

        # Calculate the new total cost
        new_total_cost = new_cost + TOTAL_DAYS * MAINTENANCE_COST
        new_total_costs.append(new_total_cost)

        # Calculate the new total cost with price increase
        new_total_cost_with_price_increase = (
            new_cost + TOTAL_DAYS * max_allowed_daily_cost_increase
        )
        new_total_costs_with_price_increase.append(new_total_cost_with_price_increase)

        results.append(max_allowed_daily_cost_increase - MAINTENANCE_COST)

    mean = sum(results) / simulations
    print(f"Average max allowed daily cost increase: {mean}")

    plot_costs(initial_total_costs, new_total_costs)
    plot_stop_hours(initial_stop_hours, new_stop_hours)
    plot_max_allowed_cost_increase(mean, results)
    plot_system_cost(
        new_total_costs_with_price_increase,
        "cost_with_price_increase",
        "Costo total con incremento de precio",
    )
    plot_system_cost(
        initial_total_costs, "initial_total_costs", "Costo total del sistema inicial"
    )


if __name__ == "__main__":
    run_sims(100)

# 132.6375390728007
