from __future__ import print_function
from simanneal import Annealer


import math
import random


def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) *
                     math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):
    """Test annealer with a travelling salesman problem"""
    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i - 1]][self.state[i]]
        return e


if __name__ == '__main__':

    # latitude and longitude for the twenty largest spanish cities (2010)
    cities = {
        'Madrid': (40.41669, -3.700346),
        'Barcelona': (41.38792, 2.169919),
        'Valencia': (39.47024, -0.3768049),
        'Sevilla': (37.38264, -5.996295),
        'Zaragoza': (41.65629, -0.8765379),
        'Malaga': (36.71965, -4.420019),
        'Murcia': (37.98344, -1.12989),
        'Palma': (39.56951, 2.649966),
        'Palmas de Gran Canaria (Las)': (28.12482, -15.43001),
        'Bilbao': (43.25696, -2.923441),
        'Alicante': (38.3452, -0.481006),
        'Cordoba': (37.88473, -4.779152),
        'Valladolid': (41.65295, -4.728388),
        'Vigo': (42.23136, -8.712447),
        'Gijon': (43.54526, -5.661926),
        'Hospitalet de Llobregat': (41.35958, 2.099704),
        'Coruna (A)': (43.37087, -8.395835),
        'Vitoria-Gasteiz': (42.84641, -2.667893),
        'Granada': (37.17649, -3.597929),
    }

    # initial_state = ['New York', 'Los Angeles', 'Boston', 'Houston']
    # tsp = TravellingSalesmanProblem(initial_state)

    # initial state, a randomly-ordered itinerary
    init_state = list(cities.keys())
    random.shuffle(init_state)

    # create a distance matrix
    distance_matrix = {}
    for ka, va in cities.items():
        distance_matrix[ka] = {}
        for kb, vb in cities.items():
            if kb == ka:
                distance_matrix[ka][kb] = 0.0
            else:
                distance_matrix[ka][kb] = distance(va, vb)

    tsp = TravellingSalesmanProblem(init_state, distance_matrix)
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    # Values for the parameters by default
    # Tmax = 25000.0
    # Tmin = 2.5
    # steps = 50000
    # updates = 100
    # Change the parameters to see the results
    # tsp.Tmax = 10000000  # Depende mas del numero de iteraciones
    # tsp.Tmin = 0.00000001  # A mayor, peor solucion
    # tsp.steps = 5  # Es mas importante que updates a la hora de encontrar
    # tsp.updates = 2  # la solucion optima
    state, e = tsp.anneal()

    while state[0] != 'Sevilla':
        state = state[1:] + state[:1]  # rotate Sevilla to start
    final_city = len(state) - 1
    while state[final_city] != 'Cordoba':
        state = state[final_city:] + state[:final_city]
    print("%i mile route:" % e)
    for city in state:
        print("\t", city)
