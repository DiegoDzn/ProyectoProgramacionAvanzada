class RoadNetwork:
    """
    Tipo de Dato Abstracto (ADT) que representa la Red Vial como un Grafo Ponderado.

    Permite modelar intersecciones o localidades como nodos y las calles o rutas
    entre ellas como aristas ponderadas con el tiempo de desplazamiento.

    Complejidades:
        - Agregar Nodo: O(1) promedio de tiempo, O(1) de espacio.
        - Agregar Arista: O(1) promedio de tiempo, O(1) de espacio.
        - Obtener Nodos: O(V) tiempo, O(V) espacio.
        - Obtener Adyacentes: O(1) tiempo promedio, O(deg(V)) para retornar/copiar.
        - Obtener Peso: O(1) promedio de tiempo, O(1) espacio.
        - Existe Nodo: O(1) promedio de tiempo, O(1) espacio.
        - Existe Arista: O(1) promedio de tiempo, O(1) espacio.
    """

    def __init__(self):
        """
        Constructor del ADT RoadNetwork.

        Precondiciones:
            - Ninguna.

        Postcondiciones:
            - Retorna una instancia vacía de RoadNetwork con la lista de adyacencia inicializada.
        """
        # Estructura interna: dict que asocia cada nodo con otro dict de {destino: peso}
        self._adjacency_list = {}

    def agregar_nodo(self, nodo: str):
        """
        Agrega una intersección o localidad (nodo) a la red vial.

        Precondiciones:
            - nodo debe ser una cadena de texto no vacía.

        Postcondiciones:
            - El nodo es registrado en la red vial. Si ya existía, no produce ningún cambio.
        """
        if not isinstance(nodo, str) or not nodo.strip():
            raise ValueError("El nombre del nodo debe ser una cadena no vacía.")

        nodo_limpio = nodo.strip()
        if nodo_limpio not in self._adjacency_list:
            self._adjacency_list[nodo_limpio] = {}

    def agregar_arista(self, origen: str, destino: str, peso: float, bidireccional: bool = True):
        """
        Agrega o actualiza una ruta (arista ponderada) entre dos nodos de la red vial.

        Precondiciones:
            - origen y destino deben ser cadenas de texto no vacías.
            - origen y destino ya deben estar registrados como nodos en la red.
            - peso (tiempo de desplazamiento) debe ser un número real o entero no negativo.

        Postcondiciones:
            - Se registra la arista de origen a destino con el peso correspondiente.
            - Si bidireccional es True, también se registra la arista de destino a origen.
        """
        if not isinstance(origen, str) or not origen.strip():
            raise ValueError("El nodo de origen debe ser una cadena no vacía.")
        if not isinstance(destino, str) or not destino.strip():
            raise ValueError("El nodo de destino debe ser una cadena no vacía.")
        if not isinstance(peso, (int, float)) or peso < 0:
            raise ValueError("El peso debe ser un número real o entero no negativo.")

        origen_limpio = origen.strip()
        destino_limpio = destino.strip()

        if origen_limpio not in self._adjacency_list:
            raise ValueError(f"El nodo de origen '{origen_limpio}' no existe en la red vial.")
        if destino_limpio not in self._adjacency_list:
            raise ValueError(f"El nodo de destino '{destino_limpio}' no existe en la red vial.")

        self._adjacency_list[origen_limpio][destino_limpio] = float(peso)
        if bidireccional:
            self._adjacency_list[destino_limpio][origen_limpio] = float(peso)

    def obtener_nodos(self) -> list:
        """
        Retorna una lista con todos los nodos registrados en la red vial.

        Precondiciones:
            - Ninguna.

        Postcondiciones:
            - Retorna una lista conteniendo los nombres de todos los nodos.
        """
        return list(self._adjacency_list.keys())

    def obtener_adyacentes(self, nodo: str) -> dict:
        """
        Retorna las conexiones adyacentes de un nodo dado y sus respectivos pesos.

        Precondiciones:
            - nodo debe ser una cadena de texto no vacía y existir en la red vial.

        Postcondiciones:
            - Retorna una copia del diccionario interno de adyacencia para el nodo dado.
        """
        if not isinstance(nodo, str) or not nodo.strip():
            raise ValueError("El nombre del nodo debe ser una cadena no vacía.")

        nodo_limpio = nodo.strip()
        if nodo_limpio not in self._adjacency_list:
            raise ValueError(f"El nodo '{nodo_limpio}' no existe en la red vial.")

        # Retornamos copia para proteger la encapsulación
        return dict(self._adjacency_list[nodo_limpio])

    def obtener_peso(self, origen: str, destino: str) -> float:
        """
        Retorna el peso (tiempo de desplazamiento) de la arista entre origen y destino.

        Precondiciones:
            - origen y destino deben ser cadenas de texto no vacías y existir en la red.
            - Debe existir una arista directa entre origen y destino.

        Postcondiciones:
            - Retorna el peso como float.
        """
        if not isinstance(origen, str) or not origen.strip():
            raise ValueError("El nodo de origen debe ser una cadena no vacía.")
        if not isinstance(destino, str) or not destino.strip():
            raise ValueError("El nodo de destino debe ser una cadena no vacía.")

        origen_limpio = origen.strip()
        destino_limpio = destino.strip()

        if origen_limpio not in self._adjacency_list:
            raise ValueError(f"El nodo de origen '{origen_limpio}' no existe en la red vial.")
        if destino_limpio not in self._adjacency_list[origen_limpio]:
            raise ValueError(f"No existe una arista directa desde '{origen_limpio}' hacia '{destino_limpio}'.")

        return self._adjacency_list[origen_limpio][destino_limpio]

    def existe_nodo(self, nodo: str) -> bool:
        """
        Verifica si un nodo existe en la red vial.

        Precondiciones:
            - Ninguna.

        Postcondiciones:
            - Retorna True si el nodo existe, False en caso contrario.
        """
        if not isinstance(nodo, str):
            return False
        return nodo.strip() in self._adjacency_list

    def existe_arista(self, origen: str, destino: str) -> bool:
        """
        Verifica si existe una arista directa entre origen y destino.

        Precondiciones:
            - Ninguna.

        Postcondiciones:
            - Retorna True si existe la conexión directa de origen a destino, False en caso contrario.
        """
        if not isinstance(origen, str) or not isinstance(destino, str):
            return False

        origen_limpio = origen.strip()
        destino_limpio = destino.strip()

        if origen_limpio not in self._adjacency_list:
            return False

        return destino_limpio in self._adjacency_list[origen_limpio]

    def __repr__(self) -> str:
        return f"RoadNetwork(nodos={len(self._adjacency_list)})"

    def __str__(self) -> str:
        res = ["Red Vial (RoadNetwork):"]
        for nodo, adyacentes in self._adjacency_list.items():
            conexiones = ", ".join(f"-> {dest} ({peso:.1f})" for dest, peso in adyacentes.items())
            res.append(f"  {nodo}: [{conexiones}]" if conexiones else f"  {nodo}: [Sin conexiones]")
        return "\n".join(res)
