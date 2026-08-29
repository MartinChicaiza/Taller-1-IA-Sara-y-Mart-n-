import math
from typing import Tuple
from algorithms import utils
from algorithms.problems import SystemRepairProblem
from world.game import Directions, Actions


def nullHeuristic(estado, problema=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(estado, problema):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    posicion, tieneKit, sistemasPendientes = estado

    if not tieneKit:
        objetivo = problema.kitPosition
    elif len(sistemasPendientes) > 0:
        objetivo = min(
            sistemasPendientes,
            key=lambda sistema: abs(posicion[0] - sistema[0]) + abs(posicion[1] - sistema[1]),
        )
    else:
        objetivo = problema.controlPosition

    return abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])


def euclideanHeuristic(estado, problema):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    posicion, tieneKit, sistemasPendientes = estado

    def distanciaEuclidea(punto1, punto2):
        return math.sqrt((punto1[0] - punto2[0]) ** 2 + (punto1[1] - punto2[1]) ** 2)

    if not tieneKit:
        objetivo = problema.kitPosition
    elif len(sistemasPendientes) > 0:
        objetivo = min(sistemasPendientes, key=lambda sistema: distanciaEuclidea(posicion, sistema))
    else:
        objetivo = problema.controlPosition

    return distanciaEuclidea(posicion, objetivo)




def mazeDistance(punto1, punto2, problema):
    """
    Devuelve la distancia real de laberinto entre punto1 y punto2, usando
    problem.heuristicInfo como caché. Como K, C y cada T son siempre los
    mismos puntos durante toda la búsqueda (solo cambia la posición del
    robot), cachear evita recalcular el mismo par de puntos en cada nodo
    expandido.
    """
    cache = problema.heuristicInfo.setdefault("mazeDistances", {})
    clave = (punto1, punto2) if punto1 <= punto2 else (punto2, punto1)

    if clave not in cache:
        cache[clave] = _bfsDistance(punto1, punto2, problema.walls)

    return cache[clave]


def systemRepairHeuristic(
    estado: Tuple[Tuple, bool, Tuple], problema: SystemRepairProblem
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
    
    
    # Como podras ver systemRepairHeuristic es casi igual a manhatan, y eso es porque me di cuenta de que 
    ambas siguen la misma lógica (K, T mas cercano, o C segun la fase),solo cambia la métrica: 
    manhattanHeuristic usa línea recta, systemRepairHeuristic usa distancia real de laberinto vía BFS.
    """
    
    posicion, tieneKit, sistemasPendientes = estado

    if not tieneKit:
        objetivo = problema.kitPosition
    elif len(sistemasPendientes) > 0:
        objetivo = min(
            sistemasPendientes,
            key=lambda sistema: mazeDistance(posicion, sistema, problema),
        )
    else:
        objetivo = problema.controlPosition

    return mazeDistance(posicion, objetivo, problema)
