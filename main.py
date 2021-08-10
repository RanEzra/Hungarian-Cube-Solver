# inspired by Prof. moshe sipper, BGU
from random import randint, random
from copy import deepcopy
RUNS = 1
POP_SIZE = 100  # population size
INDIVIDUAL_SIZE = 150 # represents the amount of the allowed actions
GENERATIONS = 100 # maximal number of generations to run evolution
TOURNAMENT_SIZE = 10  # size of tournament for tournament selection
MUTATION_PROB = 0.1 # the probability to make a mutation on each cell
RANDOMIZATION_LEVEL = 20
RANDOM_SEARCH_COMPARE = False
FULL_RANDOM = True
CUBE_DETAILS = True

#--------------class Cube-------------
class Cube:
    def __init__(self):
        self.close = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.far = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.left = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        self.right = [3, 3, 3, 3, 3, 3, 3, 3, 3]
        self.bottom = [4, 4, 4, 4, 4, 4, 4, 4, 4]
        self.up = [5, 5, 5, 5, 5, 5 ,5, 5, 5]

    def randomize_cube(self):
        R_OPTIONS = [up_1, up_2, bottom_1, bottom_2, right_1, right_2, left_1, left_2, close_1, close_2, far_1, far_2]
        moves = [8,1,2,10,1,1]
        for i in range (RANDOMIZATION_LEVEL):
            if (FULL_RANDOM == True):
                j = randint(0,len(R_OPTIONS)-1)
            else:
                j = moves[i]
            self = R_OPTIONS[j](self)

    def print_cube(self):
        print("close: ",self.close)
        print("far :", self.far)
        print("left: ", self.left)
        print("right: ",self.right)
        print("bottom ",self.bottom)
        print("up: ", self.up)

#--------Helpers----------------------
def shift_clockwise(arr):
    out = []
    out.append(arr[6])
    out.append(arr[3])
    out.append(arr[0])
    out.append(arr[7])
    out.append(arr[4])
    out.append(arr[1])
    out.append(arr[8])
    out.append(arr[5])
    out.append(arr[2])
    return out

def shift_counterclockwise(arr):
    out = []
    out.append(arr[2])
    out.append(arr[5])
    out.append(arr[8])
    out.append(arr[1])
    out.append(arr[4])
    out.append(arr[7])
    out.append(arr[0])
    out.append(arr[3])
    out.append(arr[6])
    return out

def left_to_close(c):
        c.up = shift_counterclockwise(c.up)
        c.bottom = shift_counterclockwise(c.bottom)
        t_close = c.left
        t_right = c.close
        t_far = c.right
        t_left = c.far
        c.close = t_close
        c.right = t_right
        c.far = t_far
        c.left = t_left
        return c

def right_to_close(c):
        c.up = shift_clockwise(c.up)
        c.bottom = shift_clockwise(c.bottom)
        t_close = c.right
        t_left = c.close
        t_far = c.left
        t_right = c.far
        c.close = t_close
        c.right = t_right
        c.far = t_far
        c.left = t_left
        return c

def up_to_close(c):
        t_close = c.up
        t_far = c.bottom
        t_bottom = c.close
        t_up = c.far
        c.close = t_close
        c.far = t_far
        c.bottom = t_bottom
        c.up = t_up
        c.left = shift_clockwise(c.left)
        c.right = shift_clockwise(c.right)
        return c

def bottom_to_close(c):
        t_close = c.bottom
        t_far = c.up
        t_bottom = c.far
        t_up = c.close
        c.close = t_close
        c.far = t_far
        c.bottom = t_bottom
        c.up = t_up
        c.left = shift_counterclockwise(c.left)
        c.right = shift_counterclockwise(c.right)
        return c

#--------Cube Fucnctions--------------
def up_1(c):
        c.up = shift_clockwise(c.up)
        t_close = []
        t_right = []
        t_far = []
        t_left = []
        for i in range (3):
            t_close.append(c.close[i])
            t_right.append(c.right[i])
            t_far.append(c.far[i])
            t_left.append(c.left[i])
        for i in range (3):
            c.close[i] = t_right[i]
            c.left[i] = t_close[i]
            c.far[i] = t_left[i]
            c.right[i] = t_far[i]
        return c

def up_2(c):
        c.up = shift_counterclockwise(c.up)
        t_close = []
        t_right = []
        t_far = []
        t_left = []
        for i in range (3):
            t_close.append(c.close[i])
            t_right.append(c.right[i])
            t_far.append(c.far[i])
            t_left.append(c.left[i])
        for i in range (3):
            c.close[i] = t_left[i]
            c.right[i] = t_close[i]
            c.far[i] = t_right[i]
            c.left[i] = t_far[i]
        return c

def bottom_1(c):
        c.bottom = shift_clockwise(c.bottom)
        t_close = []
        t_right = []
        t_far = []
        t_left = []
        for i in range (6,9):
            t_close.append(c.close[i])
            t_right.append(c.right[i])
            t_far.append(c.far[i])
            t_left.append(c.left[i])
        for i in range (6,9):
            c.close[i] = t_left[i-6]
            c.left[i] = t_far[i-6]
            c.far[i] = t_right[i-6]
            c.right[i] = t_close[i-6]
        return c

def bottom_2(c):
        c.bottom = shift_counterclockwise(c.bottom)
        t_close = []
        t_right = []
        t_far = []
        t_left = []
        for i in range (6,9):
            t_close.append(c.close[i])
            t_right.append(c.right[i])
            t_far.append(c.far[i])
            t_left.append(c.left[i])
        for i in range (6,9):
            c.close[i] = t_right[i-6]
            c.right[i] = t_far[i-6]
            c.far[i] = t_left[i-6]
            c.left[i] = t_close[i-6]
        return c

def left_1(c):
    c.left = shift_counterclockwise(c.left)
    rep_c = deepcopy(c)
    for i in range(3):
        c.close[i*3] = rep_c.bottom[i*3]
        c.up[i*3] = rep_c.close[i*3]
    c.far[2] = rep_c.up[6]
    c.far[5] = rep_c.up[3]
    c.far[8] = rep_c.up[0]
    c.bottom[0] = rep_c.far[8]
    c.bottom[3] = rep_c.far[5]
    c.bottom[6] = rep_c.far[2]
    return c

def left_2(c):
    c.left = shift_clockwise(c.left)
    rep_c = deepcopy(c)
    for i in range(3):
        c.close[i*3] = rep_c.up[i*3]
        c.bottom[i*3] = rep_c.close[i*3]
    c.far[2] = rep_c.bottom[6]
    c.far[5] = rep_c.bottom[3]
    c.far[8] = rep_c.bottom[0]
    c.up[0] = rep_c.far[8]
    c.up[3] = rep_c.far[5]
    c.up[6] = rep_c.far[2]
    return c

def right_1(c):
    c.left = shift_clockwise(c.left)
    rep_c = deepcopy(c)
    for i in range(3):
        c.close[i*3+2] = rep_c.bottom[i*3+2]
        c.up[i*3+2] = rep_c.close[i*3+2]
    c.far[0] = rep_c.up[8]
    c.far[3] = rep_c.up[5]
    c.far[6] = rep_c.up[2]
    c.bottom[2] = rep_c.far[6]
    c.bottom[5] = rep_c.far[3]
    c.bottom[8] = rep_c.far[0]
    return c

def right_2(c):
    c.left = shift_counterclockwise(c.left)
    rep_c = deepcopy(c)
    for i in range(3):
        c.close[i*3+2] = rep_c.up[i*3+2]
        c.bottom[i*3+2] = rep_c.close[i*3+2]
    c.far[0] = rep_c.bottom[8]
    c.far[3] = rep_c.bottom[5]
    c.far[6] = rep_c.bottom[2]
    c.up[2] = rep_c.far[6]
    c.up[5] = rep_c.far[3]
    c.up[8] = rep_c.far[0]
    return c

def far_1(c):
    c.far = shift_clockwise(c.far)
    rep_c = deepcopy(c)
    c.up[0] = rep_c.right[2]
    c.up[1] = rep_c.right[5]
    c.up[2] = rep_c.right[8]

    c.left[0] = rep_c.up[2]
    c.left[3] = rep_c.up[1]
    c.left[6] = rep_c.up[0]

    c.right[2] = rep_c.bottom[8]
    c.right[5] = rep_c.bottom[7]
    c.right[8] = rep_c.bottom[6]

    c.bottom[6] = rep_c.left[0]
    c.bottom[7] = rep_c.left[3]
    c.bottom[8] = rep_c.left[6]
    return c

def far_2(c):
    c.far = shift_counterclockwise(c.far)
    rep_c = deepcopy(c)

    c.right[2] = rep_c.up[0]
    c.right[5] = rep_c.up[1]
    c.right[8] = rep_c.up[2]

    c.up[0] = rep_c.left[6]
    c.up[1] = rep_c.left[3]
    c.up[2] = rep_c.left[0]

    c.left[0] = rep_c.bottom[6]
    c.left[3] = rep_c.bottom[7]
    c.left[6] = rep_c.bottom[8]

    c.bottom[6] = rep_c.right[8]
    c.bottom[7] = rep_c.right[5]
    c.bottom[8] = rep_c.right[2]

    return c

def close_1(c):
    c.close = shift_clockwise(c.close)
    rep_c = deepcopy(c)
    c.up[6] = rep_c.left[8]
    c.up[7] = rep_c.left[5]
    c.up[8] = rep_c.left[2]

    c.left[2] = rep_c.bottom[0]
    c.left[5] = rep_c.bottom[1]
    c.left[8] = rep_c.bottom[2]

    c.right[0] = rep_c.up[6]
    c.right[3] = rep_c.up[7]
    c.right[6] = rep_c.up[8]

    c.bottom[0] = rep_c.right[6]
    c.bottom[1] = rep_c.right[3]
    c.bottom[2] = rep_c.right[0]
    return c

def close_2(c):
    c.close = shift_counterclockwise(c.close)
    rep_c = deepcopy(c)
    c.up[6] = rep_c.right[0]
    c.up[7] = rep_c.right[3]
    c.up[8] = rep_c.right[6]

    c.left[2] = rep_c.up[8]
    c.left[5] = rep_c.up[7]
    c.left[8] = rep_c.up[6]

    c.right[0] = rep_c.bottom[2]
    c.right[3] = rep_c.bottom[1]
    c.right[6] = rep_c.bottom[0]

    c.bottom[0] = rep_c.left[2]
    c.bottom[1] = rep_c.left[5]
    c.bottom[2] = rep_c.left[8]
    return c

def do_nothing(c):
    return c

#---------super moves----------#
def s1_1(c): # F' U L' U'
    c = close_2(c)
    c = up_1(c)
    c = left_2(c)
    c = up_2(c)
    return c

def s2_1(c): #R' D-2 R D
    c = right_2(c)
    c = bottom_2(c)
    c = bottom_2(c)
    c = right_1(c)
    c = bottom_1(c)
    return c

def s2_2(c): #L D2 L' D'
    c = left_1(c)
    c = bottom_1(c)
    c = bottom_1(c)
    c = left_2(c)
    c = bottom_2(c)
    return c

def s2_3(c): # R' D' R D
    c = right_2(c)
    c = bottom_2(c)
    c = right_1(c)
    c = bottom_1(c)
    return c

def s2_4(c): #  L D L' D'
    c = left_1(c)
    c = bottom_1(c)
    c = left_2(c)
    c = bottom_2(c)
    return c

def s3_1(c): # U R U' R' U' F' U F
    c = up_1(c)
    c = right_1(c)
    c = up_2(c)
    c = right_2(c)
    c = up_2(c)
    c = close_2(c)
    c = up_1(c)
    c = close_1(c)
    return c

def s3_2(c): # U' L' U L U F U' F'
    c = up_2(c)
    c = left_2(c)
    c = up_1(c)
    c = left_1(c)
    c = up_1(c)
    c = close_1(c)
    c = up_2(c)
    c = close_2(c)
    return c

def s4_1(c): # B U L U' L' B'    B L U L' U' B'
    c = bottom_1(c)
    c = up_1(c)
    c = left_1(c)
    c = up_2(c)
    c = left_2(c)
    c = bottom_2(c)
    c = bottom_1(c)
    c = left_1(c)
    c = up_1(c)
    c = left_2(c)
    c = up_2(c)
    c = bottom_2(c)
    return c

def s4_2(c): # B L U L' U' B'
    c = bottom_1(c)
    c = left_1(c)
    c = up_1(c)
    c = left_2(c)
    c = up_2(c)
    c = bottom_2(c)
    return c

def s4_3(c): # B U L U' L' B'
    c = bottom_1(c)
    c = up_1(c)
    c = left_1(c)
    c = up_2(c)
    c = left_2(c)
    c = bottom_2(c)
    return c

def s5_1(c) : #R U R' U R U2 R'
    c = right_1(c)
    c = up_1(c)
    c = right_2(c)
    c = up_1(c)
    c = right_1(c)
    c = up_1(c)
    c = up_1(c)
    c = right_2(c)
    return c

def s6_1(c): # U R U' L' U R' U' L
    c = up_1(c)
    c = right_1(c)
    c = up_2(c)
    c = left_2(c)
    c = up_1(c)
    c = right_2(c)
    c = up_2(c)
    c = left_1(c)
    return c

def s7_1(c): # R' D R F D     F' U F D'     F' R' D' R U'
    c = right_2(c)
    c = bottom_1(c)
    c = right_1(c)
    c = close_1(c)
    c = bottom_1(c)
    c = close_2(c)
    c = up_1(c)
    c = close_1(c)
    c = bottom_2(c)
    c = close_2(c)
    c = right_2(c)
    c = bottom_2(c)
    c = right_1(c)
    c = up_2(c)
    return c


L1_OPTIONS = [up_1,up_2,left_to_close,right_to_close,up_to_close,bottom_to_close]
L2_OPTIONS = [up_1, up_2, bottom_1, bottom_2, right_1, right_2, left_1, left_2, close_1, close_2, far_1, far_2]
L3_OPTIONS = [s1_1,s2_1,s2_2,s2_3,s2_4,s3_1,s3_2,s4_1,s4_2,s4_3,s5_1,s6_1,s7_1]
OPTIONS = L2_OPTIONS

#-------------Evolutionaty Fuctions-----------------
def init_population():
    return [[randint(0, len(OPTIONS) - 1) for j in range(INDIVIDUAL_SIZE)] for i in range(POP_SIZE)]

def fitness(c, moves):
    best = -1;
    test_c = deepcopy(c)
    for i in range (len(moves)):
        test_c = (OPTIONS[moves[i]](test_c))
        hits = weighted_count(test_c)
        if (hits > best):
            best = hits
    return best

def selection(population,fitnesses):
    tournament = [randint(0, POP_SIZE-1) for i in range(TOURNAMENT_SIZE)] # select tournament contenders
    tournament_fitnesses = [fitnesses[tournament[i]] for i in range(TOURNAMENT_SIZE)]
    return deepcopy(population[tournament[tournament_fitnesses.index(max(tournament_fitnesses))]])

def mutation(c, child):
    test_c = deepcopy(c)
    best = - 1
    best_ind = - 1
    for i in range (INDIVIDUAL_SIZE):
        test_c = (OPTIONS[child[i]](test_c))
        hits = count(test_c)
        if (hits>best):
            best = hits
            best_ind = i
    for i in range (0,INDIVIDUAL_SIZE):
        if i <=  best_ind: #
            if random() < (MUTATION_PROB / 10 ):
                child[i] = randint(0,len(OPTIONS)-1)
        else:
            if random () < MUTATION_PROB:
                child[i] = randint(0, len(OPTIONS)-1)
    return child

def crossover(parent1, parent2):
    son = []
    cut = randint(1,INDIVIDUAL_SIZE-1)
    for i in range (cut):
        son.append(parent1[i])
    for i in range (cut,INDIVIDUAL_SIZE):
        son.append(parent2[i])
    return son

def usual_fitness(c, moves):
    test_c = deepcopy(c)
    for i in range (len(moves)):
        test_c = (OPTIONS[moves[i]](test_c))
    return count(test_c)

def usual_mutation(child):
    for i in range (INDIVIDUAL_SIZE):
            if (i % 10 == 0):
                child[i] = randint(0,len(OPTIONS)-1)
    return child

#-------------Others---------------------------------
def count(test_c):
    out = 0
    for i in range(9):
        if test_c.up[i] == test_c.up[4]:
            out = out + 1
        if test_c.bottom[i] == test_c.bottom[4]:
            out = out + 1
        if test_c.left[i] == test_c.left[4]:
            out = out + 1
        if test_c.right[i] == test_c.right[4]:
            out = out + 1
        if test_c.close[i] == test_c.close[4]:
            out = out + 1
        if test_c.far[i] == test_c.far[4]:
            out = out + 1
    return out

def check_cross(side):
    if (side[1] == side [4]):
        if (side[3] == side[4]):
            if (side [5] == side[4]):
                if (side[7] == side[4]):
                    return 1
    return 0

def weighted_count(test_c):
    out = 0
    up = 0
    bottom = 0
    left = 0
    right = 0
    close = 0
    far = 0
    crosses = 0
    crosses = crosses + check_cross(test_c.up)
    crosses = crosses + check_cross(test_c.bottom)
    crosses = crosses + check_cross(test_c.left)
    crosses = crosses + check_cross(test_c.right)
    crosses = crosses + check_cross(test_c.far)
    crosses = crosses + check_cross(test_c.close)
    for i in range(9):
        if test_c.up[i] == test_c.up[4]:
            out = out + 1
            up = up + 1
        if test_c.bottom[i] == test_c.bottom[4]:
            out = out + 1
            bottom = bottom + 1
        if test_c.left[i] == test_c.left[4]:
            left = left + 1
            out = out + 1
        if test_c.right[i] == test_c.right[4]:
            right = right + 1
            out = out + 1
        if test_c.close[i] == test_c.close[4]:
            close = close + 1
            out = out + 1
        if test_c.far[i] == test_c.far[4]:
            far = far + 1
            out = out + 1
    if (up == 9) : out = out + 1
    if (bottom == 9) : out = out + 1
    if (left == 9) : out = out + 1
    if (right == 9) : out = out + 1
    if (close == 9) : out = out + 1
    if (far == 9) : out = out + 1
    out = out + crosses
    return out

def calculate_cube(c, moves):
    test_c = deepcopy(c)
    best = - 1
    best_ind = - 1
    for i in range (INDIVIDUAL_SIZE):
        test_c = (OPTIONS[moves[i]](test_c))
        hits = count(test_c)
        if (hits>best):
            best = hits
            best_ind = i
    for i in range (best_ind+1):
        c = (OPTIONS[moves[i]](c))
    print("Moves: ", best_ind)
    return c

def random_search_best(c):
    random_population = [[randint(0, len(OPTIONS) - 1) for j in range(INDIVIDUAL_SIZE)] for i in range(POP_SIZE*GENERATIONS)]
    fitnesses = [usual_fitness(c, random_population[i]) for i in range(POP_SIZE*GENERATIONS)]
    return max(fitnesses)

def main():
    EA_results = []
    random_results = []
    for i in range (RUNS):
        c = Cube()
        c.randomize_cube()
        if (CUBE_DETAILS == True):
            print("Cube Initial State: ")
            c.print_cube()
            starting_count = count(c)
            print("Matching bricks At The Begining: ", starting_count, "\n")
        population = init_population()
        best_of_run = None
        best_of_run_fitness = 0
        best_of_run_genenetation = 0
        fitnesses = [fitness(c, population[i]) for i in range(POP_SIZE)]
        for gen in range(GENERATIONS):
            print("----------Genertaion",gen,"-------")
            nextgen_population = []
            # Elitism
            best = population[fitnesses.index(max(fitnesses))]
            nextgen_population.append(best)
            for i in range(int(POP_SIZE)):
                parent1 = selection(population, fitnesses)
                parent2 = selection(population, fitnesses)
                child = crossover(parent1,parent2)
                child = mutation(c, child)
                nextgen_population.append(child)
            population = nextgen_population
            fitnesses = [fitness(c, population[i]) for i in range(POP_SIZE)]
            if max(fitnesses) > best_of_run_fitness:
                best_of_run_fitness = max(fitnesses)
                best_of_run_genenetation = gen
                best_of_run = population[fitnesses.index(max(fitnesses))]
                print("_________Improvement Achieved!_______________")
                print("gen:", gen, ", best_of_run_f:", max(fitnesses))
            if best_of_run_fitness == 66: break
        print("_________End Of Evolution!_______________")
        if (RANDOM_SEARCH_COMPARE==True):
            random_search_bricks = random_search_best(c)
            print("Random Search Max Bricks: ", random_search_bricks)
        result_c = deepcopy(c)
        result_c = calculate_cube(result_c,best_of_run)
        end_count = count(result_c)
        if (CUBE_DETAILS == True):
            print("The Cube is now:")
            result_c.print_cube()
            print("Matching bricks At The End: " , end_count, "\n")
        print("-----Details:------")
        print("Best Evolutionary Fitness: ", best_of_run_fitness)
        print("Best Generation:", best_of_run_genenetation)
        EA_results.append(end_count)
        print("EA So Far results: " , EA_results)
        if (RANDOM_SEARCH_COMPARE == True):
            print("random So Far results: " , random_results)
            random_results.append(random_search_bricks)
if __name__ == "__main__":
    main()
