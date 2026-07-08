import unittest
from models.road_network import RoadNetwork
from structures.graph_search import bfs, dijkstra, a_star

class TestSearchAlgorithms(unittest.TestCase):
    """Pruebas unitarias para los algoritmos de búsqueda: BFS, Dijkstra y A*."""

    def setUp(self):
        # Crear red vial de prueba:
        # A(0,0) --(30)--------------> C(0,4)   [Ruta más corta en hops (1 hop, costo 30)]
        # A(0,0) --(2)--> D(0,2) --(2)--> C(0,4) [Ruta más rápida en peso (2 hops, costo 4)]
        # A(0,0) --(10.2)--> B(10,2) --(10.2)--> C(0,4) [Ruta larga (2 hops, costo 20.4)]
        # E(30,30) está desconectado.
        self.net = RoadNetwork()
        for node in ["A", "B", "C", "D", "E"]:
            self.net.agregar_nodo(node)

        self.net.establecer_coordenadas("A", 0.0, 0.0)
        self.net.establecer_coordenadas("B", 10.0, 2.0)
        self.net.establecer_coordenadas("C", 0.0, 4.0)
        self.net.establecer_coordenadas("D", 0.0, 2.0)
        self.net.establecer_coordenadas("E", 30.0, 30.0)

        # Aristas
        self.net.agregar_arista("A", "C", 30.0, bidireccional=True)
        self.net.agregar_arista("A", "D", 2.0, bidireccional=True)
        self.net.agregar_arista("D", "C", 2.0, bidireccional=True)
        self.net.agregar_arista("A", "B", 10.2, bidireccional=True)
        self.net.agregar_arista("B", "C", 10.2, bidireccional=True)

    def test_bfs_shortest_hops(self):
        """Verifica que BFS encuentre la ruta con menos hops (A -> C = 1 hop, costo 30)."""
        res = bfs(self.net, "A", "C")
        self.assertEqual(res["ruta"], ["A", "C"])
        self.assertEqual(res["costo"], 30.0)
        self.assertIn("A", res["visitados"])

    def test_dijkstra_fastest_time(self):
        """Verifica que Dijkstra encuentre la ruta más rápida en tiempo (A -> D -> C, costo 4)."""
        res = dijkstra(self.net, "A", "C")
        self.assertEqual(res["ruta"], ["A", "D", "C"])
        self.assertEqual(res["costo"], 4.0)

    def test_a_star_fastest_time(self):
        """Verifica que A* encuentre la ruta óptima idéntica a Dijkstra en costo (costo 4)."""
        res = a_star(self.net, "A", "C")
        self.assertEqual(res["ruta"], ["A", "D", "C"])
        self.assertEqual(res["costo"], 4.0)

    def test_disconnected_destination(self):
        """Verifica el comportamiento cuando no existe ruta al destino (nodo E)."""
        for search_func in [bfs, dijkstra, a_star]:
            res = search_func(self.net, "A", "E")
            self.assertIsNone(res["ruta"])
            self.assertEqual(res["costo"], float("inf"))

    def test_nonexistent_nodes(self):
        """Verifica que buscar con nodos que no están en el grafo retorne None e infinito."""
        for search_func in [bfs, dijkstra, a_star]:
            res1 = search_func(self.net, "A", "X")
            res2 = search_func(self.net, "X", "A")
            self.assertIsNone(res1["ruta"])
            self.assertEqual(res1["costo"], float("inf"))
            self.assertIsNone(res2["ruta"])
            self.assertEqual(res2["costo"], float("inf"))

if __name__ == "__main__":
    unittest.main()
