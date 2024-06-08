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


def plot_costs(initial_costs, new_costs, simulations: int):
    """
    Plot the costs of the initial and new system
    :param simulations:
    :param initial_costs: The costs of the initial system
    :param new_costs: The costs of the new system
    """

    fig, ax = plt.subplots()
    ax.plot(initial_costs, label="Initial system")
    ax.plot(new_costs, label="New system")
    ax.set_xlabel("Simulation")
    ax.set_ylabel("Cost")
    ax.legend()

    # save the image to img dir
    fig.savefig(f"img/{simulations}-costs.png")


def plot_stop_hours(initial_stop_hours, new_stop_hours, simulations: int):
    """
    Plot the total stop hours of the initial and new system
    :param simulations:
    :param initial_stop_hours: The total stop hours of the initial system
    :param new_stop_hours: The total stop hours of the new system
    :return:
    """

    fig, ax = plt.subplots()
    ax.plot(initial_stop_hours, label="Initial system")
    ax.plot(new_stop_hours, label="New system")
    ax.set_xlabel("Simulation")
    ax.set_ylabel("Stop hours")
    ax.legend()

    # save the image to img dir
    fig.savefig(f"img/{simulations}-stop_hours.png")


def plot_max_allowed_daily_cost_increase(mean: float, results: list, simulations: int):
    """
    Plot the max allowed daily cost increase for the new system
    and the mean
    :param simulations:
    :param mean:  Average of the max allowed daily cost increase
    :param results: The results of the simulations
    """

    fig, ax = plt.subplots()
    ax.plot(results)
    ax.set_xlabel("Simulation")
    ax.set_ylabel("Max allowed daily cost increase")
    ax.axhline(
        y=mean,
        color="r",
        linestyle="-",
        label="Mean",
    )

    # save the image to img dir
    fig.savefig(f"img/{simulations}-max_allowed_daily_cost_increase.png")


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

        # Calculate the new total cost
        new_total_cost = new_cost + TOTAL_DAYS * MAINTENANCE_COST
        new_total_costs.append(new_total_cost)

        # Calculate the max allowed daily cost increase
        max_allowed_daily_cost_increase = (total_initial_cost - new_cost) / TOTAL_DAYS

        results.append(max_allowed_daily_cost_increase - MAINTENANCE_COST)

    mean = sum(results) / simulations
    print(f"Average max allowed daily cost increase: {mean}")

    plot_costs(initial_total_costs, new_total_costs, simulations)
    plot_stop_hours(initial_stop_hours, new_stop_hours, simulations)
    plot_max_allowed_daily_cost_increase(mean, results, simulations)


if __name__ == "__main__":
    run_sims(100)
