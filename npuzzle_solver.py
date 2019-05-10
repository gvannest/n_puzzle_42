import time

from math import sqrt

from snailer import create_success_grid
from node_class import Node
from algo_class import Algo, Idastar
from visu import Visu

def print_results(algo, detail):
    """ Print the output of the search algorithm, including time and space complexity"""
    if detail:
        for node in algo.path:
            print(node)

    print("=======================")
    print('Number of moves from initial to final state :', len(algo.path) - 1)
    print("=======================")
    print('Time complexity (number of selected nodes) :', algo.selected_nodes)
    print("=======================")
    print('Space complexity (max states in memory at a point in time) :', algo.max_memory)
    print("=======================")
    print('Solving time : {:.3f} s'.format(algo.time))

    return None

def ida_star(node, algo):
    """
    Function which implements our search algorithm using IDA*.

    :param node: node which will be treated in this instance of the function
    :param algo: our search algorithm objects which stores relevant informations about the search process
    :return: none as the outcome of the search algorithm is in the algo object
    """

    directions = ['down', 'up', 'left', 'right']

    def procedure(node, algo):
        threshold = node.h
        while True:
            algo.path = [node]
            algo.closed_set = {tuple(node.grid)}
            t = search(threshold)
            if t == "FOUND":
                return None
            threshold = t
            algo.clear()

    def search(threshold):
            min = -1
            node = algo.path[-1]
            if node.f > threshold: return node.f
            if node.is_final(): return "FOUND"
            queue = []
            for d in directions:
                new_node = node.move(d, algo)
                if new_node:
                    algo.push_to_heap(new_node, queue)
            child_node = algo.pop_from_heap(queue)
            while child_node:
                if tuple(child_node.grid) not in algo.closed_set:
                    algo.path.append(child_node)
                    algo.closed_set.add(tuple(child_node.grid))
                    t = search(threshold)
                    if t == "FOUND":
                        return t
                    min = t if min==-1 or t < min else min
                algo.path.pop()
                algo.closed_set.remove(tuple(child_node.grid))
                algo.memory_state -= 1
                child_node = algo.pop_from_heap(queue)
            return min

    return procedure(node, algo)


def search_algo(node, algo):
    """
    Function which implements our search algorithm : A*, gbfs or uniform_cost.

    :param node: node which will be treated in this instance of the function
    :param algo: our search algorithm objects which stores relevant informations about the search process
    :return: none as the outcome of the search algorithm is in the algo object
    """

    directions = ['down', 'up', 'left', 'right']
    while not node.is_final():
        for d in directions:
            new_node = node.move(d, algo)
            if new_node:
                algo.push_to_heap(new_node)
        algo.closed_set.add(tuple(node.grid))
        node = algo.pop_from_heap()

    while node:
        algo.path.appendleft(node)
        node = node.parent
    return None

def main(grid, args):
    grid_size = int(sqrt(len(grid)))
    Node.final_grid = create_success_grid(grid_size)
    Node.size = grid_size
    Node.h_method = args.method
    Node.h_algo = args.algo

    initial_node = Node(grid=grid, g=0, parent=None)
    start = time.time()
    if args.algo == 'ida_star':
        algo = Idastar()
        ida_star(initial_node, algo)
    else:
        algo = Algo()
        search_algo(initial_node, algo)
    end = time.time()
    algo.time = end - start

    if args.visu:
        visu = Visu(algo)
        visu.play()
    else:
        print_results(algo, args.detail)
    return None


if __name__ == "__main__":
    initial_grid = [3,1,5,7,2,6,8,0,4]
    main(initial_grid)
