import random
from itertools import product
import numpy as np

STATES = {
    'ALABAMA': 5024279, 'ALASKA': 733391, 'ARIZONA': 7151502, 'ARKANSAS': 3011524,
    'CALIFORNIA': 39538223, 'COLORADO': 5773714, 'CONNECTICUT': 3605944, 'DELAWARE': 989948,
    'FLORIDA': 21538187, 'GEORGIA': 10711908, 'HAWAII': 1455271, 'IDAHO': 1839106,
    'ILLINOIS': 12812508, 'INDIANA': 6785528, 'IOWA': 3190369, 'KANSAS': 2937880,
    'KENTUCKY': 4505836, 'LOUISIANA': 4657757, 'MAINE': 1362359, 'MARYLAND': 6177224,
    'MASSACHUSETTS': 7029917, 'MICHIGAN': 10077331, 'MINNESOTA': 5706494, 'MISSISSIPPI': 2961279,
    'MISSOURI': 6154913, 'MONTANA': 1084225, 'NEBRASKA': 1961504, 'NEVADA': 3104614,
    'NEWHAMPSHIRE': 1377529, 'NEWJERSEY': 9288994, 'NEWMEXICO': 2117522, 'NEWYORK': 20201249,
    'NORTHCAROLINA': 10439388, 'NORTH DAKOTA': 779094, 'OHIO': 11799448, 'OKLAHOMA': 3959353,
    'OREGON': 4237256, 'PENNSYLVANIA': 13002700, 'RHODEISLAND': 1097379, 'SOUTHCAROLINA': 5118425,
    'SOUTHDAKOTA': 886667, 'TENNESSEE': 6910840, 'TEXAS': 29145505, 'UTAH': 3271616,
    'VERMONT': 643077, 'VIRGINIA': 8631393, 'WASHINGTON': 7693612, 'WESTVIRGINIA': 1793716,
    'WISCONSIN': 5893718, 'WYOMING': 576851
}

UNIQUE_LETTERS = list({letter for state in STATES for letter in state if letter != ' '})
DIRECTIONS = [d for d in product([-1, 0, 1], repeat = 2) if d != (0,0)]
ALTER_TOLERANCE = 1

### GENETIC ALGORITHM parameters
TEMPERATURE = 7 # the higher the value, the closer to 50/50 the genetics of the child are
MUTATION_RATE = 0.2 # the chance of mutation



class Grid:
    def __init__(self, rows):
        self.R = len(rows)
        self.C = len(rows[0])
        for row in rows:
            if len(row) != self.C:
                raise Exception("row sizes don't match!")
        self.rows = rows
        (self.fitness, self.states) = self.score_grid()

    def init_rand(R, C):
        rows = [[random.choice(UNIQUE_LETTERS) for _ in range(C)] for _ in range(R)]
        return Grid(rows)

    def print_grid(self):
        for row in self.rows:
            print(" ".join(row))

    def get_value(self, pos):
        (r, c) = pos
        return self.rows[r][c]

    def get_neighbors(self, pos):
        (r, c) = pos
        return [(r + dr, c + dc) for dr, dc in DIRECTIONS if 0 <= r + dr < self.R and 0 <= c + dc < self.C]  

    def check_pos(self, pos, letter):
        return self.get_value(pos) == letter

    def check_word_from(self, pos, word, alter=0):
        pos_check = self.check_pos(pos, word[0])
        if not pos_check:
            if alter > ALTER_TOLERANCE:
                return False
            alter += 1
        check_with_alter = pos_check or alter == ALTER_TOLERANCE
        if len(word) == 1:
            return check_with_alter
        return check_with_alter and any([self.check_word_from(n, word[1:], alter=alter) for n in self.get_neighbors(pos)])
    
    def check_word(self, word):
        return any([self.check_word_from((r,c), word) for r in range(self.R) for c in range(self.C)])
    
    def score_grid(self):
        score = 0
        states = []
        for state, population in STATES.items():
            if self.check_word(state):
                score += population
                states.append(state)
        return score, states

    
    def cross(self, other):
        if (self.R != other.R or self.C != other.C):
            raise Exception("To be crossed, grids must be the same size!")
        #if (random.random() < 0.5):
        return self.cross1(other)  
       # else:
       #     return self.cross2(other)
    
    # method 1: crossover at probabilistic k-point (which is biased to the center) split
    def cross1(self, other):
        N = self.R * self.C
        mean = (N - 1) / 2
        std_dev =  N / TEMPERATURE 
        k = int(np.random.normal(mean, std_dev))
        k = max(0, min(N - 1, k)) # make sure k stays within bounds
        child_rows = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                if (random.random() <= MUTATION_RATE):
                    row.append(random.choice(UNIQUE_LETTERS)) # new mutated letter
                elif (r * self.R + c) < k:
                    row.append(self.get_value((r,c))) # letter from self parent
                else:
                    row.append(other.get_value((r,c))) # letter from other parent
            child_rows.append(row)
        return Grid(child_rows)
    
    # method 2: crossover uniformly
    def cross2(self, other):
        child_rows = [[self.get_value((r,c)) if random.random() > 0.5 else other.get_value((r,c)) for c in range(self.C)] for r in range(self.R)]
        return Grid(child_rows)


