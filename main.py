import time
import random
import os
from data_generator import verificar_y_generar_datos
from models.incident import Incident
from models.center import EmergencyCenter
from models.road_network import RoadNetwork
from structures.hash_table import HashTable
from structures.priority_queue import PriorityQueue
from structures.sorting import merge_sort, quick_sort
from structures.graph_search import bfs, dijkstra, a_star




def mostrar_estadisticas_tabla(tabla: HashTable, titulo: str):
    """Muestra de manera formateada las estadísticas de la HashTable."""
    stats = tabla.get_stats()
    print("-" * 50)
    print(f" METRICAS DE LA TABLA HASH: {titulo}")
    print("-" * 50)
    print(f" Capacidad de la Tabla (M)  : {stats['capacity']}")
    print(f" Elementos Almacenados (N) : {stats['size']}")
    print(f" Factor de Carga (N/M)     : {stats['load_factor']:.4f}")
    print(f" Total de Colisiones       : {stats['collisions']}")
    print(f" Buckets Utilizados        : {stats['buckets_used']}")
    print(f" Tamaño Máximo de Bucket   : {stats['max_bucket_size']}")
    print("-" * 50)
    print()


def main():
    print("=" * 60)
    print("   SISTEMA INTELIGENTE DE GESTIÓN DE EMERGENCIAS (Fase 1)")
    print("=" * 60)
    print()

    # 1. Inicialización de la Red Vial (ADT RoadNetwork - Completa la Parte 1)
    print("[1] Inicializando la Red Vial (RoadNetwork)...")
    red_vial = RoadNetwork()
    
    # Agregar nodos (intersecciones y zonas)
    nodos_sistema = [
        "Interseccion_A", "Interseccion_B", "Interseccion_C", 
        "Interseccion_D", "Interseccion_E", "Interseccion_F", 
        "Zona_1", "Zona_2", "Zona_3", "Zona_4"
    ]
    for nodo in nodos_sistema:
        red_vial.agregar_nodo(nodo)
        
    # Agregar aristas con pesos (tiempos de desplazamiento en minutos)
    red_vial.agregar_arista("Interseccion_A", "Zona_1", 10.0, bidireccional=True)
    red_vial.agregar_arista("Interseccion_A", "Zona_2", 15.0, bidireccional=True)
    red_vial.agregar_arista("Zona_1", "Zona_3", 5.0, bidireccional=True)
    red_vial.agregar_arista("Zona_2", "Interseccion_C", 8.0, bidireccional=True)
    red_vial.agregar_arista("Interseccion_C", "Zona_4", 12.0, bidireccional=True)
    red_vial.agregar_arista("Zona_3", "Interseccion_F", 7.0, bidireccional=True)
    red_vial.agregar_arista("Zona_4", "Interseccion_F", 4.0, bidireccional=True)
    
    print("  -> Red Vial creada exitosamente:")
    print(red_vial)
    print()

    # 2. Inicialización de Centros de Emergencia (ADTs)
    print("[2] Inicializando Centros de Emergencia...")
    centro_norte = EmergencyCenter("EC-01", "Centro de Emergencia Norte", "Interseccion_A")
    centro_sur = EmergencyCenter("EC-02", "Centro de Emergencia Sur", "Interseccion_F")
    print(f"  -> Creado: {centro_norte}")
    print(f"  -> Creado: {centro_sur}")
    print()

    # 3. Inicialización de la HashTable para Incidentes (Parte 2)
    # Elegimos una capacidad pequeña para observar colisiones de forma controlada
    print("[3] Creando Tabla Hash propia para Incidentes...")
    tabla_incidentes = HashTable(initial_capacity=13)
    mostrar_estadisticas_tabla(tabla_incidentes, "Inicial")

    # 4. Creación e Inserción de Incidentes de Prueba (Parte 2)
    print("[4] Creando e insertando Incidentes en la Tabla Hash...")
    incidentes_demo = [
        Incident("I-152", "Zona_1", 8.5, "Incendio", time.time()),
        Incident("I-102", "Zona_2", 3.0, "Accidente Vial", time.time()),
        Incident("I-305", "Zona_1", 9.2, "Emergencia Medica", time.time()),
        Incident("I-204", "Zona_3", 5.5, "Derrumbe", time.time()),
        Incident("I-110", "Zona_2", 2.1, "Inundacion", time.time()),
        Incident("I-099", "Zona_4", 7.0, "Incendio", time.time()),
        Incident("I-180", "Zona_1", 4.0, "Accidente Vial", time.time()),
        Incident("I-210", "Zona_3", 6.8, "Rescate", time.time()),
        Incident("I-412", "Zona_4", 9.9, "Emergencia Medica", time.time()),
        Incident("I-050", "Zona_2", 1.5, "Fuga de Gas", time.time()),
    ]

    for inc in incidentes_demo:
        tabla_incidentes.insert(inc.id, inc)
        print(f"  + Insertado: {inc}")

    print()
    mostrar_estadisticas_tabla(tabla_incidentes, "Lote Inicial Insertado")

    # 5. Búsqueda y Actualización de un Incidente (Parte 2)
    print("[5] Buscando y actualizando incidentes...")
    try:
        id_busqueda = "I-152"
        incidente_recuperado: Incident = tabla_incidentes.get(id_busqueda)
        print(f"  -> Encontrado: {incidente_recuperado}")
        
        print(f"  * Actualizando estado del incidente {id_busqueda} a 'En Proceso'...")
        incidente_recuperado.actualizar_estado("En Proceso")
        
        # Verificar que el cambio se refleja al volver a buscar
        incidente_verificar = tabla_incidentes.get(id_busqueda)
        print(f"  -> Estado actualizado en la tabla: {incidente_verificar}")
    except KeyError as e:
        print(f"  Error: {e}")
    print()

    # 6. Demostración de Eliminación (Parte 2)
    id_eliminar = "I-110"
    print(f"[6] Eliminando incidente {id_eliminar}...")
    if id_eliminar in tabla_incidentes:
        tabla_incidentes.delete(id_eliminar)
        print(f"  - Incidente {id_eliminar} eliminado con éxito.")
        print(f"  - ¿Existe en la tabla?: {id_eliminar in tabla_incidentes}")
    else:
        print(f"  El incidente {id_eliminar} no existe.")

    print()
    mostrar_estadisticas_tabla(tabla_incidentes, "Post-Eliminación")

    # 7. Demostración de Redimensionamiento Automático (Rehash) (Parte 2)
    # Insertaremos más incidentes para sobrepasar el factor de carga de 0.75
    # Capacidad actual es 13 (primo inicial). El rehash ocurre cuando load_factor > 0.75 (N > 9)
    # Actualmente tenemos 9 elementos. Insertar uno más forzará el rehash.
    print("[7] Forzando el redimensionamiento dinámico (Rehash)...")
    incidente_rehash = Incident("I-999", "Zona_Especial", 10.0, "Explosion", time.time())
    print(f"  * Insertando incidente adicional: {incidente_rehash}")
    tabla_incidentes.insert(incidente_rehash.id, incidente_rehash)

    mostrar_estadisticas_tabla(tabla_incidentes, "Post-Rehash")

    # 8. Demostración de Cola de Prioridad y Heap (Parte 3)
    print("[8] Inicializando Cola de Prioridad (PriorityQueue) y poblando con incidentes...")
    cola_prioridad = PriorityQueue()
    
    # Insertar los incidentes activos en la cola de prioridad (excluyendo el eliminado)
    for inc in incidentes_demo:
        if inc.id != "I-110":
            cola_prioridad.insertar(inc)
    cola_prioridad.insertar(incidente_rehash)
    
    print(f"  -> Cola de prioridad poblada con {len(cola_prioridad)} incidentes.")
    print()
    
    # Mostrar Top-3 incidentes críticos
    print("  * Consultando el Top-3 de incidentes críticos en la cola:")
    top_3 = cola_prioridad.obtener_top_k(3)
    for i, inc in enumerate(top_3, 1):
        print(f"    {i}. {inc}")
    print()

    # Actualizar prioridad en O(log N)
    id_actualizar = "I-102"  # Originalmente prioridad 3.0
    print(f"  * Actualizando la prioridad del incidente {id_actualizar} de 3.0 a 12.0 (máxima urgencia)...")
    cola_prioridad.actualizar_prioridad(id_actualizar, 12.0)
    
    # Volver a consultar Top-3 para ver si cambió
    print("  * Consultando nuevamente el Top-3 de incidentes críticos:")
    top_3_nuevo = cola_prioridad.obtener_top_k(3)
    for i, inc in enumerate(top_3_nuevo, 1):
        print(f"    {i}. {inc}")
    print()
    
    # Extraer el incidente más urgente
    urgente = cola_prioridad.extraer_urgente()
    print(f"  -> Incidente extraído (más urgente): {urgente}")
    print(f"  -> Tamaño actual de la cola de prioridad: {len(cola_prioridad)}")
    print()

    # 9. Demostración de Ordenamiento y Reportes (Parte 4)
    print("[9] Generando Reportes Ordenados mediante MergeSort y QuickSort...")
    
    # Recolectamos todos los incidentes activos (excluyendo el eliminado I-110)
    incidentes_activos = [inc for inc in incidentes_demo if inc.id != "I-110"]
    # Agregamos también el incidente de rehash
    incidentes_activos.append(incidente_rehash)
    
    # Reporte A: Incidentes más antiguos (ordenados de forma ascendente por timestamp)
    print("  * Reporte A: Incidentes más antiguos (MergeSort por timestamp - ascendente):")
    reporte_antiguos = merge_sort(incidentes_activos, key=lambda x: x.timestamp)
    for i, inc in enumerate(reporte_antiguos, 1):
        print(f"    {i}. ID: {inc.id} | Tipo: {inc.tipo:<18} | Reportado: {time.strftime('%H:%M:%S', time.localtime(inc.timestamp))}")
    print()
    
    # Reporte B: Incidentes más críticos (ordenados de forma descendente por prioridad)
    print("  * Reporte B: Incidentes más críticos (QuickSort por prioridad - descendente):")
    reporte_criticos = quick_sort(incidentes_activos, key=lambda x: x.prioridad, reverse=True)
    for i, inc in enumerate(reporte_criticos, 1):
        print(f"    {i}. ID: {inc.id} | Tipo: {inc.tipo:<18} | Prioridad: {inc.prioridad:.2f}")
    print()
    
    # Reporte C: Zonas con más incidentes (ordenadas por frecuencia descendente)
    print("  * Reporte C: Zonas con más incidentes (MergeSort por frecuencia - descendente):")
    frecuencias = {}
    for inc in incidentes_activos:
        frecuencias[inc.ubicacion] = frecuencias.get(inc.ubicacion, 0) + 1
    lista_frecuencias = list(frecuencias.items())
    reporte_zonas = merge_sort(lista_frecuencias, key=lambda x: x[1], reverse=True)
    for i, (zona, freq) in enumerate(reporte_zonas, 1):
        print(f"    {i}. Zona: {zona:<15} | Incidentes reportados: {freq}")
    print()

    # 10. Análisis Experimental Comparativo (Parte 4)
    print("[10] Iniciando Análisis Experimental de Algoritmos de Ordenamiento...")
    ejecutar_benchmarks()
    print()

    # 11. Escenario Integrado (Parte 7)
    print("[11] Iniciando Escenario Integrado de Emergencia...")
    # Asegurar que existan los archivos de datos
    verificar_y_generar_datos()
    
    # A. Carga de la Red Vial Completa (Parte 5)
    print("  * Cargando Red Vial desde 'red_vial.json'...")
    red_vial_completa = RoadNetwork()
    red_vial_completa.cargar_desde_json("red_vial.json")
    print(f"    -> Cargado: {len(red_vial_completa.obtener_nodos())} nodos y 121 aristas ponderadas con coordenadas.")
    
    # Inicialización de Centros de Emergencia en la Red Vial
    centro_a_id, centro_a_nodo = "EC-01", "Nodo_0_0"  # Extremo Superior Izquierdo de la cuadrícula
    centro_b_id, centro_b_nodo = "EC-02", "Nodo_4_9"  # Extremo Inferior Derecho de la cuadrícula
    centro_a = EmergencyCenter(centro_a_id, "Centro de Emergencia Norte", centro_a_nodo)
    centro_b = EmergencyCenter(centro_b_id, "Centro de Emergencia Sur", centro_b_nodo)
    print(f"    -> Centros Operacionales: {centro_a} y {centro_b}")
    
    # B. Carga de Incidentes desde CSV (Parte 7)
    print("  * Cargando 500 incidentes desde 'incidentes.csv'...")
    tabla_completa = HashTable(initial_capacity=500)
    cola_completa = PriorityQueue()
    
    with open("incidentes.csv", "r", encoding="utf-8") as f:
        lineas = f.readlines()
        
    for line in lineas[1:]:  # Omitir cabecera
        parts = line.strip().split(",")
        if len(parts) >= 5:
            inc_id = parts[0]
            zona = parts[1]
            prioridad = float(parts[2])
            tipo = parts[3]
            timestamp = float(parts[4])
            inc = Incident(inc_id, zona, prioridad, tipo, timestamp)
            
            # Almacenar en ambas estructuras
            tabla_completa.insert(inc_id, inc)
            cola_completa.insertar(inc)
            
    print(f"    -> Tabla Hash: {tabla_completa.size} incidentes almacenados.")
    print(f"    -> Cola de Prioridad: {len(cola_completa)} incidentes almacenados.")
    
    # C. Extraer el Incidente Más Urgente
    urgente = cola_completa.extraer_urgente()
    print(f"  -> Incidente extraído por urgencia: {urgente}")
    
    # D. Buscar la ruta óptima desde el centro de emergencia más cercano (Parte 7)
    print(f"  * Buscando el Centro de Emergencia más cercano a la zona del incidente '{urgente.ubicacion}'...")
    
    # Calcular la ruta más rápida con Dijkstra desde ambos centros
    res_centro_a = dijkstra(red_vial_completa, centro_a_nodo, urgente.ubicacion)
    res_centro_b = dijkstra(red_vial_completa, centro_b_nodo, urgente.ubicacion)
    
    # Seleccionar el centro más cercano
    if res_centro_a["costo"] <= res_centro_b["costo"]:
        centro_seleccionado = centro_a
        nodo_inicio = centro_a_nodo
        ruta_op = res_centro_a
        print(f"    -> Centro asignado: {centro_a.nombre} (Costo: {res_centro_a['costo']:.2f} min)")
    else:
        centro_seleccionado = centro_b
        nodo_inicio = centro_b_nodo
        ruta_op = res_centro_b
        print(f"    -> Centro asignado: {centro_b.nombre} (Costo: {res_centro_b['costo']:.2f} min)")
        
    print(f"    -> Ruta sugerida: {' -> '.join(ruta_op['ruta'])}")
    print(f"    -> Tiempo estimado de llegada: {ruta_op['costo']:.2f} minutos.")
    print()

    # E. Análisis Experimental de Algoritmos de Búsqueda (Parte 7)
    print("  * Análisis Experimental de Algoritmos de Búsqueda (BFS vs Dijkstra vs A*):")
    # Ejecutamos las tres búsquedas para el mismo par origen-destino
    res_bfs = bfs(red_vial_completa, nodo_inicio, urgente.ubicacion)
    res_dijkstra = dijkstra(red_vial_completa, nodo_inicio, urgente.ubicacion)
    res_astar = a_star(red_vial_completa, nodo_inicio, urgente.ubicacion)
    
    print("-" * 75)
    print(f"{'Algoritmo':<15} | {'Nodos Visitados':<18} | {'Costo Total (min)':<18} | {'Cantidad de Hops':<12}")
    print("-" * 75)
    print(f"{'BFS':<15} | {len(res_bfs['visitados']):<18} | {res_bfs['costo']:<18} | {len(res_bfs['ruta']) - 1:<12}")
    print(f"{'Dijkstra':<15} | {len(res_dijkstra['visitados']):<18} | {res_dijkstra['costo']:<18} | {len(res_dijkstra['ruta']) - 1:<12}")
    print(f"{'A* (Euc.)':<15} | {len(res_astar['visitados']):<18} | {res_astar['costo']:<18} | {len(res_astar['ruta']) - 1:<12}")
    print("-" * 75)
    print()
    print("  [Interpretación]:")
    print("  - BFS encuentra la ruta con menor número de hops, pero ignora el tiempo real (costo).")
    print("  - Dijkstra garantiza el menor tiempo real de viaje, pero explora un espacio de búsqueda grande.")
    print("  - A* utiliza la heurística de distancia para guiar el camino de forma óptima, logrando")
    print("    el mismo tiempo de llegada de Dijkstra pero visitando significativamente menos nodos.")
    print()
    print("Fase de demostraciones completada con éxito.")
    print()



def ejecutar_benchmarks():
    """Ejecuta una serie de experimentos comparativos entre MergeSort y QuickSort."""
    print("-" * 75)
    print(f"{'Tamaño (N)':<12} | {'Caso':<15} | {'MergeSort (s)':<18} | {'QuickSort (s)':<18}")
    print("-" * 75)
    
    tamanos = [100, 500, 1000]
    # Usar semilla para reproducibilidad
    random.seed(42)
    
    for N in tamanos:
        for caso in ["Aleatorio", "Ordenado", "Inverso"]:
            if caso == "Aleatorio":
                data = [random.randint(1, 100000) for _ in range(N)]
            elif caso == "Ordenado":
                data = list(range(N))
            else:
                data = list(range(N, 0, -1))
            
            # Benchmark MergeSort
            t_merge_acum = 0.0
            for _ in range(3): # Promedio de 3 corridas
                data_copy = list(data)
                inicio = time.perf_counter()
                merge_sort(data_copy)
                t_merge_acum += (time.perf_counter() - inicio)
            t_merge_prom = t_merge_acum / 3.0
            
            # Benchmark QuickSort
            t_quick_acum = 0.0
            for _ in range(3): # Promedio de 3 corridas
                data_copy = list(data)
                inicio = time.perf_counter()
                quick_sort(data_copy)
                t_quick_acum += (time.perf_counter() - inicio)
            t_quick_prom = t_quick_acum / 3.0
            
            print(f"{N:<12} | {caso:<15} | {t_merge_prom:16.6f}s | {t_quick_prom:16.6f}s")
    print("-" * 75)
    print()



if __name__ == '__main__':
    main()
