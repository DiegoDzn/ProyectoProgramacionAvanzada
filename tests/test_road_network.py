import unittest
from models import RoadNetwork

class TestRoadNetwork(unittest.TestCase):
    """Pruebas unitarias para verificar el correcto funcionamiento del ADT RoadNetwork."""

    def test_creation(self):
        """Verifica la inicialización vacía de la red vial."""
        net = RoadNetwork()
        self.assertEqual(len(net.obtener_nodos()), 0)

    def test_agregar_nodo(self):
        """Verifica la inserción de nodos y sus validaciones."""
        net = RoadNetwork()
        net.agregar_nodo("Nodo_A")
        self.assertTrue(net.existe_nodo("Nodo_A"))
        self.assertFalse(net.existe_nodo("Nodo_B"))
        self.assertEqual(net.obtener_nodos(), ["Nodo_A"])

        # Insertar nodo duplicado no debería cambiar la lista
        net.agregar_nodo("Nodo_A")
        self.assertEqual(net.obtener_nodos(), ["Nodo_A"])

        # Validaciones de precondiciones
        with self.assertRaises(ValueError):
            net.agregar_nodo("")
        with self.assertRaises(ValueError):
            net.agregar_nodo("  ")
        with self.assertRaises(ValueError):
            net.agregar_nodo(None)

    def test_agregar_arista_bidireccional(self):
        """Verifica la inserción de aristas bidireccionales."""
        net = RoadNetwork()
        net.agregar_nodo("Nodo_A")
        net.agregar_nodo("Nodo_B")

        # Agregar arista bidireccional
        net.agregar_arista("Nodo_A", "Nodo_B", 10.5, bidireccional=True)
        self.assertTrue(net.existe_arista("Nodo_A", "Nodo_B"))
        self.assertTrue(net.existe_arista("Nodo_B", "Nodo_A"))

        # Consultar pesos
        self.assertEqual(net.obtener_peso("Nodo_A", "Nodo_B"), 10.5)
        self.assertEqual(net.obtener_peso("Nodo_B", "Nodo_A"), 10.5)

    def test_agregar_arista_unidireccional(self):
        """Verifica la inserción de aristas unidireccionales."""
        net = RoadNetwork()
        net.agregar_nodo("Nodo_A")
        net.agregar_nodo("Nodo_B")

        # Agregar arista unidireccional
        net.agregar_arista("Nodo_A", "Nodo_B", 5.0, bidireccional=False)
        self.assertTrue(net.existe_arista("Nodo_A", "Nodo_B"))
        self.assertFalse(net.existe_arista("Nodo_B", "Nodo_A"))

        self.assertEqual(net.obtener_peso("Nodo_A", "Nodo_B"), 5.0)
        with self.assertRaises(ValueError):
            net.obtener_peso("Nodo_B", "Nodo_A")

    def test_agregar_arista_validaciones(self):
        """Verifica precondiciones al agregar aristas."""
        net = RoadNetwork()
        net.agregar_nodo("Nodo_A")

        # Nodos que no existen
        with self.assertRaises(ValueError):
            net.agregar_arista("Nodo_A", "Nodo_Inexistente", 10.0)
        with self.assertRaises(ValueError):
            net.agregar_arista("Nodo_Inexistente", "Nodo_A", 10.0)

        # Pesos negativos o inválidos
        net.agregar_nodo("Nodo_B")
        with self.assertRaises(ValueError):
            net.agregar_arista("Nodo_A", "Nodo_B", -1.0)
        with self.assertRaises(ValueError):
            net.agregar_arista("Nodo_A", "Nodo_B", "diez")

    def test_obtener_adyacentes(self):
        """Verifica la consulta de nodos adyacentes."""
        net = RoadNetwork()
        net.agregar_nodo("Nodo_A")
        net.agregar_nodo("Nodo_B")
        net.agregar_nodo("Nodo_C")

        net.agregar_arista("Nodo_A", "Nodo_B", 3.0, bidireccional=False)
        net.agregar_arista("Nodo_A", "Nodo_C", 7.0, bidireccional=False)

        adyacentes_a = net.obtener_adyacentes("Nodo_A")
        self.assertEqual(adyacentes_a, {"Nodo_B": 3.0, "Nodo_C": 7.0})

        # Comprobar que modificar el dict retornado no altera la red interna
        adyacentes_a["Nodo_B"] = 99.0
        self.assertEqual(net.obtener_peso("Nodo_A", "Nodo_B"), 3.0)

        # Consultar adyacentes de nodo inexistente
        with self.assertRaises(ValueError):
            net.obtener_adyacentes("Nodo_Inexistente")

if __name__ == "__main__":
    unittest.main()
