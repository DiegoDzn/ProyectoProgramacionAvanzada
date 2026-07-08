import math
from models.road_network import RoadNetwork
from structures.priority_queue import MinPriorityQueue

def bfs(graph: RoadNetwork, start: str, end: str) -> dict:
    """
    Algoritmo BFS (Breadth-First Search) para buscar en anchura sobre la red vial.
    Encuentra la ruta con menor número de tramos (aristas) sin considerar los pesos.

    Complejidad:
        - Tiempo: O(V + E) donde V son nodos y E aristas.
        - Espacio: O(V) para registrar visitados y cola.
    """
    start = start.strip()
    end = end.strip()
    
    if not graph.existe_nodo(start) or not graph.existe_nodo(end):
        return {"ruta": None, "visitados": [], "costo": float("inf")}

    cola = [(start, [start])]
    visitados = []
    visitados_set = {start}

    while cola:
        u, camino = cola.pop(0)
        visitados.append(u)

        if u == end:
            # Calcular el costo de tiempo acumulado de la ruta encontrada
            costo = 0.0
            for k in range(len(camino) - 1):
                costo += graph.obtener_peso(camino[k], camino[k+1])
            return {"ruta": camino, "visitados": visitados, "costo": round(costo, 2)}

        for v in graph.obtener_adyacentes(u):
            if v not in visitados_set:
                visitados_set.add(v)
                cola.append((v, camino + [v]))

    return {"ruta": None, "visitados": visitados, "costo": float("inf")}


def dijkstra(graph: RoadNetwork, start: str, end: str) -> dict:
    """
    Algoritmo Dijkstra para encontrar la ruta más rápida (costo mínimo de tiempo).
    Utiliza un Min-Heap (MinPriorityQueue) de forma eficiente.

    Complejidad:
        - Tiempo: O((V + E) log V).
        - Espacio: O(V) para almacenar distancias y estados.
    """
    start = start.strip()
    end = end.strip()

    if not graph.existe_nodo(start) or not graph.existe_nodo(end):
        return {"ruta": None, "visitados": [], "costo": float("inf")}

    cola = MinPriorityQueue()
    cola.insertar(0.0, (start, [start]))
    
    distancias = {start: 0.0}
    visitados = []
    visitados_set = set()

    while not cola.esta_vacia():
        costo_acum, (u, camino) = cola.extraer_min()

        if u in visitados_set:
            continue
        visitados_set.add(u)
        visitados.append(u)

        if u == end:
            return {"ruta": camino, "visitados": visitados, "costo": round(costo_acum, 2)}

        for v, peso in graph.obtener_adyacentes(u).items():
            if v in visitados_set:
                continue
            
            nueva_dist = costo_acum + peso
            if nueva_dist < distancias.get(v, float("inf")):
                distancias[v] = nueva_dist
                cola.insertar(nueva_dist, (v, camino + [v]))

    return {"ruta": None, "visitados": visitados, "costo": float("inf")}


def a_star(graph: RoadNetwork, start: str, end: str) -> dict:
    """
    Algoritmo de búsqueda informada A* (A-Estrella).
    Utiliza coordenadas de RoadNetwork para calcular la distancia euclidiana como heurística.

    Complejidad:
        - Tiempo: O((V + E) log V) en el peor caso (depende de la calidad de la heurística).
        - Espacio: O(V).
    """
    start = start.strip()
    end = end.strip()

    if not graph.existe_nodo(start) or not graph.existe_nodo(end):
        return {"ruta": None, "visitados": [], "costo": float("inf")}

    def calcular_heuristica(u, v):
        x1, y1 = graph.obtener_coordenadas(u)
        x2, y2 = graph.obtener_coordenadas(v)
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    cola = MinPriorityQueue()
    # Prioridad inicial f = g + h = 0.0 + h(start, end)
    h_start = calcular_heuristica(start, end)
    cola.insertar(h_start, (0.0, start, [start]))
    
    g_scores = {start: 0.0}
    visitados = []
    visitados_set = set()

    while not cola.esta_vacia():
        f_score, (g_score, u, camino) = cola.extraer_min()

        if u in visitados_set:
            continue
        visitados_set.add(u)
        visitados.append(u)

        if u == end:
            return {"ruta": camino, "visitados": visitados, "costo": round(g_score, 2)}

        for v, peso in graph.obtener_adyacentes(u).items():
            if v in visitados_set:
                continue
            
            nuevo_g = g_score + peso
            if nuevo_g < g_scores.get(v, float("inf")):
                g_scores[v] = nuevo_g
                f_score_vecino = nuevo_g + calcular_heuristica(v, end)
                cola.insertar(f_score_vecino, (nuevo_g, v, camino + [v]))

    return {"ruta": None, "visitados": visitados, "costo": float("inf")}
