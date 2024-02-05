# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import numpy as np
import math
from random import choice
import statistics
import copy
import operator
from operator import attrgetter


class Square:
    def __init__(self, cost, n):
        self.cost = 0
        self.square = np.zeros((n, n), int)
        self.fixed_value = np.zeros((n, n), int)


def print_square(square, lim):
    for i1 in range(0, lim):
        print(square[i1])
    #    for j1 in range(0, lim):

    # print("\n")


# function to generate initial state
def generate_latin_square(array, n):
    new_array = array
    new_list = list([])
    latin_square = np.zeros((n, n), int)
    for j in range(0, n):
        for i in range(0, n):
            random_number = random.choice(new_array)
            new_array.remove(random_number)
            new_list.append(random_number)
        latin_square[j] = new_list
        new_list = []
    # print(latin_square,'latin square')
    return latin_square


def swap_state_value(state, i1, j1, i2, j2, n):
    # print("swapping", i1, j1, " with ", i2, j2)
    temp = state.square[i1][j1]
    state.square[i1][j1] = state.square[i2][j2]
    state.square[i2][j2] = temp
    state.cost = calculate_square_cost(state.square, n)
    state.fixed_value[i1][j1] = 1
    state.fixed_value[i2][j2] = 1
    # print(state.square)
    print(state.cost, 'cost of square')
    return state


# function to generate permutation of latin_square
def generate_state_permutation(state, n):
    print('called generate state function!!!')
    neighbour_list = list([])
    min_state = copy.deepcopy(state)
    # print('Fixed positions are', state.fixed_value)
    # for itr in range(0, 3):
    while True:
        i1 = random.randint(0, n - 1)
        j1 = random.randint(0, n - 1)
        i2 = random.randint(0, n - 1)
        j2 = random.randint(0, n - 1)
        # if i1 != i2 and j1 != j2 and state.fixed_value[i1][j1] != 1 and state.fixed_value[i1][j1] != 1 and state.square[i1][j1] != state.square[i2][j2]:
        # break
        if (i1 != i2 or j1 != j2) and state.square[i1][j1] != state.square[i2][j2]:
            break
    temp_state = copy.deepcopy(state)
    # neighbour_list.append(swap_state_value(temp_state, i1, j1, i2, j2, n))
    temp_state = swap_state_value(temp_state, i1, j1, i2, j2, n)
    # if temp_state.cost < min_state.cost:
    # min_state = copy.deepcopy(temp_state)
    # min_state = min(neighbour_list, key=attrgetter('cost'))
    # print(min_state.square, 'min value square')
    return temp_state


# function to calculate cost of duplicates row and column wise in square
def calculate_row_col_cost(square, n, type):
    if type == 'row':
        total_row_cost = 0
        for i in range(0, n):
            temp_row = square[i]
            value_count = np.zeros(n + 1, int)
            for ele in temp_row:
                value_count[ele] += 1
            # print(value_count, 'value count')
            for j in range(1, n + 1):
                # print(value_count[j], ' ')
                if value_count[j] >= 2:
                    total_row_cost += value_count[j] - 1
        # print(total_row_cost, 'final rows cost')
        return total_row_cost
    if type == 'col':
        num_columns = len(square[0])
        column_counts = [0] * num_columns
        for col in range(num_columns):
            column_values = []
            for row in square:
                if row[col] in column_values:
                    column_counts[col] += 1
                else:
                    column_values.append(row[col])
        total_col_cost = 0
        for ele in range(0, len(column_counts)):
            total_col_cost = total_col_cost + column_counts[ele]
        return total_col_cost


def calculate_square_cost(square, n):
    row_cost = calculate_row_col_cost(square, n, 'row')
    col_cost = calculate_row_col_cost(square, n, 'col')
    return row_cost + col_cost


def calculate_initial_temperature(array_values, n):
    initial_costs = list([])
    for itr in range(0, 200):
        initial_state = Square(0, n)
        initial_state.square = generate_latin_square(array_values.copy(), n).copy()
        initial_costs.append(calculate_square_cost(initial_state.square, n))
    #initial_temperature = statistics.stdev(initial_costs)
    initial_temperature = max(initial_costs)
    return initial_temperature


def main():
    n = int(input("Enter the value of n:"))
    if n % 2 != 0:
        print("Error n value is not even ")
        return
    if n not in range(4, 20):
        print("Error n value is not in desired range (4 - 20) ")
        return
    array_values = list([])
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            array_values.append(j)
    print('option values', array_values)
    initial_temperature = round(calculate_initial_temperature(array_values, n), 2)
    print('standard deviation', initial_temperature)
    initial_state = Square(0, n)
    initial_state.square = generate_latin_square(array_values, n).copy()
    initial_state.cost = calculate_square_cost(initial_state.square, n)
    # print(initial_state.square, 'initial state')
    freezing_factor = 0
    temperature_decrement_factor = 0.99
    current_state = copy.copy(initial_state)
    best_solution = copy.copy(initial_state)
    print(current_state.square, 'current state')
    print('current state cost is:', current_state.cost)
    iterations = 0
    temperature = initial_temperature
    while temperature > 0.0000000000000000001:

        for i in range(0, 3):
            min_state = generate_state_permutation(copy.copy(current_state), n)
            print(min_state.square, "min state square value")
            print(min_state.cost, 'min state cost')
            # if current_state.cost == 0:
            # print("final Solution Found!!!!:", current_state.square)
            # return
            if current_state.cost > min_state.cost:
                print('Setting min state to current state!!!!')
                current_state = copy.deepcopy(min_state)
                #freezing_factor = 0
                if min_state.cost < best_solution.cost:
                    best_solution = copy.deepcopy(min_state)
            else:
                # acceptance probability
                random_number = random.random()
                scaled_cost = (-(min_state.cost - current_state.cost) / temperature)
                acceptance_probability = np.exp(scaled_cost)
                print('acceptance probability is:', acceptance_probability)
                if random_number < acceptance_probability:
                    print('acceptance probability accepted!!!!!')
                    current_state = copy.deepcopy(min_state)
                    freezing_factor = 0
                else:
                    print('incrementing freezing factor')
                    # freezing_factor += 1
                    print('freezing factor is:', freezing_factor)

            temperature = temperature * temperature_decrement_factor
            print('temperature is: ', temperature)
            iterations += 1
            print('Iteration number: ', iterations)
            # if current_state.cost < best_solution.cost:
                # best_solution = copy.deepcopy(current_state)
            if current_state.cost == 0:
                print("final Solution Found!!!!:", current_state.square)
                return
            if freezing_factor >= 1000:
                print('freezing point reached!!!', best_solution.square)
                print('cost is :', best_solution.cost)
                return current_state.square
            # if current_state.cost == best_solution.cost:
                #freezing_factor += 1
        if current_state.cost > best_solution.cost:
            current_state = copy.copy(best_solution)
    print('Best Solution is:', best_solution.square)
    print('best Solution cost is: ', best_solution.cost)


main()
