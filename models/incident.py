class Incident:
    """
    Tipo de Dato Abstracto (ADT) que representa un Incidente de emergencia reportado.

    Atributos:
        id (str): Identificador único del incidente.
        ubicacion (str): Ubicación geográfica (nombre del nodo o zona en el grafo).
        prioridad (float): Nivel de prioridad/urgencia calculado o asignado.
        tipo (str): Tipo de incidente (ej: 'Incendio', 'Accidente', 'Medico').
        timestamp (float): Tiempo de reporte (secuencial o timestamp epoch).
        estado (str): Estado actual ('Pendiente', 'En Proceso', 'Resuelto').

    Complejidades:
        - Crear Incidente: O(1) tiempo, O(1) espacio.
        - Actualizar Estado: O(1) tiempo, O(1) espacio.
    """

    VALID_STATES = {"Pendiente", "En Proceso", "Resuelto"}

    def __init__(self, id_incidente: str, ubicacion: str, prioridad: float, tipo: str, timestamp: float, estado: str = "Pendiente"):
        """
        Constructor del Incidente.

        Precondiciones:
            - id_incidente debe ser una cadena no vacía.
            - ubicacion debe ser una cadena no vacía.
            - prioridad debe ser un número flotante o entero mayor o igual a 0.
            - tipo debe ser una cadena no vacía.
            - timestamp debe ser un número real mayor o igual a 0.
            - estado debe pertenecer a VALID_STATES ('Pendiente', 'En Proceso', 'Resuelto').

        Postcondiciones:
            - Retorna una instancia válida del ADT Incident con los atributos inicializados.
        """
        if not isinstance(id_incidente, str) or not id_incidente.strip():
            raise ValueError("El ID del incidente debe ser una cadena no vacía.")
        if not isinstance(ubicacion, str) or not ubicacion.strip():
            raise ValueError("La ubicación debe ser una cadena no vacía.")
        if not isinstance(prioridad, (int, float)) or prioridad < 0:
            raise ValueError("La prioridad debe ser un número real no negativo.")
        if not isinstance(tipo, str) or not tipo.strip():
            raise ValueError("El tipo de incidente debe ser una cadena no vacía.")
        if not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise ValueError("El timestamp debe ser un número real no negativo.")
        if estado not in self.VALID_STATES:
            raise ValueError(f"Estado inválido. Los estados permitidos son: {self.VALID_STATES}")

        self._id = id_incidente.strip()
        self._ubicacion = ubicacion.strip()
        self._prioridad = float(prioridad)
        self._tipo = tipo.strip()
        self._timestamp = float(timestamp)
        self._estado = estado

    # Getters y Setters
    @property
    def id(self) -> str:
        """Retorna el ID único del incidente (O(1))."""
        return self._id

    @property
    def ubicacion(self) -> str:
        """Retorna la ubicación del incidente (O(1))."""
        return self._ubicacion

    @property
    def prioridad(self) -> float:
        """Retorna la prioridad del incidente (O(1))."""
        return self._prioridad

    @prioridad.setter
    def prioridad(self, nueva_prioridad: float):
        """
        Permite actualizar la prioridad del incidente (O(1)).
        Precondición: nueva_prioridad >= 0
        """
        if not isinstance(nueva_prioridad, (int, float)) or nueva_prioridad < 0:
            raise ValueError("La prioridad debe ser un número real no negativo.")
        self._prioridad = float(nueva_prioridad)

    @property
    def tipo(self) -> str:
        """Retorna el tipo de incidente (O(1))."""
        return self._tipo

    @property
    def timestamp(self) -> float:
        """Retorna el tiempo de reporte del incidente (O(1))."""
        return self._timestamp

    @property
    def estado(self) -> str:
        """Retorna el estado actual del incidente (O(1))."""
        return self._estado

    def actualizar_estado(self, nuevo_estado: str):
        """
        Actualiza el estado del incidente (O(1)).

        Precondición:
            - nuevo_estado debe pertenecer a VALID_STATES.
        Postcondición:
            - El atributo _estado se actualiza al nuevo estado.
        """
        if nuevo_estado not in self.VALID_STATES:
            raise ValueError(f"Estado inválido. Debe ser uno de: {self.VALID_STATES}")
        self._estado = nuevo_estado

    def __repr__(self) -> str:
        return f"Incident(id='{self._id}', ubicacion='{self._ubicacion}', prioridad={self._prioridad}, tipo='{self._tipo}', timestamp={self._timestamp}, estado='{self._estado}')"

    def __str__(self) -> str:
        return f"[{self._id}] Tipo: {self._tipo} | Ubicacion: {self._ubicacion} | Prioridad: {self._prioridad:.2f} | Estado: {self._estado}"
