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
        
    mi_frontera = utils.Stack()
    nodos_visitados = []  # aqui guardo los estados que ya recorri

    mi_frontera.push((problem.getStartState(), []))  # aqui empiezo desde el estado inicial

    while not mi_frontera.isEmpty():
        estado, camino = mi_frontera.pop()  # aqui saco el ultimo que meti

        if problem.isGoalState(estado): 
            return camino

        if estado not in nodos_visitados:  
            nodos_visitados.append(estado)  # aqui lo marco como visitado
            for sucesor, accion, costo_del_paso in problem.getSuccessors(estado):
                if sucesor not in nodos_visitados:  
                    mi_frontera.push((sucesor, camino + [accion]))  # aqui lo agrego a la pila
                    

    return []  # si no encontre nada, devuelvo vacio


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
    mi_frontera = utils.PriorityQueue()
    nodos_visitados = set()

    estado_inicial = problem.getStartState()
    mi_frontera.push((estado_inicial, [], 0), heuristic(estado_inicial, problem))

    while not mi_frontera.isEmpty():
        estado, camino, costo_acumulado = mi_frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if estado not in nodos_visitados:
            nodos_visitados.add(estado)
            for sucesor, accion, costo_del_paso in problem.getSuccessors(estado):
                if sucesor not in nodos_visitados:
                    nuevo_costo = costo_acumulado + costo_del_paso
                    prioridad = nuevo_costo + heuristic(sucesor, problem)
                    mi_frontera.push((sucesor, camino + [accion], nuevo_costo), prioridad)
    

    return []


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
