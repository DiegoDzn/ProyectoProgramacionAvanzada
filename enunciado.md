Proyecto Integrador Final

### Sistema Inteligente de Gestión y Optimización de Rutas de Emergencia


### Contexto
Durante un desastre natural, los centros de emergencia reciben numerosas solicitudes de ayuda. Los equipos de respuesta deben priorizar incidentes y encontrar rutas eficientes para atenderlos. El objetivo es desarrollar un sistema que apoye la toma de decisiones en situaciones de emergencia.

**Cada solicitud posee**:
- Un identificador único.
- Ubicación geográfica.
- Nivel de prioridad.
- Tipo de incidente.
- Tiempo de reporte.

Los equipos de respuesta (ambulancias, brigadas, bomberos, vehículos de rescate, etc.) deben ser asignados eficientemente a los incidentes más críticos y encontrar rutas adecuadas para llegar a los lugares afectados.

La información cambia constantemente y debe ser procesada en tiempo real.

Su equipo ha sido contratado para desarrollar un prototipo de software que permita gestionar incidentes y apoyar la toma de decisiones durante una emergencia.


### Objetivo
Diseñar e implementar un sistema que permita registrar incidentes, priorizarlos, almacenarlos eficientemente, analizar información operacional y calcular rutas óptimas para la atención de emergencias.

1. Registrar y gestionar incidentes.
2. Priorizar solicitudes de emergencia.
3. Mantener información eficiente de acceso rápido.
4. Analizar zonas afectadas.
5. Calcular rutas entre centros de operación y puntos de emergencia.
6. Generar reportes y estadísticas.

# Requerimientos del Sistema

## Parte 1 – Modelo de Datos (ADT)
Diseñar los ADT Incident, EmergencyCenter y RoadNetwork, documentando operaciones, precondiciones, postcondiciones y complejidades.

### Incident
Representa un incidente reportado.

**Atributos mínimos:** id, ubicacion, prioridad, tipo, timestamp, estado

---
### EmergencyCenter
Representa un centro de operaciones.

id, nombre, ubicacion

---
### RoadNetwork
Representa la red vial.

Debe modelarse como un grafo.


## Parte 2 – Hashing
Implementar una tabla hash propia para almacenar incidentes y soportar inserción, búsqueda, actualización y eliminación. Incluir métricas de colisiones y factor de carga.

**El sistema deberá permitir:**
### Operaciones
- Insertar incidente
- Buscar incidente por ID
- Actualizar estado
- Eliminar incidente
- Obtener estadísticas
- Debe desarrollarse una tabla hash propia.(NO USAR DICT, en python)

### Métricas
**Registrar:**
- Factor de carga
- Colisiones
- Buckets utilizados
- Máximo tamaño de bucket

## Parte 3 – Heap y Priority Queue
Implementar una Priority Queue basada en Heap para gestionar incidentes según su prioridad.

Los incidentes deben ser gestionados mediante una cola de prioridad.

La prioridad puede calcularse usando:

prioridad = severidad × factor_tiempo

o alguna fórmula equivalente.

### Funcionalidades
- Insertar incidente
- Extraer incidente más urgente
- Actualizar prioridad
- Mostrar Top-K incidentes críticos

## Parte 4 – Sorting
Implementar al menos dos algoritmos de ordenamiento y comparar su rendimiento mediante experimentación.

El sistema deberá generar reportes ordenados.

Ejemplos:

### Incidentes más antiguos
Ordenados por tiempo.

### Incidentes más críticos
Ordenados por prioridad.

### Zonas con más incidentes
Ordenadas por frecuencia.

### Requisito
Implementar al menos dos algoritmos de ordenamiento:

- MergeSort
- QuickSort
o equivalentes.


## Parte 5 – Grafos
Modelar la red vial mediante un grafo con nodos y aristas ponderadas.


### Nodos
Intersecciones o localidades.

### Aristas
Caminos entre nodos.

### Peso
Tiempo de desplazamiento.

Ejemplo:

Centro_A --10--> Zona_1\
Centro_A --15--> Zona_2\
Zona_1   --5--> Zona_3


El grafo podrá cargarse desde:

- CSV
- JSON
- Datos definidos en código

## Parte 6 – Algoritmos de Búsqueda
Implementar BFS y UCS/Dijkstra de forma obligatoria. A* puede implementarse como extensión opcional.

Implementar al menos dos algoritmos:

### Obligatorios
- BFS
- UCS (o Dijkstra)
### Opcional (+ bono)
- A*

El sistema deberá responder preguntas como:

¿Cuál es la ruta más rápida desde el Centro de Emergencia Norte hasta el incidente I-152?

Mostrar:

- Nodos visitados
- Ruta encontrada
- Distancia total
- Costo acumulado

## Parte 7 – Escenario Integrado
Leer incidentes, almacenarlos en las estructuras desarrolladas, seleccionar el incidente más urgente y calcular la mejor ruta disponible.

El sistema deberá ser capaz de ejecutar el siguiente flujo:

### Paso 1
**Leer:** incidentes.csv

### Paso 2
Insertar los incidentes en:
- Tabla Hash
- Priority Queue

### Paso 3
Extraer el incidente más urgente.

### Paso 4
Buscar la ruta óptima desde el centro de emergencia más cercano.

### Paso 5
**Mostrar:** Incidente asignado, Prioridad, Ruta sugerida, Costo total, Tiempo estimado



### Dataset mínimo
Al menos 500 incidentes y una red vial con 50 nodos y 100 aristas.

Se deberá generar: **500 incidentes** como mínimo.

**Cada incidente debe incluir:** ID, Zona, Prioridad, Tipo, Fecha


### Grafo
**Al menos:** 50 nodos, 100 aristas

### Análisis Experimental
Comparar el desempeño de las estructuras y algoritmos implementados.

## Análisis Experimental
El informe deberá incluir:

### Hashing
Colisiones
Factor de carga
Rendimiento

### Heap
Tiempo inserción
Tiempo extracción

### Sorting
Comparación entre algoritmos.


### Grafos
Comparación de rutas encontradas.

## Entregables
Repositorio GitHub, informe técnico de 5 a 10 páginas, evidencias de ejecución y video opcional.

## Conceptos Integrados
ADT, estructuras de datos, hashing, heaps, priority queues, sorting, grafos, BFS, UCS/Dijkstra, A* y análisis de complejidad.

## Informe Técnico (5–10 páginas)
Debe incluir:
- Diseño ADT
- Diagramas
- Complejidades
- Resultados experimentales
- Discusión

## Video (opcional)
5 minutos mostrando el sistema.