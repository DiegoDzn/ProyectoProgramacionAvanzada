import unittest
import time
from models.incident import Incident
from structures.priority_queue import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
    """Pruebas unitarias para verificar la Cola de Prioridad basada en Heap."""

    def test_init_and_properties(self):
        """Verifica la inicialización vacía de la cola de prioridad."""
        pq = PriorityQueue()
        self.assertTrue(pq.esta_vacia())
        self.assertEqual(len(pq), 0)
        self.assertFalse(pq.contiene("I-101"))

    def test_insertar_and_extraer(self):
        """Verifica la inserción y extracción en orden correcto de prioridad."""
        pq = PriorityQueue()
        
        inc_baja = Incident("I-101", "Zona_A", 2.0, "Incendio", 100.0)
        inc_alta = Incident("I-102", "Zona_B", 9.0, "Accidente", 101.0)
        inc_media = Incident("I-103", "Zona_C", 5.5, "Rescate", 102.0)

        pq.insertar(inc_baja)
        pq.insertar(inc_alta)
        pq.insertar(inc_media)

        self.assertEqual(len(pq), 3)
        self.assertFalse(pq.esta_vacia())
        self.assertTrue(pq.contiene("I-101"))
        self.assertTrue(pq.contiene("I-102"))
        self.assertTrue(pq.contiene("I-103"))

        # Debe extraer en orden: alta (9.0) -> media (5.5) -> baja (2.0)
        first = pq.extraer_urgente()
        self.assertEqual(first.id, "I-102")
        self.assertFalse(pq.contiene("I-102"))
        self.assertEqual(len(pq), 2)

        second = pq.extraer_urgente()
        self.assertEqual(second.id, "I-103")
        self.assertEqual(len(pq), 1)

        third = pq.extraer_urgente()
        self.assertEqual(third.id, "I-101")
        self.assertEqual(len(pq), 0)
        self.assertTrue(pq.esta_vacia())

    def test_incidente_duplicado_lanzar_error(self):
        """Verifica que no se permita insertar incidentes con el mismo ID."""
        pq = PriorityQueue()
        inc1 = Incident("I-100", "Zona_A", 4.0, "Medico", 100.0)
        inc2 = Incident("I-100", "Zona_B", 7.0, "Incendio", 101.0)

        pq.insertar(inc1)
        with self.assertRaises(ValueError):
            pq.insertar(inc2)

    def test_extraer_de_vacio_lanzar_error(self):
        """Verifica que extraer de una cola vacía lance un IndexError."""
        pq = PriorityQueue()
        with self.assertRaises(IndexError):
            pq.extraer_urgente()

    def test_empate_prioridades_timestamp(self):
        """Verifica que si hay empate de prioridad, se extrae el de menor timestamp (más antiguo)."""
        pq = PriorityQueue()
        
        # Ambos tienen prioridad 5.0
        inc_antiguo = Incident("I-101", "Zona_A", 5.0, "Derrumbe", 50.0)
        inc_reciente = Incident("I-102", "Zona_B", 5.0, "Derrumbe", 120.0)

        pq.insertar(inc_reciente)
        pq.insertar(inc_antiguo)

        # Debe extraer primero el antiguo (50.0 < 120.0)
        first = pq.extraer_urgente()
        self.assertEqual(first.id, "I-101")
        second = pq.extraer_urgente()
        self.assertEqual(second.id, "I-102")

    def test_actualizar_prioridad_incrementar(self):
        """Verifica el reacomodo de un elemento cuando sube su prioridad (sift-up)."""
        pq = PriorityQueue()
        inc_baja = Incident("I-101", "Zona_A", 1.0, "Rescate", 100.0)
        inc_alta = Incident("I-102", "Zona_B", 8.0, "Incendio", 101.0)
        
        pq.insertar(inc_baja)
        pq.insertar(inc_alta)

        # Al actualizar I-101 de 1.0 a 10.0, debe subir por encima de I-102 (8.0)
        pq.actualizar_prioridad("I-101", 10.0)
        self.assertEqual(pq._heap[0].id, "I-101")
        self.assertEqual(pq.extraer_urgente().id, "I-101")

    def test_actualizar_prioridad_decrementar(self):
        """Verifica el reacomodo de un elemento cuando baja su prioridad (sift-down)."""
        pq = PriorityQueue()
        inc_alta = Incident("I-102", "Zona_B", 8.0, "Incendio", 101.0)
        inc_media = Incident("I-103", "Zona_C", 5.0, "Rescate", 102.0)
        
        pq.insertar(inc_alta)
        pq.insertar(inc_media)

        # Al bajar I-102 de 8.0 a 2.0, debe quedar debajo de I-103 (5.0)
        pq.actualizar_prioridad("I-102", 2.0)
        self.assertEqual(pq.extraer_urgente().id, "I-103")
        self.assertEqual(pq.extraer_urgente().id, "I-102")

    def test_actualizar_prioridad_inexistente(self):
        """Verifica que actualizar la prioridad de un ID que no existe lance KeyError."""
        pq = PriorityQueue()
        with self.assertRaises(KeyError):
            pq.actualizar_prioridad("I-999", 5.0)

    def test_obtener_top_k(self):
        """Verifica la consulta de los Top-K incidentes sin mutar el heap original."""
        pq = PriorityQueue()
        
        incidentes = [
            Incident("I-01", "Zona_A", 3.0, "A", 10.0),
            Incident("I-02", "Zona_B", 9.0, "B", 11.0),
            Incident("I-03", "Zona_C", 7.0, "C", 12.0),
            Incident("I-04", "Zona_D", 1.0, "D", 13.0),
        ]
        
        for inc in incidentes:
            pq.insertar(inc)

        top_2 = pq.obtener_top_k(2)
        self.assertEqual(len(top_2), 2)
        self.assertEqual(top_2[0].id, "I-02") # Prioridad 9.0
        self.assertEqual(top_2[1].id, "I-03") # Prioridad 7.0

        # Verificar que la cola original sigue intacta
        self.assertEqual(len(pq), 4)
        self.assertEqual(pq.extraer_urgente().id, "I-02")

        # Consultar K mayor que el tamaño de la cola
        top_10 = pq.obtener_top_k(10)
        self.assertEqual(len(top_10), 3) # Quedaban 3 en la cola
        self.assertEqual(top_10[0].id, "I-03")

        # Validaciones de K
        with self.assertRaises(ValueError):
            pq.obtener_top_k(0)
        with self.assertRaises(ValueError):
            pq.obtener_top_k(-1)

if __name__ == "__main__":
    unittest.main()
