class HashTable:
    """
    Implementación propia de una Tabla Hash utilizando Direccionamiento Encadenado (Separate Chaining).
    Diseñada específicamente para almacenar incidentes u otros objetos asociados a una clave (string).
    No utiliza el diccionario ('dict') nativo de Python para su funcionamiento interno.

    Complejidades:
        - Inserción (sin colisiones): O(1) promedio, O(N) peor caso.
        - Búsqueda: O(1) promedio, O(N) peor caso.
        - Eliminación: O(1) promedio, O(N) peor caso.
        - Redimensionamiento (Rehash): O(N) tiempo, O(N) espacio.
    """

    def __init__(self, initial_capacity: int = 97):
        """
        Inicializa la tabla hash con una capacidad inicial (preferiblemente un número primo).

        Precondiciones:
            - initial_capacity debe ser un entero positivo.
        """
        if not isinstance(initial_capacity, int) or initial_capacity <= 0:
            raise ValueError("La capacidad inicial debe ser un entero positivo.")
        
        self._capacity = self._next_prime(initial_capacity)
        self._size = 0
        # Inicializamos el arreglo con listas vacías (Separate Chaining)
        self._table = [[] for _ in range(self._capacity)]

    def _is_prime(self, n: int) -> bool:
        """Determina si un número es primo (O(sqrt(N)))."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _next_prime(self, n: int) -> int:
        """Encuentra el menor número primo mayor o igual a n (O(N * sqrt(N)))."""
        prime = n
        if prime % 2 == 0:
            prime += 1
        while not self._is_prime(prime):
            prime += 2
        return prime

    def _hash(self, key: str) -> int:
        """
        Función hash personalizada para cadenas utilizando el método polinomial (Horner).
        Evita depender del hash() interno de Python que tiene aleatoriedad de semilla (seed).
        """
        h = 0
        p = 31  # Constante multiplicativa
        for char in key:
            h = (h * p + ord(char)) & 0xFFFFFFFFFFFFFFFF  # Mantener dentro de 64 bits
        return h % self._capacity

    @property
    def size(self) -> int:
        """Retorna la cantidad de elementos en la tabla."""
        return self._size

    @property
    def capacity(self) -> int:
        """Retorna la capacidad actual del arreglo."""
        return self._capacity

    @property
    def load_factor(self) -> float:
        """Retorna el factor de carga actual (alfa = N/M)."""
        return self._size / self._capacity

    @property
    def collisions(self) -> int:
        """
        Retorna el número total de colisiones actuales en la tabla.
        Definido matemáticamente como la suma de (longitud - 1) para cada bucket con colisiones.
        """
        total_collisions = 0
        for bucket in self._table:
            if len(bucket) > 1:
                total_collisions += len(bucket) - 1
        return total_collisions

    @property
    def buckets_used(self) -> int:
        """Retorna la cantidad de buckets (casillas) que contienen al menos un elemento."""
        return sum(1 for bucket in self._table if len(bucket) > 0)

    @property
    def max_bucket_size(self) -> int:
        """Retorna la longitud del bucket más largo (cadena de colisiones máxima)."""
        if not self._table:
            return 0
        return max(len(bucket) for bucket in self._table)

    def insert(self, key: str, value) -> bool:
        """
        Inserta un par clave-valor en la tabla hash. Si la clave ya existe, actualiza su valor.

        Precondiciones:
            - key debe ser una cadena no vacía.
        Postcondiciones:
            - El par (key, value) es almacenado en la tabla hash.
            - Si es una clave nueva y el factor de carga supera 0.75, la tabla se redimensiona.
            - Retorna True si se insertó un nuevo elemento, False si se actualizó uno existente.
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError("La clave debe ser una cadena de texto no vacía.")

        key = key.strip()
        index = self._hash(key)
        bucket = self._table[index]

        # Verificar si la clave ya existe para actualizar el valor
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return False  # Actualizado

        # Si no existe, lo agregamos al final del bucket
        bucket.append((key, value))
        self._size += 1

        # Verificar si es necesario redimensionar
        if self.load_factor > 0.75:
            self._resize()

        return True  # Insertado nuevo

    def get(self, key: str):
        """
        Busca y retorna el valor asociado a la clave.

        Precondiciones:
            - key debe ser una cadena de texto no vacía.
        Postcondiciones:
            - Retorna el valor si la clave existe.
            - Lanza KeyError si la clave no está registrada en la tabla.
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError("La clave debe ser una cadena de texto no vacía.")

        key = key.strip()
        index = self._hash(key)
        bucket = self._table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"La clave '{key}' no se encuentra en la tabla hash.")

    def contains(self, key: str) -> bool:
        """
        Verifica si una clave existe en la tabla hash (O(1) promedio).
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def delete(self, key: str) -> bool:
        """
        Elimina el elemento asociado a la clave de la tabla hash.

        Precondiciones:
            - key debe ser una cadena de texto no vacía.
        Postcondiciones:
            - Elimina la clave de la tabla, decrementando size en 1.
            - Retorna True si se eliminó con éxito.
            - Lanza KeyError si la clave no existe.
        """
        if not isinstance(key, str) or not key.strip():
            raise ValueError("La clave debe ser una cadena de texto no vacía.")

        key = key.strip()
        index = self._hash(key)
        bucket = self._table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True

        raise KeyError(f"La clave '{key}' no se encuentra en la tabla hash.")

    def _resize(self):
        """
        Redimensiona internamente la tabla hash al siguiente número primo
        mayor al doble de su capacidad actual, y reordena todos los elementos (rehash).
        """
        old_table = self._table
        new_capacity = self._next_prime(self._capacity * 2)
        
        self._capacity = new_capacity
        self._table = [[] for _ in range(self._capacity)]
        self._size = 0  # Se recalcula al insertar de nuevo

        for bucket in old_table:
            for k, v in bucket:
                self.insert(k, v)

    def get_stats(self) -> dict:
        """
        Retorna un reporte de métricas y estadísticas actuales de la tabla hash.
        """
        return {
            "capacity": self._capacity,
            "size": self._size,
            "load_factor": round(self.load_factor, 4),
            "collisions": self.collisions,
            "buckets_used": self.buckets_used,
            "max_bucket_size": self.max_bucket_size
        }

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: str) -> bool:
        return self.contains(key)
