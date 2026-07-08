import unittest
from models.incident import Incident
from structures.sorting import merge_sort, quick_sort

class TestSorting(unittest.TestCase):
    """Pruebas unitarias para los algoritmos MergeSort y QuickSort."""

    def setUp(self):
        # Elementos numéricos de prueba
        self.num_lista = [5, 2, 9, 1, 5, 6]
        self.num_lista_ordenada_asc = [1, 2, 5, 5, 6, 9]
        self.num_lista_ordenada_desc = [9, 6, 5, 5, 2, 1]

        # Objetos Incident de prueba
        self.incidente_1 = Incident("I-01", "Zona_A", 5.0, "Incendio", 1600000000.0)
        self.incidente_2 = Incident("I-02", "Zona_B", 9.5, "Rescate", 1600000010.0)
        self.incidente_3 = Incident("I-03", "Zona_A", 1.5, "Medico", 1599999900.0)
        self.incidentes = [self.incidente_1, self.incidente_2, self.incidente_3]

    def test_empty_and_single_element(self):
        """Verifica el comportamiento con listas vacías o de un solo elemento."""
        for sort_func in [merge_sort, quick_sort]:
            self.assertEqual(sort_func([]), [])
            self.assertEqual(sort_func([42]), [42])

    def test_numeric_sorting_asc(self):
        """Verifica la ordenación numérica ascendente."""
        for sort_func in [merge_sort, quick_sort]:
            res = sort_func(self.num_lista)
            self.assertEqual(res, self.num_lista_ordenada_asc)
            # Verificar que no modifica la lista original (in-place interna pero retorna copia)
            self.assertEqual(self.num_lista, [5, 2, 9, 1, 5, 6])

    def test_numeric_sorting_desc(self):
        """Verifica la ordenación numérica descendente."""
        for sort_func in [merge_sort, quick_sort]:
            res = sort_func(self.num_lista, reverse=True)
            self.assertEqual(res, self.num_lista_ordenada_desc)

    def test_incident_sorting_by_priority(self):
        """Verifica la ordenación de incidentes por prioridad (descendente)."""
        for sort_func in [merge_sort, quick_sort]:
            res = sort_func(self.incidentes, key=lambda x: x.prioridad, reverse=True)
            self.assertEqual(res[0].id, "I-02")  # Prioridad 9.5
            self.assertEqual(res[1].id, "I-01")  # Prioridad 5.0
            self.assertEqual(res[2].id, "I-03")  # Prioridad 1.5

    def test_incident_sorting_by_timestamp(self):
        """Verifica la ordenación de incidentes por timestamp (ascendente)."""
        for sort_func in [merge_sort, quick_sort]:
            res = sort_func(self.incidentes, key=lambda x: x.timestamp)
            self.assertEqual(res[0].id, "I-03")  # Timestamp 1599999900.0
            self.assertEqual(res[1].id, "I-01")  # Timestamp 1600000000.0
            self.assertEqual(res[2].id, "I-02")  # Timestamp 1600000010.0

    def test_sorting_tuples(self):
        """Verifica la ordenación de tuplas (como frecuencia de zonas)."""
        zonas_frecuencia = [("Zona_A", 12), ("Zona_B", 3), ("Zona_C", 25), ("Zona_D", 12)]
        
        # Ordenar por frecuencia descendente
        for sort_func in [merge_sort, quick_sort]:
            res = sort_func(zonas_frecuencia, key=lambda x: x[1], reverse=True)
            self.assertEqual(res[0], ("Zona_C", 25))
            self.assertEqual(res[-1], ("Zona_B", 3))

    def test_mergesort_stability(self):
        """Verifica que MergeSort sea estable (mantiene orden relativo ante claves iguales)."""
        # Tuplas donde la clave es el primer valor.
        # Ordenaremos por el primer valor.
        # Original: (2, 'a'), (1, 'x'), (2, 'b'), (1, 'y')
        data = [(2, 'a'), (1, 'x'), (2, 'b'), (1, 'y')]
        
        # Ordenación ascendente por número
        res = merge_sort(data, key=lambda x: x[0])
        # Al ser estable, el resultado debe ser: (1, 'x'), (1, 'y'), (2, 'a'), (2, 'b')
        expected = [(1, 'x'), (1, 'y'), (2, 'a'), (2, 'b')]
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()
