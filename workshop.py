import itertools
import random

import simpy

AVERAGE_ARRIVAL_TIME = 8  # Average time it takes for a car to arrive in hours
AVERAGE_REPAIR_TIME = 7  # Average time it takes to repair a car in hours
NEW_AVERAGE_REPAIR_TIME = 5  # New  Average time it takes to repair a car in hours
TOTAL_DAYS = 365  # Total days in a year
SIMULATION_TIME = 24 * TOTAL_DAYS  # Total hours in a year
RANDOM_SEED = 42
MAINTENANCE_COST = 375  # Maintenance cost per hours in euros
STOP_COST = 25 / 24  # Stop cost in euros per hour

reparation_times = []


class Workshop:
    """
    A Workshop has a limited number of resources (``1`) to
    repair cars.

    Cars have to wait for the workshop to become available.

    """

    def __init__(self, env, average_repair_time):
        self.env = env
        self.average_repair_time = average_repair_time
        self.resource = simpy.Resource(env, capacity=1)

    def repair_car(self):
        """
        The repair process. It takes a ``car`` process and repairs it.
        :return:  The time it took to repair the car
        """

        repair_time = random.expovariate(1 / self.average_repair_time)
        yield self.env.timeout(repair_time)
        reparation_times.append(repair_time)
        return repair_time


def car(env, name, workshop, results):
    """
    The car process (each car has a ``name``) arrives at the workshop (`` workshop``) for repairs.
    It then starts the repair process and leaves the workshop once it's done.

    :param env:  The simpy environment
    :param name: The name of the car
    :param workshop: The workshop resource
    :param results:  A list to store the results
    """
    arrival_time = env.now

    with workshop.resource.request() as req:
        yield req
        start_repair_time = env.now
        _ = yield env.process(workshop.repair_car())
        end_repair_time = env.now
        time_stopped = end_repair_time - arrival_time
        results.append(
            {
                "name": name,
                "arrival_time": arrival_time,
                "start_repair_time": start_repair_time,
                "end_repair_time": end_repair_time,
                "time_stopped": time_stopped,
            }
        )


def setup(env, average_repair_time, results, car_arrivals_delay):
    """
    Create a workshop, and keep creating cars approx. every ``average_arrival_time`` hours.
    :param car_arrivals_delay: The list of car arrivals delay
    :param env: The simpy environment
    :param average_repair_time: The average time it takes to repair a car
    :param results: A list to store the results

    """
    workshop = Workshop(env, average_repair_time)

    car_count = itertools.count()
    idx = 0
    while True:
        yield env.timeout(car_arrivals_delay[idx])
        env.process(car(env, f"Car {next(car_count)}", workshop, results))
        idx += 1


def run_simulation(average_repair_time, simulation_time, car_arrivals_delay):
    """
    Run the simulation and return the total cost of every car stopped in the workshop
    :param average_repair_time: The average time it takes to repair a car
    :param simulation_time: The time to run the simulation
    :param car_arrivals_delay: The list of car arrivals delay

    """
    env = simpy.Environment()

    results = []

    env.process(setup(env, average_repair_time, results, car_arrivals_delay))
    env.run(until=simulation_time)

    total_stop_time = sum(i["time_stopped"] for i in results)
    total_stop_cost = total_stop_time * STOP_COST

    return total_stop_cost, results


# Set the random seed, uncomment this line to get the same results every time
random.seed(RANDOM_SEED)


"""
The initial cost is C_1*365 + x1 *p
The new cost is C_2*365 + x2 *p
The new cost must be less than the initial cost
C_1*365 + x1 *p > C_2*365 + x2 *p
(C1*365+x1*p -x2*p)/365 > C2

(CA - y*r)/365 > C2
"""
