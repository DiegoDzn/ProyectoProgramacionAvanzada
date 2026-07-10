# Sistema Inteligente de Gestión y Optimización de Rutas de Emergencia

Este es el prototipo de software diseñado para gestionar incidentes, priorizar solicitudes de emergencia, almacenar información de manera eficiente y calcular rutas óptimas en situaciones de desastre natural.

---

## Estado del Proyecto (Partes 1 a 7 Completadas)

Hemos establecido y validado todas las fases del sistema con los siguientes componentes principales:

* **ADT Incident:** Modelo del incidente con validaciones y control de estados.
* **ADT EmergencyCenter:** Modelo para los centros de operaciones.
* **ADT RoadNetwork:** Modelo de la red vial representado mediante un grafo ponderado con tiempos de desplazamiento y coordenadas espaciales `(x, y)` para guiar búsquedas informadas.
* **HashTable Personalizada:** Estructura propia para almacenamiento de incidentes que maneja colisiones vía Separate Chaining, redimensionamiento dinámico cuando factor de carga > 0.75, y recolección de estadísticas de colisiones.
* **PriorityQueue (Max-Heap y Min-Heap):** Cola de prioridad para la urgencia de incidentes en tiempo logarítmico (Max-Heap optimizado con mapa de posiciones) y cola de prioridad genérica de mínimos (Min-Heap) para búsquedas de caminos óptimos. Incluye benchmarks de inserción y extracción.
* **Sorting (MergeSort y QuickSort):** Implementaciones genéricas de ordenación para generar reportes por antigüedad, severidad y frecuencia de incidentes por zona, evaluadas mediante benchmarking de rendimiento.
* **Frecuencia por Zona:** Reporte de zonas con más incidentes ordenado por frecuencia descendente usando MergeSort.
* **Graph Search (BFS, Dijkstra, A\*):** Algoritmos de búsqueda de caminos mínimos implementados desde cero. BFS encuentra el camino de menos tramos, mientras que Dijkstra y A* (asistido por heurística euclidiana) localizan la ruta más rápida.
* **Escenario Integrado & Dataset Generator:** Simulación completa que genera un dataset de 500 incidentes y una red vial de 50 nodos y 121 aristas para realizar el despacho y ruta de vehículos en tiempo real.

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
El archivo `main.py` contiene un flujo interactivo que ilustra los pasos del 1 al 11 del proyecto. Generará automáticamente los archivos de prueba `incidentes.csv` (500 incidentes) y `red_vial.json` (50 nodos, 121 aristas) en caso de que no existan en la raíz.

Para ejecutar la demostración, abre la terminal en la raíz del proyecto y corre:
```bash
python main.py
```

### 3. Ejecutar las Pruebas Unitarias
Para verificar el correcto funcionamiento de todas las estructuras de datos y los tipos abstractos de datos implementados, puedes correr la suite de pruebas unitarias de 41 casos mediante el módulo nativo de Python:

```bash
python -m unittest discover -s tests
```

---

## Estructura del Código

* `/models/`: Contiene las clases de los Tipos de Datos Abstractos ([incident.py](./models/incident.py), [center.py](./models/center.py) y [road_network.py](./models/road_network.py)).
* `/structures/`: Contiene las estructuras de datos avanzadas ([hash_table.py](./structures/hash_table.py), [priority_queue.py](./structures/priority_queue.py), [sorting.py](./structures/sorting.py) y [graph_search.py](./structures/graph_search.py)).
* `/tests/`: Suite de pruebas unitarias ([test_structures.py](./tests/test_structures.py), [test_road_network.py](./tests/test_road_network.py), [test_priority_queue.py](./tests/test_priority_queue.py), [test_sorting.py](./tests/test_sorting.py) y [test_search.py](./tests/test_search.py)).
* [main.py](./main.py): Archivo principal de ejecución de demostraciones.
* [data_generator.py](./data_generator.py): Generador de datasets para la simulación integrada.