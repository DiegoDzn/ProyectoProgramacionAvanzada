import unittest
from models.incident import Incident
from models.center import EmergencyCenter
from structures.hash_table import HashTable


class TestADTs(unittest.TestCase):
    """Pruebas unitarias para verificar los ADTs Incident y EmergencyCenter."""

    def test_incident_creation_and_validation(self):
        # Crear incidente válido
        inc = Incident("I-101", "Zona_A", 4.5, "Incendio", 1625097600.0)
        self.assertEqual(inc.id, "I-101")
        self.assertEqual(inc.ubicacion, "Zona_A")
        self.assertEqual(inc.prioridad, 4.5)
        self.assertEqual(inc.tipo, "Incendio")
        self.assertEqual(inc.timestamp, 1625097600.0)
        self.assertEqual(inc.estado, "Pendiente")

        # Validaciones de precondiciones
        with self.assertRaises(ValueError):
            Incident("", "Zona_A", 4.5, "Incendio", 1625097600.0)  # ID vacío
        with self.assertRaises(ValueError):
            Incident("I-101", "  ", 4.5, "Incendio", 1625097600.0)  # Ubicación vacía
        with self.assertRaises(ValueError):
            Incident("I-101", "Zona_A", -1.0, "Incendio", 1625097600.0)  # Prioridad negativa
        with self.assertRaises(ValueError):
            Incident("I-101", "Zona_A", 4.5, "Incendio", -50.0)  # Timestamp negativo
        with self.assertRaises(ValueError):
            Incident("I-101", "Zona_A", 4.5, "Incendio", 1625097600.0, estado="Invalido")  # Estado inválido

    def test_incident_state_update(self):
        inc = Incident("I-101", "Zona_A", 4.5, "Incendio", 1625097600.0)
        inc.actualizar_estado("En Proceso")
        self.assertEqual(inc.estado, "En Proceso")
        
        inc.actualizar_estado("Resuelto")
        self.assertEqual(inc.estado, "Resuelto")

        with self.assertRaises(ValueError):
            inc.actualizar_estado("Completado")  # Estado no permitido

    def test_incident_priority_update(self):
        inc = Incident("I-101", "Zona_A", 4.5, "Incendio", 1625097600.0)
        inc.prioridad = 10.0
        self.assertEqual(inc.prioridad, 10.0)

        with self.assertRaises(ValueError):
            inc.prioridad = -2.5

    def test_emergency_center_creation(self):
        center = EmergencyCenter("C-01", "Hospital Central", "Zona_Centro")
        self.assertEqual(center.id, "C-01")
        self.assertEqual(center.nombre, "Hospital Central")
        self.assertEqual(center.ubicacion, "Zona_Centro")

        with self.assertRaises(ValueError):
            EmergencyCenter("", "Hospital Central", "Zona_Centro")
        with self.assertRaises(ValueError):
            EmergencyCenter("C-01", "", "Zona_Centro")


class TestHashTable(unittest.TestCase):
    """Pruebas unitarias para la HashTable propia."""

    def test_insert_and_get(self):
        ht = HashTable(initial_capacity=11)
        self.assertEqual(ht.size, 0)

        # Inserciones básicas
        inserted1 = ht.insert("I-101", "Incidente 1")
        inserted2 = ht.insert("I-102", "Incidente 2")
        self.assertTrue(inserted1)
        self.assertTrue(inserted2)
        self.assertEqual(ht.size, 2)

        self.assertEqual(ht.get("I-101"), "Incidente 1")
        self.assertEqual(ht.get("I-102"), "Incidente 2")

        # Verificar contención
        self.assertTrue("I-101" in ht)
        self.assertFalse("I-999" in ht)

    def test_update_value(self):
        ht = HashTable(initial_capacity=11)
        ht.insert("I-101", "Original")
        self.assertEqual(ht.get("I-101"), "Original")

        # Actualizar misma clave
        inserted = ht.insert("I-101", "Modificado")
        self.assertFalse(inserted)  # Retorna False porque es actualización
        self.assertEqual(ht.size, 1)
        self.assertEqual(ht.get("I-101"), "Modificado")

    def test_delete(self):
        ht = HashTable(initial_capacity=11)
        ht.insert("I-101", "Valor")
        self.assertEqual(ht.size, 1)

        deleted = ht.delete("I-101")
        self.assertTrue(deleted)
        self.assertEqual(ht.size, 0)
        self.assertFalse("I-101" in ht)

        # Intentar eliminar inexistente
        with self.assertRaises(KeyError):
            ht.delete("I-101")

    def test_resize_and_rehash(self):
        # Iniciamos con capacidad pequeña
        ht = HashTable(initial_capacity=5)  # Se ajusta al siguiente primo mayor o igual: 5 es primo.
        initial_capacity = ht.capacity
        self.assertEqual(initial_capacity, 5)

        # Insertamos elementos para forzar redimensionamiento (> 0.75 de factor de carga)
        # Límite para cap=5: 5 * 0.75 = 3.75 (se activa al insertar el 4to elemento)
        ht.insert("K1", "V1")
        ht.insert("K2", "V2")
        ht.insert("K3", "V3")
        self.assertEqual(ht.capacity, 5)
        self.assertEqual(ht.size, 3)

        # 4to elemento activa rehash
        ht.insert("K4", "V4")
        # Nueva capacidad esperada: next_prime(5 * 2) = next_prime(10) = 11
        self.assertEqual(ht.capacity, 11)
        self.assertEqual(ht.size, 4)

        # Verificar que todos los elementos sigan accesibles
        self.assertEqual(ht.get("K1"), "V1")
        self.assertEqual(ht.get("K2"), "V2")
        self.assertEqual(ht.get("K3"), "V3")
        self.assertEqual(ht.get("K4"), "V4")

    def test_metrics(self):
        # Forzar colisiones insertando claves que den el mismo hash.
        # Como usamos Horner con p=31, diseñamos un hash table con capacidad pequeña y claves.
        ht = HashTable(initial_capacity=7)
        
        # Para asegurarnos de las colisiones, podemos simplemente insertar muchos elementos
        # en una tabla que tiene redimensionamiento desactivado o simplemente insertar y medir.
        # Si insertamos 3 elementos en una tabla de cap=7, el factor de carga es 3/7 ≈ 0.428.
        # Medimos las métricas directamente.
        ht.insert("I-001", "A")
        ht.insert("I-002", "B")
        ht.insert("I-003", "C")

        stats = ht.get_stats()
        self.assertEqual(stats["size"], 3)
        self.assertEqual(stats["capacity"], 7)
        self.assertEqual(stats["load_factor"], round(3 / 7, 4))
        
        # Verificar coherencia matemática
        # total_collisions = sum(len(bucket) - 1 for bucket en table si len > 1)
        computed_collisions = 0
        buckets_used = 0
        max_bucket_size = 0
        for i in range(ht.capacity):
            bucket_len = len(ht._table[i])
            if bucket_len > 0:
                buckets_used += 1
            if bucket_len > max_bucket_size:
                max_bucket_size = bucket_len
            if bucket_len > 1:
                computed_collisions += (bucket_len - 1)

        self.assertEqual(stats["collisions"], computed_collisions)
        self.assertEqual(stats["buckets_used"], buckets_used)
        self.assertEqual(stats["max_bucket_size"], max_bucket_size)


if __name__ == "__main__":
    unittest.main()
