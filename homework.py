#!/usr/bin/env python3
import time
import sys
import math

from common import read_input, format_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def expanded_distance_squared(city1, city2, expansion_rate):
    """
    Calculate the distance after expanding in the vertical direction

    expansion_rate: Expansion rate in the vertical direction
    """
    return (city1[0] - city2[0]) ** 2 + ((city1[1] - city2[1])*expansion_rate) ** 2


def total_distance(tour, dist):
    """ Calculate the total distance of tour """
    total = 0
    for index in range(len(tour)):
        total += dist[tour[index-1]][tour[index]]
    return total


def greedy(cities, expansion_rate):

    N = len(cities)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = expanded_distance_squared(
                cities[i], cities[j], expansion_rate)

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour


def two_opt(tour, dist):
    """
    Swap two edges a-b,c-d to a-c,b-d if edges intersect

    dist: Array of distances between two cities
    """
    start_time = time.time()
    N = len(tour)
    while True:
        count = 0  # Number of times tour was changed
        for a_index in range(N-2):
            b_index = a_index+1
            for c_index in range(a_index+2, N):
                d_index = (c_index+1) % N
                A = tour[a_index]
                B = tour[b_index]
                C = tour[c_index]
                D = tour[d_index]
                if dist[A][B]+dist[C][D] > dist[A][C]+dist[B][D]:
                    tour[b_index:c_index +
                         1] = reversed(tour[b_index: c_index+1])
                    count += 1

        if count == 0:
            break
    end_time = time.time()
    print("Two_opt has finished. \nTime:", round(end_time-start_time, 1),
          "[s] Total distance: ", total_distance(tour, dist))
    return tour


def move_subsequence(tour, dist, subsequence_length):
    """
    Move subsequence E from between A and B to between C and D 
    if the total distance becomes shorter

    dist: Array of distances between two cities
    subsequence_length: The length of E
    """
    start_time = time.time()
    N = len(tour)
    while True:
        count = 0  # Number of times tour was changed
        for a_index in range(N-1):
            b_index = (a_index+subsequence_length+1) % N
            e_indexes = [(a_index+1+i) % N for i in range(subsequence_length)]
            for c_index in range(N-1):
                d_index = (c_index+1) % N

                # When C,D sre not included in e_indexes
                if d_index not in e_indexes and d_index != b_index:
                    A = tour[a_index]
                    B = tour[b_index]
                    C = tour[c_index]
                    D = tour[d_index]
                    E = [tour[index] for index in e_indexes]
                    if dist[A][E[0]]+dist[E[-1]][B]+dist[C][D] > dist[A][B]+dist[C][E[-1]]+dist[E[0]][D]:
                        # Replace the cities of E with -1. The indexes of C and D are not changed
                        for i in range(subsequence_length):
                            tour[(a_index+1+i) % N] = -1
                        # Reverse E and put E between C and D
                        for i in range(subsequence_length):
                            tour.insert(d_index, E[i])
                        # Remove the cities of E by removing -1
                        for i in range(subsequence_length):
                            tour = [city for city in tour if city != -1]
                        count += 1
        if count == 0:
            break
    end_time = time.time()
    print("Move_sequence (Length=", subsequence_length, ")has finished.", "\nTime:", round(end_time-start_time, 1),
          "[s] Total distance:", total_distance(tour, dist))
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 2
    cities = read_input(sys.argv[1])
    N = len(cities)

    dist = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    print("Distance array was created.")
    if N == 5 or N == 8 or N == 16:
        expansion_rate = 1.0
        tour = greedy(cities, expansion_rate)
        tour = two_opt(tour, dist)
        tour = move_subsequence(tour, dist, 1)
    elif N == 64:
        expansion_rate = 1.5
        tour = greedy(cities, expansion_rate)
        tour = move_subsequence(tour, dist, 5)
        for _ in range(2):
            tour = two_opt(tour, dist)
            tour = move_subsequence(tour, dist, 4)
            tour = move_subsequence(tour, dist, 3)
            tour = move_subsequence(tour, dist, 2)
            tour = move_subsequence(tour, dist, 1)
    elif N == 128:
        expansion_rate = 1.15
        tour = greedy(cities, expansion_rate)
        tour = move_subsequence(tour, dist, 4)
        tour = two_opt(tour, dist)
        tour = move_subsequence(tour, dist, 3)
        tour = move_subsequence(tour, dist, 2)
        tour = move_subsequence(tour, dist, 1)
    elif N == 512:
        expansion_rate = 1.37
        tour = greedy(cities, expansion_rate)
        for _ in range(2):
            tour = two_opt(tour, dist)
            tour = move_subsequence(tour, dist, 5)
            tour = move_subsequence(tour, dist, 4)
            tour = move_subsequence(tour, dist, 3)
            tour = move_subsequence(tour, dist, 2)
            tour = move_subsequence(tour, dist, 1)
    elif N == 2048:
        expansion_rate = 1.15
        tour = greedy(cities, expansion_rate)
        for _ in range(4):
            tour = two_opt(tour, dist)
            tour = move_subsequence(tour, dist, 7)
            tour = move_subsequence(tour, dist, 6)
            tour = move_subsequence(tour, dist, 5)
            tour = move_subsequence(tour, dist, 4)
            tour = move_subsequence(tour, dist, 3)
            tour = move_subsequence(tour, dist, 2)
            tour = move_subsequence(tour, dist, 1)


with open(sys.argv[2], mode='w') as f:
    f.write(format_tour(tour))
