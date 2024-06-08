import random

import simpy

from workshop import AVERAGE_ARRIVAL_TIME, SIMULATION_TIME


def simulate_car_arrival(env, car_arrival_de):
    """
    Simulates car arrival at a rate of 3 every day for a year independent of the workshop
    :param env: The simpy environment
    :param car_arrival_de    : The list to store the car arrivals delay
    """

    while True:
        arrival_time = random.expovariate(1 / AVERAGE_ARRIVAL_TIME)
        yield env.timeout(arrival_time)
        car_arrival_de.append(arrival_time)


def run_car_arrival():
    env = simpy.Environment()
    car_arrival_delay = []
    env.process(simulate_car_arrival(env, car_arrival_delay))
    env.run(until=SIMULATION_TIME)

    # add a dummy value that never gets processed
    car_arrival_delay.append(1000)

    return car_arrival_delay
