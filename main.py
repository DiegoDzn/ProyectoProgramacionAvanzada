import time
from models.incident import Incident
from models.center import EmergencyCenter
from models.road_network import RoadNetwork
from structures.hash_table import HashTable
from structures.priority_queue import PriorityQueue


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


if __name__ == '__main__':
    main()
