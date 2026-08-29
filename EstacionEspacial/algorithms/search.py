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

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    # TODO: Add your code here
    
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    
    """
    nodos_por_expandir = problem.getSuccessors(problem.getStartState())
    nodos_visitados = []
    for i in range (10):
        
        if (nodo_expandido in nodos_visitados):
            nodos_visitados.append(nodo_expandido)
            nodos_por_expandir.delete(tamano_cola-1)
            tamano_cola = len(nodos_por_expandir)
            nodo_expandido = nodos_por_expandir[tamano_cola-1]
            
        else:
            nodo_expandido = nodos_por_expandir[tamano_cola-1]
        
        print("Mi nodo a expandir: ", nodo_expandido)
        
        
        estado_de_mi_sucesor_a_expandir1 = nodo_expandido[0]
        print("Estado / coordendas de mi sucesor a expandir {i}: ", estado_de_mi_sucesor_a_expandir1)
        print ("Este sucesor es la meta? ", problem.isGoalState(estado_de_mi_sucesor_a_expandir1))
            
        sucesores_de_mi_sucesor = problem.getSuccessors(estado_de_mi_sucesor_a_expandir1)
        for j in range (len(sucesores_de_mi_sucesor)):
            nodos_por_expandir.append(sucesores_de_mi_sucesor[j])
            
        print("sucesores de mi sucesor: ", sucesores_de_mi_sucesor)
    """
        
    frontera = utils.Stack()
    visitados = set()
     
    frontera.push((problem.getStartState(), []))
     
    while not frontera.isEmpty():
        estado, camino = frontera.pop()
     
        if estado not in visitados:
            if problem.isGoalState(estado):
                return camino

            visitados.add(estado)
            for sucesor, accion, costoPaso in problem.getSuccessors(estado):
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
    frontera = utils.PriorityQueue()
    visitados = set()

    frontera.push((problem.getStartState(), [], 0), 0)

    while not frontera.isEmpty():
        estado, camino, costo = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if estado not in visitados:
            visitados.add(estado)

            for sucesor, accion, costoPaso in problem.getSuccessors(estado):
                if sucesor not in visitados:
                    nuevo_costo = costo + costoPaso
                    frontera.push((sucesor, camino + [accion], nuevo_costo), nuevo_costo)
    
    return []


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
