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


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Espera a que el usuario presione Enter para continuar."""
    input("\nPresione [Enter] para volver al menú principal...")


def imprimir_lento(texto: str, delay: float = 0.015):
    """Imprime el texto letra por letra para simular teletipo."""
    for char in texto:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def animar_calculo(mensaje: str, pasos: int = 4):
    """Muestra una animación simple de carga en la terminal."""
    print("  ", end="", flush=True)
    for i in range(pasos):
        print(f"\r  [PROCESSING] {mensaje}" + "." * (i + 1), end="", flush=True)
        time.sleep(0.4)
    print(f"\r  [SUCCESS] {mensaje}... OK       \n")


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


def ejecutar_demostracion_adts_estructuras():
    """Ejecuta demostraciones de verificación interna para los ADTs, HashTable y PriorityQueue."""
    print("[STEP 1/4] VERIFICACION INTERNA DE ADTs Y ESTRUCTURAS")
    print("=" * 70)
    
    # 1. Red Vial Básica
    red_vial = RoadNetwork()
    nodos_sistema = ["Interseccion_A", "Interseccion_B", "Interseccion_C", "Zona_1", "Zona_2"]
    for nodo in nodos_sistema:
        red_vial.agregar_nodo(nodo)
    red_vial.agregar_arista("Interseccion_A", "Zona_1", 10.0, bidireccional=True)
    red_vial.agregar_arista("Interseccion_A", "Zona_2", 15.0, bidireccional=True)
    
    print("[OK] ADT RoadNetwork inicializado con exito.")
    
    # 2. Centros de Emergencia
    centro_norte = EmergencyCenter("EC-01", "Centro de Emergencia Norte", "Interseccion_A")
    print(f"[OK] ADT EmergencyCenter inicializado: {centro_norte.nombre} en {centro_norte.ubicacion}")
    
    # 3. HashTable
    tabla_incidentes = HashTable(initial_capacity=13)
    inc_demo = Incident("I-152", "Zona_1", 8.5, "Incendio", time.time())
    tabla_incidentes.insert(inc_demo.id, inc_demo)
    print(f"[OK] HashTable funcional. Elemento I-152 insertado y recuperado: {tabla_incidentes.get('I-152').tipo}")
    
    # 4. PriorityQueue
    cola_prioridad = PriorityQueue()
    cola_prioridad.insertar(inc_demo)
    cola_prioridad.insertar(Incident("I-102", "Zona_2", 12.0, "Accidente Vial", time.time()))
    print(f"[OK] PriorityQueue Max-Heap funcional. Incidente mas urgente extraido: {cola_prioridad.extraer_urgente().id}")
    print("=" * 70)
    print()


def ejecutar_demostracion_reportes():
    """Genera reportes de incidentes ordenados usando MergeSort y QuickSort."""
    print("[STEP 2/4] GENERACION DE REPORTES DE INCIDENTES (SORTING)")
    print("=" * 70)
    
    timestamp_base = time.time()
    incidentes_activos = [
        Incident("I-152", "Zona_1", 8.5, "Incendio", timestamp_base - 500),
        Incident("I-102", "Zona_2", 12.0, "Accidente Vial", timestamp_base - 100),
        Incident("I-305", "Zona_1", 9.2, "Emergencia Medica", timestamp_base - 400),
        Incident("I-204", "Zona_3", 5.5, "Derrumbe", timestamp_base - 300),
        Incident("I-099", "Zona_4", 7.0, "Incendio", timestamp_base - 200),
    ]

    # Reporte A: Por timestamp
    reporte_antiguos = merge_sort(incidentes_activos, key=lambda x: x.timestamp)
    print("Reporte A: Incidentes mas antiguos (MergeSort por timestamp - ascendente):")
    for i, inc in enumerate(reporte_antiguos, 1):
        print(f"  {i}. ID: {inc.id} | Tipo: {inc.tipo:<18} | Timestamp: {inc.timestamp:.2f}")
    print()
    
    # Reporte B: Por prioridad
    reporte_criticos = quick_sort(incidentes_activos, key=lambda x: x.prioridad, reverse=True)
    print("Reporte B: Incidentes mas criticos (QuickSort por prioridad - descendente):")
    for i, inc in enumerate(reporte_criticos, 1):
        print(f"  {i}. ID: {inc.id} | Tipo: {inc.tipo:<18} | Prioridad: {inc.prioridad:.2f}")
    print("=" * 70)
    print()


def ejecutar_fase_5_6_7():
    """Fases 5, 6 y 7: Red Vial de 50 Nodos, Búsqueda de Caminos Mínimos y Simulación de Despacho."""
    print("[STEP 3/4] SIMULACION DE DESPACHO E INTEGRACION EN TIEMPO REAL")
    print("=" * 70)

    verificar_y_generar_datos()
    
    # A. Carga de la Red Vial Completa
    print("[SATELLITE] Cargando mapa de la red vial...")
    red_vial_completa = RoadNetwork()
    red_vial_completa.cargar_desde_json("red_vial.json")
    time.sleep(0.5)
    print(f"[SATELLITE] Mapa cargado: {len(red_vial_completa.obtener_nodos())} distritos y 121 rutas monitoreadas.")
    print()
    
    # Inicialización de Centros de Emergencia en la Red Vial
    centro_a_id, centro_a_nodo = "EC-01", "Nodo_0_0"  # Extremo Superior Izquierdo
    centro_b_id, centro_b_nodo = "EC-02", "Nodo_4_9"  # Extremo Inferior Derecho
    centro_a = EmergencyCenter(centro_a_id, "Centro de Emergencia Norte (Base Alfa)", centro_a_nodo)
    centro_b = EmergencyCenter(centro_b_id, "Centro de Emergencia Sur (Base Beta)", centro_b_nodo)
    print(f"  * {centro_a.nombre} en {centro_a.ubicacion}")
    print(f"  * {centro_b.nombre} en {centro_b.ubicacion}")
    print()
    
    # B. Carga de 500 Incidentes desde CSV
    print("[DATABASE] Sincronizando incidentes en tiempo real...")
    tabla_completa = HashTable(initial_capacity=500)
    cola_completa = PriorityQueue()
    
    with open("incidentes.csv", "r", encoding="utf-8") as f:
        lineas = f.readlines()
        
    for line in lineas[1:]:
        parts = line.strip().split(",")
        if len(parts) >= 5:
            inc_id = parts[0]
            zona = parts[1]
            prioridad = float(parts[2])
            tipo = parts[3]
            timestamp = float(parts[4])
            inc = Incident(inc_id, zona, prioridad, tipo, timestamp)
            tabla_completa.insert(inc_id, inc)
            cola_completa.insertar(inc)
            
    time.sleep(0.5)
    print(f"[DATABASE] Sincronizacion completa: {tabla_completa.size} incidentes históricos indexados.")
    print(f"[DATABASE] Cola de Emergencias: {len(cola_completa)} incidentes en espera de despacho.")
    print()
    
    # C. Simular la alerta del incidente más urgente
    print("[SYSTEM] Monitoreando alertas entrantes...")
    time.sleep(0.8)
    
    urgente = cola_completa.extraer_urgente()
    
    print("-" * 70)
    print("ALERTA DE EMERGENCIA DETECTADA")
    print(f"  ID Incidente : {urgente.id}")
    print(f"  Tipo         : {urgente.tipo}")
    print(f"  Ubicacion    : {urgente.ubicacion}")
    print(f"  Prioridad    : {urgente.prioridad:.2f}")
    print("-" * 70)
    print()
    
    time.sleep(0.6)
    
    # D. Buscar Centro de Emergencia más cercano
    animar_calculo("Calculando tiempos de viaje desde bases operativas por Dijkstra")
    res_centro_a = dijkstra(red_vial_completa, centro_a_nodo, urgente.ubicacion)
    res_centro_b = dijkstra(red_vial_completa, centro_b_nodo, urgente.ubicacion)
    
    if res_centro_a["costo"] <= res_centro_b["costo"]:
        centro_seleccionado = centro_a
        nodo_inicio = centro_a_nodo
        ruta_op = res_centro_a
    else:
        centro_seleccionado = centro_b
        nodo_inicio = centro_b_nodo
        ruta_op = res_centro_b
        
    print("DESPACHO ASIGNADO:")
    print(f"  Unidad despachada desde: {centro_seleccionado.nombre} ({nodo_inicio})")
    print(f"  Ruta mas rapida (Dijkstra): {' -> '.join(ruta_op['ruta'])}")
    print(f"  Tiempo Estimado de Arribo (ETA): {ruta_op['costo']:.2f} minutos.")
    print()
    
    time.sleep(0.8)

    # Animación interactiva del viaje de la unidad
    print("[TELEMETRY] Iniciando desplazamiento del vehiculo...")
    print(f"  [SALIDA] Base {centro_seleccionado.nombre}")
    
    ruta = ruta_op["ruta"]
    acumulado = 0.0
    
    for idx in range(len(ruta) - 1):
        u = ruta[idx]
        v = ruta[idx + 1]
        peso = red_vial_completa.obtener_peso(u, v)
        acumulado += peso
        time.sleep(0.8) # Simular tiempo de viaje
        print(f"    [UNIT] Transito {u} -> {v} ({peso:.2f} min). Costo acumulado: {acumulado:.2f} min.")
        
    time.sleep(0.5)
    print(f"\n[SUCCESS] Unidad arribo a la escena en {acumulado:.2f} minutos.")
    print(f"[SYSTEM] Estado del incidente '{urgente.id}' actualizado a: 'ATENDIDO'.")
    print("=" * 70)
    print()


def ejecutar_analisis_experimental():
    """Análisis Experimental de los Algoritmos (Ordenación y Grafos)."""
    print("[STEP 4/4] ANALISIS EXPERIMENTAL DE ALGORITMOS (BENCHMARKS)")
    print("=" * 70)

    # 1. Benchmarking de Ordenamiento
    print("Benchmark: Algoritmos de Ordenamiento (MergeSort vs QuickSort)")
    print("-" * 75)
    print(f"{'Tamano (N)':<12} | {'Caso':<15} | {'MergeSort (s)':<18} | {'QuickSort (s)':<18}")
    print("-" * 75)
    
    tamanos = [100, 500, 1000]
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
            for _ in range(3):
                data_copy = list(data)
                inicio = time.perf_counter()
                merge_sort(data_copy)
                t_merge_acum += (time.perf_counter() - inicio)
            t_merge_prom = t_merge_acum / 3.0
            
            # Benchmark QuickSort
            t_quick_acum = 0.0
            for _ in range(3):
                data_copy = list(data)
                inicio = time.perf_counter()
                quick_sort(data_copy)
                t_quick_acum += (time.perf_counter() - inicio)
            t_quick_prom = t_quick_acum / 3.0
            
            print(f"{N:<12} | {caso:<15} | {t_merge_prom:16.6f}s | {t_quick_prom:16.6f}s")
    print("-" * 75)
    print()
    
    # 2. Benchmarking de Búsqueda en Grafos
    print("Benchmark: Algoritmos de Busqueda en Grafos (BFS vs Dijkstra vs A*)")
    red_vial_completa = RoadNetwork()
    red_vial_completa.cargar_desde_json("red_vial.json")
    
    nodo_inicio = "Nodo_0_0"
    nodo_fin = "Nodo_4_9"
    
    res_bfs = bfs(red_vial_completa, nodo_inicio, nodo_fin)
    res_dijkstra = dijkstra(red_vial_completa, nodo_inicio, nodo_fin)
    res_astar = a_star(red_vial_completa, nodo_inicio, nodo_fin)
    
    print("-" * 75)
    print(f"{'Algoritmo':<15} | {'Nodos Visitados':<18} | {'Costo Total (min)':<18} | {'Cantidad de Hops':<12}")
    print("-" * 75)
    print(f"{'BFS':<15} | {len(res_bfs['visitados']):<18} | {res_bfs['costo']:<18} | {len(res_bfs['ruta']) - 1:<12}")
    print(f"{'Dijkstra':<15} | {len(res_dijkstra['visitados']):<18} | {res_dijkstra['costo']:<18} | {len(res_dijkstra['ruta']) - 1:<12}")
    print(f"{'A* (Euc.)':<15} | {len(res_astar['visitados']):<18} | {res_astar['costo']:<18} | {len(res_astar['ruta']) - 1:<12}")
    print("-" * 75)
    print()
    print("Interpretacion de resultados:")
    print("  - BFS encuentra la ruta con menor numero de hops, pero ignora el costo de tiempo real.")
    print("  - Dijkstra garantiza el tiempo de viaje optimo, explorando un espacio amplio de nodos.")
    print("  - A* utiliza la heuristica euclidiana para podar y guiar la busqueda de manera optima,")
    print("    reduciendo los nodos visitados y logrando la misma ruta optima de Dijkstra.")
    print("=" * 70)
    print()


def main():
    while True:
        limpiar_pantalla()
        print("==============================================================")
        print("  SISTEMA INTELIGENTE DE GESTION Y OPTIMIZACION DE RUTA (CLI)")
        print("==============================================================")
        print(" 1. Iniciar Simulacion y Analisis de Rendimiento del Sistema")
        print(" 2. Salir")
        print("==============================================================")
        
        opcion = input("Seleccione una opcion (1-2): ").strip()
        
        if opcion == "1":
            limpiar_pantalla()
            ejecutar_demostracion_adts_estructuras()
            ejecutar_demostracion_reportes()
            ejecutar_fase_5_6_7()
            ejecutar_analisis_experimental()
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            print("\nCerrando programa operativo...")
            print("Cierre de conexion exitoso.\n")
            break
        else:
            print("\nOpcion no valida. Intente de nuevo.")
            time.sleep(1.2)


if __name__ == '__main__':
    main()
