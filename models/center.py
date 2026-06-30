class EmergencyCenter:
    """
    Tipo de Dato Abstracto (ADT) que representa un Centro de Emergencia (ej. hospital, bomberos).

    Atributos:
        id (str): Identificador único del centro de emergencias.
        nombre (str): Nombre descriptivo del centro.
        ubicacion (str): Ubicación geográfica (nombre del nodo en el grafo).

    Complejidades:
        - Crear Centro: O(1) tiempo, O(1) espacio.
    """

    def __init__(self, id_centro: str, nombre: str, ubicacion: str):
        """
        Constructor del Centro de Emergencia.

        Precondiciones:
            - id_centro debe ser una cadena no vacía.
            - nombre debe ser una cadena no vacía.
            - ubicacion debe ser una cadena no vacía.

        Postcondiciones:
            - Retorna una instancia del ADT EmergencyCenter con los atributos inicializados.
        """
        if not isinstance(id_centro, str) or not id_centro.strip():
            raise ValueError("El ID del centro debe ser una cadena no vacía.")
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        if not isinstance(ubicacion, str) or not ubicacion.strip():
            raise ValueError("La ubicación debe ser una cadena no vacía.")

        self._id = id_centro.strip()
        self._nombre = nombre.strip()
        self._ubicacion = ubicacion.strip()

    # Getters
    @property
    def id(self) -> str:
        """Retorna el ID del centro (O(1))."""
        return self._id

    @property
    def nombre(self) -> str:
        """Retorna el nombre del centro (O(1))."""
        return self._nombre

    @property
    def ubicacion(self) -> str:
        """Retorna la ubicación del centro (O(1))."""
        return self._ubicacion

    def __repr__(self) -> str:
        return f"EmergencyCenter(id='{self._id}', nombre='{self._nombre}', ubicacion='{self._ubicacion}')"

    def __str__(self) -> str:
        return f"Centro [{self._id}] {self._nombre} en {self._ubicacion}"
