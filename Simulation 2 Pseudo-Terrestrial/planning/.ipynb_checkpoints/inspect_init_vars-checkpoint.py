from game import Game
from simulator import Knowledge
from mcts import SearchParams, UnitTestMCTS
from experiment import ExperimentParams, Experiment
from entropy import UnitTestENTROPY
from utils import UnitTestUTILS, Random
from coord import COORD, UnitTestCOORD
from grid import Grid
from entropy import Entropy
from astar import AStar
from math import floor
from time import time

import os, sys, pickle, itertools
from pathlib import Path
import numpy as np

PATH = "/projects/e32704/andy/decisionmaking/gridworld-results/initial_test/init_vars.pkl"


def main():
    with open(PATH, 'rb') as f:
        v = pickle.load(f)

    print(type(v))                  # <class 'list'>
    print(len(v))                   # 2
    print(type(v[0]), type(v[1]))   # <class 'list'> <class 'list'>
    print(len(v[0]), len(v[1]))     # 20 20
    print(type(v[0][0]))            # <class 'list'>
    print(len(v[0][0]))             # 10
    print(type(v[0][0][0]))         # <class 'list'>
    print(len(v[0][0][0]))          # 0
    print(len(v[0][0][1]))          # 3
    


if __name__ == "__main__":
    main()
