import pytest
import random

from algo_class import Algo
from node_class import Node

"""Tests du calcul heuristique manhattan distance et linear conflict"""

@pytest.fixture
def node_generator():
    """Creates nodes for testing functions"""
    Node.h_method = 'manhattan'
    Node.final_grid = [1,2,3,8,0,4,7,6,5]
    Node.size = 3

    Node1 = Node(grid = [5, 8, 6, 2, 0, 7, 4, 1, 3])
    Node2 = Node(grid = [0, 8, 5, 3, 1, 2, 7, 4, 6])

    return [Node1, Node2]


def test_manhattan(node_generator):
    assert node_generator[0].h_calc('manhattan') == 22
    assert node_generator[1].h_calc('manhattan') == 14

