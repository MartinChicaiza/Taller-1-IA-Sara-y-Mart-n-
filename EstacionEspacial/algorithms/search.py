from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    """

    frontera = utils.Stack()
    visitados = set()

    frontera.push((problem.getStartState(), []))

    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if estado not in visitados:
            visitados.add(estado)
            for sucesor, accion, _ in problem.getSuccessors(estado):
                if sucesor not in visitados:
                    frontera.push((sucesor, camino + [accion]))

    return []


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    frontera = utils.Queue()
    visitados = set()

    if problem.isGoalState(problem.getStartState()):
        return []

    frontera.push((problem.getStartState(), []))
    visitados.add(problem.getStartState())

    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if problem.isGoalState(sucesor):
                return camino + [accion]

            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.push((sucesor, camino + [accion]))

    return []


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    utils.raiseNotDefined()


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
