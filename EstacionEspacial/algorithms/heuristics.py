import math
from typing import Tuple
from algorithms import utils
from algorithms.problems import SystemRepairProblem
from world.game import Directions, Actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pendingSystems = state

    if not hasKit:
        objetivo = problem.kitPosition
    elif len(pendingSystems) > 0:
        objetivo = min(
            pendingSystems,
            key=lambda t: abs(position[0] - t[0]) + abs(position[1] - t[1]),
        )
    else:
        objetivo = problem.controlPosition

    return abs(position[0] - objetivo[0]) + abs(position[1] - objetivo[1])


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pendingSystems = state

    def distanciaEuclidea(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    if not hasKit:
        objetivo = problem.kitPosition
    elif len(pendingSystems) > 0:
        objetivo = min(pendingSystems, key=lambda t: distanciaEuclidea(position, t))
    else:
        objetivo = problem.controlPosition

    return distanciaEuclidea(position, objetivo)


def _bfsDistance(inicio, meta, walls):
    """
    Calcula la distancia real (en pasos) entre 'inicio' y 'meta' recorriendo
    el mapa con BFS y respetando las paredes (walls). Es la distancia real
    del laberinto, no una estimación en línea recta.
    """
    if inicio == meta:
        return 0

    frontera = utils.Queue()
    visitados = {inicio}
    frontera.push((inicio, 0))

    while not frontera.isEmpty():
        (x, y), distancia = frontera.pop()

        for direction in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST,
        ]:
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)

            if not walls[nextx][nexty]:
                siguiente = (nextx, nexty)
                if siguiente == meta:
                    return distancia + 1
                if siguiente not in visitados:
                    visitados.add(siguiente)
                    frontera.push((siguiente, distancia + 1))

    # No debería ocurrir en un mapa válido y conexo
    return 999999


def mazeDistance(punto1, punto2, problem):
    """
    Devuelve la distancia real de laberinto entre punto1 y punto2, usando
    problem.heuristicInfo como caché. Como K, C y cada T son siempre los
    mismos puntos durante toda la búsqueda (solo cambia la posición del
    robot), cachear evita recalcular el mismo par de puntos en cada nodo
    expandido.
    """
    cache = problem.heuristicInfo.setdefault("mazeDistances", {})
    clave = (punto1, punto2) if punto1 <= punto2 else (punto2, punto1)

    if clave not in cache:
        cache[clave] = _bfsDistance(punto1, punto2, problem.walls)

    return cache[clave]


def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    position, hasKit, pendingSystems = state

    if not hasKit:
        objetivo = problem.kitPosition
    elif len(pendingSystems) > 0:
        objetivo = min(
            pendingSystems,
            key=lambda t: mazeDistance(position, t, problem),
        )
    else:
        objetivo = problem.controlPosition

    return mazeDistance(position, objetivo, problem)
