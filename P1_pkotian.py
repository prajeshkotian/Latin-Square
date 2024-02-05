# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import numpy as np
import statistics
import copy
from operator import attrgetter


# class to keep track of square matrix and cost
class Square:
    def __init__(self, cost, n):
        self.cost = 0
        self.square = np.zeros((n, n), int)
        self.fixed_value = np.zeros((n, n), int)


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


# function to swap pairs of values to generate new neighbour
def swap_state_value(state, i1, j1, i2, j2, n):
    # print("swapping", i1, j1, " with ", i2, j2)
    temp = state.square[i1][j1]
    state.square[i1][j1] = state.square[i2][j2]
    state.square[i2][j2] = temp
    state.cost = calculate_square_cost(state.square, n)
    # print(state.square)
    # print(state.cost, 'cost of square')
    return state


# function to generate permutation of latin_square
def generate_state_permutation(state, n):
    neighbour_list = list([])
    for itr in range(0, 3):
        while True:
            i1 = random.randint(0, n - 1)
            j1 = random.randint(0, n - 1)
            i2 = random.randint(0, n - 1)
            j2 = random.randint(0, n - 1)
            # check to prevent swapping of same number or index values
            if state.square[i1][j1] != state.square[i2][j2]:
                break

        temp_state = copy.deepcopy(state)
        neighbour_list.append(swap_state_value(temp_state, i1, j1, i2, j2, n))
    min_state = min(neighbour_list, key=attrgetter('cost'))

    return min_state


# function to calculate cost of duplicates row and column wise in square(objective fn)
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


# objective function
def calculate_square_cost(square, n):
    row_cost = calculate_row_col_cost(square, n, 'row')
    col_cost = calculate_row_col_cost(square, n, 'col')
    return row_cost + col_cost


# to calculate initial temperature
def calculate_initial_temperature(array_values, n):
    initial_costs = list([])
    for itr in range(0, 200):
        initial_state = Square(0, n)
        initial_state.square = generate_latin_square(array_values.copy(), n).copy()
        initial_costs.append(calculate_square_cost(initial_state.square, n))
    # calculate standard deviation over 200 initial state costs
    initial_temperature = statistics.stdev(initial_costs)
    return initial_temperature


# annealing function
def simulated_annealing(initial_state, initial_temperature, n):
    freezing_factor = 0
    temperature_decrement_factor = 0.99
    current_state = copy.copy(initial_state)
    best_state = copy.copy(initial_state)
    iterations = 0
    temperature = initial_temperature
    while temperature > 0.0000000000000001:
        if freezing_factor >= n * 200:
            print('freezing point reached!!!')
            print('Iteration number: ', iterations)
            return best_state
        # calling neighbour function
        min_state = generate_state_permutation(copy.copy(current_state), n)
        # check if new state needs to update the current state
        if current_state.cost > min_state.cost:
            freezing_factor = 0
            current_state = copy.deepcopy(min_state)
            if best_state.cost > min_state.cost:
                best_state = copy.deepcopy(min_state)
        else:
            # acceptance probability check
            freezing_factor += 1
            random_number = random.random()
            scaled_cost = (current_state.cost - min_state.cost) / temperature
            acceptance_probability = np.exp(scaled_cost)
            if random_number < acceptance_probability:
                current_state = copy.deepcopy(min_state)

        temperature = temperature * temperature_decrement_factor
        #print('temperature is: ', temperature)
        iterations += 1
        if current_state.cost == 0:
            # Solution found
            print("final Solution Found!!!!:")
            print('Iteration number: ', iterations)
            return best_state
        #elif current_state.cost == best_state.cost:
           # freezing_factor += 1
        #else:
           # freezing_factor = 0

    print('Iteration number: ', iterations)
    # return best solution when final temp reached
    print('Final Temperature reached!!!!')
    return best_state


def main():
    n = int(input("Enter the value of n:"))
    if n % 2 != 0:
        print("Error n value is not even ")
        return
    if n not in range(4, 21):
        print("Error n value is not in desired range (4 - 20) ")
        return
    # populate possible option values to generate initial state
    array_values = list([])
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            array_values.append(j)

    # calculate initial temperature
    initial_temperature = round(calculate_initial_temperature(array_values, n), 2)
    #print('standard deviation', initial_temperature)

    # initialise square class object
    initial_state = Square(0, n)
    # generate initial state and cost
    initial_state.square = generate_latin_square(array_values, n).copy()
    initial_state.cost = calculate_square_cost(initial_state.square, n)

    final_solution = simulated_annealing(initial_state, initial_temperature, n, )
    print(final_solution.square)
    print('cost is:', final_solution.cost)


main()
