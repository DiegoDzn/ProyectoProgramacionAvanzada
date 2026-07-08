from models.incident import Incident

class PriorityQueue:
    """
    Tipo de Dato Abstracto (ADT) que representa una Cola de Prioridad para incidentes.
    Implementado mediante un Heap Binario de Máximos (Max-Heap) representado en un arreglo.
    
    Utiliza un mapa de posiciones interno para poder buscar y actualizar
    la prioridad de un incidente en tiempo logarítmico O(log N).

    Estabilidad de prioridad:
        - Si dos incidentes tienen la misma prioridad, se prioriza el que tiene menor
          timestamp (el que se reportó primero en el tiempo).

    Complejidades:
        - Inserción (insertar): O(log N) tiempo.
        - Extracción (extraer_urgente): O(log N) tiempo.
        - Actualización (actualizar_prioridad): O(log N) tiempo.
        - Obtener Top-K (obtener_top_k): O(K log N) tiempo.
        - Consultar tamaño: O(1) tiempo.
    """

    def __init__(self):
        """
        Constructor de la cola de prioridad.

        Precondiciones:
            - Ninguna.
        Postcondiciones:
            - Inicializa un heap vacío y un mapa de posiciones vacío.
        """
        self._heap = []
        # Diccionario que asocia incident_id -> índice en self._heap
        self._posiciones = {}

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la cola de prioridad (O(1))."""
        return len(self._heap)

    def esta_vacia(self) -> bool:
        """Verifica si la cola está vacía (O(1))."""
        return len(self._heap) == 0

    def contiene(self, incident_id: str) -> bool:
        """Verifica si un incidente está en la cola (O(1))."""
        if not isinstance(incident_id, str):
            return False
        return incident_id.strip() in self._posiciones

    def _es_mas_urgente(self, inc1: Incident, inc2: Incident) -> bool:
        """
        Determina si el incidente inc1 es más urgente que inc2.
        
        Criterios:
            1. Mayor prioridad.
            2. Menor timestamp (en caso de empate de prioridad).
        """
        if inc1.prioridad > inc2.prioridad:
            return True
        elif inc1.prioridad < inc2.prioridad:
            return False
        else:
            # Empate: prioriza el que ocurrió antes (menor timestamp)
            return inc1.timestamp < inc2.timestamp

    def _swap(self, i: int, j: int):
        """Intercambia dos elementos en el heap y actualiza sus posiciones en el mapa (O(1))."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._posiciones[self._heap[i].id] = i
        self._posiciones[self._heap[j].id] = j

    def _sift_up(self, idx: int):
        """Desplaza un elemento hacia arriba en el heap para restaurar la propiedad (O(log N))."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._es_mas_urgente(self._heap[idx], self._heap[parent]):
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int):
        """Desplaza un elemento hacia abajo en el heap para restaurar la propiedad (O(log N))."""
        n = len(self._heap)
        while 2 * idx + 1 < n:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = left

            if right < n and self._es_mas_urgente(self._heap[right], self._heap[left]):
                largest = right

            if self._es_mas_urgente(self._heap[largest], self._heap[idx]):
                self._swap(idx, largest)
                idx = largest
            else:
                break

    def insertar(self, incidente: Incident):
        """
        Inserta un incidente en la cola de prioridad.

        Precondiciones:
            - incidente debe ser una instancia válida de la clase Incident.
            - El ID del incidente no debe existir previamente en la cola.

        Postcondiciones:
            - El incidente es almacenado en la posición correcta según su urgencia.
        """
        if not isinstance(incidente, Incident):
            raise ValueError("Solo se pueden insertar instancias de la clase Incident.")
        if incidente.id in self._posiciones:
            raise ValueError(f"El incidente con ID '{incidente.id}' ya se encuentra en la cola de prioridad.")

        self._heap.append(incidente)
        idx = len(self._heap) - 1
        self._posiciones[incidente.id] = idx
        self._sift_up(idx)

    def extraer_urgente(self) -> Incident:
        """
        Remueve y retorna el incidente más urgente (mayor prioridad/menor timestamp).

        Precondiciones:
            - La cola de prioridad no debe estar vacía.

        Postcondiciones:
            - La cola reduce su tamaño en 1.
            - Se reestructura el heap para mantener la propiedad de max-heap.
        """
        if self.esta_vacia():
            raise IndexError("No se puede extraer de una cola de prioridad vacía.")

        self._swap(0, len(self._heap) - 1)
        removido = self._heap.pop()
        del self._posiciones[removido.id]

        if not self.esta_vacia():
            self._posiciones[self._heap[0].id] = 0
            self._sift_down(0)

        return removido

    def actualizar_prioridad(self, incident_id: str, nueva_prioridad: float):
        """
        Actualiza la prioridad de un incidente dentro de la cola en O(log N).

        Precondiciones:
            - incident_id debe ser una cadena no vacía y existir en la cola.
            - nueva_prioridad debe ser un número real no negativo.

        Postcondiciones:
            - La prioridad del incidente es actualizada.
            - El incidente es reordenado (sift-up o sift-down) para mantener el heap válido.
        """
        if not isinstance(incident_id, str) or not incident_id.strip():
            raise ValueError("El ID del incidente debe ser una cadena no vacía.")
        if not isinstance(nueva_prioridad, (int, float)) or nueva_prioridad < 0:
            raise ValueError("La prioridad debe ser un número real no negativo.")

        id_limpio = incident_id.strip()
        if id_limpio not in self._posiciones:
            raise KeyError(f"El incidente '{id_limpio}' no existe en la cola de prioridad.")

        idx = self._posiciones[id_limpio]
        incidente = self._heap[idx]
        prioridad_anterior = incidente.prioridad

        if nueva_prioridad == prioridad_anterior:
            return  # No hay cambios

        incidente.prioridad = nueva_prioridad

        # Como es max-heap, si sube prioridad hacemos sift-up, si baja hacemos sift-down
        if nueva_prioridad > prioridad_anterior:
            self._sift_up(idx)
        else:
            self._sift_down(idx)

    def obtener_top_k(self, k: int) -> list:
        """
        Retorna los Top-K incidentes más críticos en orden descendente, sin modificar la cola actual.

        Precondiciones:
            - k debe ser un entero positivo.

        Postcondiciones:
            - Retorna una lista de tamaño min(k, N) con los incidentes ordenados por urgencia.
        """
        if not isinstance(k, int) or k <= 0:
            raise ValueError("El parámetro K debe ser un entero positivo.")

        # Crear una copia superficial del heap y su mapa de posiciones para no mutar el estado
        temp_pq = PriorityQueue()
        temp_pq._heap = list(self._heap)
        temp_pq._posiciones = dict(self._posiciones)

        resultados = []
        limite = min(k, len(self._heap))
        for _ in range(limite):
            resultados.append(temp_pq.extraer_urgente())

        return resultados


class MinPriorityQueue:
    """
    Cola de Prioridad genérica de Mínimos implementada mediante un Min-Heap binario.
    Almacena elementos como tuplas (prioridad, item) y extrae el menor de forma eficiente en O(log N).
    """

    def __init__(self):
        """Inicializa una cola de prioridad de mínimos vacía."""
        self._heap = []

    def __len__(self) -> int:
        """Retorna la cantidad de elementos en la cola (O(1))."""
        return len(self._heap)

    def esta_vacia(self) -> bool:
        """Verifica si la cola está vacía (O(1))."""
        return len(self._heap) == 0

    def insertar(self, prioridad, item):
        """Inserta un par (prioridad, item) en la cola (O(log N))."""
        self._heap.append((prioridad, item))
        self._sift_up(len(self._heap) - 1)

    def extraer_min(self) -> tuple:
        """Remueve y retorna la tupla (prioridad, item) con menor prioridad (O(log N))."""
        if self.esta_vacia():
            raise IndexError("No se puede extraer de una cola de prioridad vacía.")
        self._swap(0, len(self._heap) - 1)
        removido = self._heap.pop()
        if not self.esta_vacia():
            self._sift_down(0)
        return removido

    def _swap(self, i: int, j: int):
        """Intercambia dos elementos en el heap (O(1))."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, idx: int):
        """Desplaza un elemento hacia arriba en el heap (O(log N))."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx][0] < self._heap[parent][0]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int):
        """Desplaza un elemento hacia abajo en el heap (O(log N))."""
        n = len(self._heap)
        while 2 * idx + 1 < n:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = left

            if right < n and self._heap[right][0] < self._heap[left][0]:
                smallest = right

            if self._heap[smallest][0] < self._heap[idx][0]:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break
