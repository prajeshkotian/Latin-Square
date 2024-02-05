import random
import numpy as np
from random import choice
import statistics
import copy
from operator import attrgetter


# class to keep track of square matrix and cost
class Square:
    def __init__(self, cost, n):
        self.cost = 0
        self.square = np.zeros((n, n), int)
        self.fixed_value = np.zeros((n, n), int)


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

def cost_function(square, n):
    cost = 0
    for i in range(n):
        cost += (n-len(np.unique(square[:,i]))) + (n-len(np.unique(square[i,:])))
    return cost
def swap(square,x1,y1,x2,y2):
    temp = square[x1][y1]
    square[x1][y1] = square[x2][y2]
    square[x2][y2] = temp
    return square
def neighbour(square, n):
    neighbour = copy.deepcopy(square)
    # neighbour = swap(neighbour,random.randint(0,n-1),random.randint(0,n-1),random.randint(0,n-1),random.randint(0,n-1))
    cost = 0
    i = 0
    while (i < 3):
        x1 = random.randint(0, n - 1)
        y1 = random.randint(0, n - 1)
        x2 = random.randint(0, n - 1)
        y2 = random.randint(0, n - 1)

        if (neighbour[x1][y1] != neighbour[x2][y2]):

            neighbour = swap(neighbour, x1, y1, x2, y2)
            temp_cost = calculate_square_cost(neighbour, n)

            if i == 0:
                cost = temp_cost
            elif cost < temp_cost:
                neighbour = swap(neighbour, x1, y1, x2, y2)
            else:
                cost = temp_cost
            i += 1
    return neighbour, cost

def generate_state_permutation(state, n):
    neighbour_list = list([])
    min_state=copy.deepcopy(state)
    temp_state=neighbour(state.square, n)
    #neighbour_list.append(swap_state_value(temp_state, i1, j1, i2, j2, n))
    #min_state = min(neighbour_list, key=attrgetter('cost'))
    min_state.square = temp_state[0]
    min_state.cost = temp_state[1]
    return min_state


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
            return current_state.square
        # calling neighbour function
        min_state = generate_state_permutation(copy.copy(current_state), n)
        # check if new state needs to update the current state
        if current_state.cost > min_state.cost:
            current_state = copy.deepcopy(min_state)
            if best_state.cost > min_state.cost:
                best_state = copy.deepcopy(min_state)
        else:
            # acceptance probability check
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
            return best_state
        # elif current_state.cost == best_state.cost:
        # freezing_factor += 1
        else:
            freezing_factor = 0
        #print('Iteration number: ', iterations)

    # return best solution
    return best_state


def main():
    n = int(input("Enter the value of n:"))
    # populate possible option values to generate initial state
    array_values = list([])
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            array_values.append(j)
    #print('option values', array_values)
    # calculate initial temperature
    initial_temperature = 3.7
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

