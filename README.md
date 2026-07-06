# Sistema Inteligente de Gestión y Optimización de Rutas de Emergencia

Este es el prototipo de software diseñado para gestionar incidentes, priorizar solicitudes de emergencia, almacenar información de manera eficiente y calcular rutas óptimas en situaciones de desastre natural.

---

## Estado del Proyecto (Partes 1, 2 y 3 Completadas)

Hemos establecido las bases del sistema con los siguientes componentes principales:
* **ADT Incident:** Modelo del incidente con validaciones y control de estados.
* **ADT EmergencyCenter:** Modelo para los centros de operaciones.
* **ADT RoadNetwork:** Modelo de la red vial representado mediante un grafo ponderado con tiempos de desplazamiento.
* **HashTable Personalizada:** Estructura propia para almacenamiento de incidentes que maneja colisiones vía Separate Chaining, redimensionamiento dinámico cuando factor de carga > 0.75, y recolección de estadísticas de colisiones.
* **PriorityQueue (Max-Heap):** Cola de prioridad para gestionar la urgencia de los incidentes en tiempo logarítmico, optimizada con mapeo de posiciones e indexación para actualizaciones eficientes.

---

## Cómo Ejecutar el Proyecto

### 1. Requisitos Previos
* **Versión de Python mínima requerida:** Python 3.8 o superior (antes de ejecutar el programa).
* **Versión de Python en producción:** Python 3.13 (usada para desarrollo y pruebas base).
* **Compatibilidad Multiplataforma:** El programa es compatible y se ejecuta exactamente de la misma forma en los principales sistemas operativos:
  * **Windows 11**
  * **macOS**
  * **Linux**
* **Sin dependencias externas:** Toda la implementación de estructuras es nativa de Python (no requiere instalar librerías de terceros).

### 2. Ejecutar la Demostración Principal
El archivo [main.py](./main.py) contiene un flujo interactivo que crea la red vial, centros de emergencia, inserta un lote de incidentes, actualiza sus estados, simula eliminaciones, ilustra el proceso de redimensionamiento dinámico (*rehash*) e interactúa con la cola de prioridad.

Para ejecutar la demostración, abre la terminal en la raíz del proyecto y corre:
```bash
python main.py
```

### 3. Ejecutar las Pruebas Unitarias
Para verificar el correcto funcionamiento de todas las estructuras de datos y los tipos abstractos de datos implementados, puedes correr la suite de pruebas unitarias de 29 casos mediante el módulo nativo de Python:

```bash
python -m unittest discover -s tests
```

---

## Estructura del Código

* `/models/`: Contiene las clases de los Tipos de Datos Abstractos ([incident.py](./models/incident.py), [center.py](./models/center.py) y [road_network.py](./models/road_network.py)).
* `/structures/`: Contiene las estructuras de datos avanzadas ([hash_table.py](./structures/hash_table.py) y [priority_queue.py](./structures/priority_queue.py)).
* `/tests/`: Suite de pruebas unitarias ([test_structures.py](./tests/test_structures.py), [test_road_network.py](./tests/test_road_network.py) y [test_priority_queue.py](./tests/test_priority_queue.py)).
* [main.py](./main.py): Archivo principal de ejecución de demostraciones.