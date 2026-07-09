import http.server
import json
import os
import time
import random
import webbrowser
from models.incident import Incident
from models.center import EmergencyCenter
from models.road_network import RoadNetwork
from structures.hash_table import HashTable
from structures.priority_queue import PriorityQueue
from structures.sorting import merge_sort, quick_sort
from structures.graph_search import bfs, dijkstra, a_star
from data_generator import verificar_y_generar_datos

class DashboardRequestHandler(http.server.BaseHTTPRequestHandler):
    """Manejador HTTP para la API y archivos estáticos del Dashboard."""

    def log_message(self, format, *args):
        # Desactivar logging por defecto en terminal para mantener la consola limpia
        pass

    def do_GET(self):
        url = self.path.split("?")[0]

        # 1. API Endpoints
        if url == "/api/mapa":
            self.servir_mapa()
        elif url == "/api/simular":
            self.servir_simulacion()
        elif url == "/api/reportes":
            self.servir_reportes()
        # 2. Servir archivos estáticos
        elif url == "/" or url == "/index.html":
            self.servir_archivo_estatico("index.html", "text/html; charset=utf-8")
        elif url == "/index.css":
            self.servir_archivo_estatico("index.css", "text/css")
        elif url == "/index.js":
            self.servir_archivo_estatico("index.js", "application/javascript")
        else:
            self.send_error(404, "Archivo no encontrado")

    def servir_archivo_estatico(self, filename, content_type):
        if not os.path.exists(filename):
            self.send_error(404, f"Archivo {filename} no existe")
            return
        
        try:
            with open(filename, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error interno: {str(e)}")

    def servir_mapa(self):
        verificar_y_generar_datos()
        if not os.path.exists("red_vial.json"):
            self.send_error(500, "Archivo red_vial.json no generado")
            return
        
        try:
            with open("red_vial.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.send_json_response(data)
        except Exception as e:
            self.send_error(500, f"Error al leer red: {str(e)}")

    def servir_simulacion(self):
        verificar_y_generar_datos()
        
        # Logs telemétricos simulados
        logs = []
        logs.append("[SATELLITE] Cargando mapa de la red vial completa...")
        
        red_vial_completa = RoadNetwork()
        red_vial_completa.cargar_desde_json("red_vial.json")
        logs.append(f"[SATELLITE] Mapa cargado con {len(red_vial_completa.obtener_nodos())} distritos y 121 aristas.")
        
        # Centros
        centro_a_id, centro_a_nodo = "EC-01", "Nodo_0_0"
        centro_b_id, centro_b_nodo = "EC-02", "Nodo_4_9"
        centro_a = EmergencyCenter(centro_a_id, "Centro Norte (Base Alfa)", centro_a_nodo)
        centro_b = EmergencyCenter(centro_b_id, "Centro Sur (Base Beta)", centro_b_nodo)
        
        logs.append(f"[DATABASE] Sincronizando base de datos de incidentes...")
        
        tabla_completa = HashTable(initial_capacity=500)
        cola_completa = PriorityQueue()
        incidentes_lista = []
        
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
                incidentes_lista.append(inc)
                
        logs.append(f"[DATABASE] Sincronizacion completa: {tabla_completa.size} incidentes listos.")
        logs.append(f"[SYSTEM] Monitoreando alertas entrantes...")
        
        # Seleccionar un incidente aleatorio para el despacho en vivo
        urgente = random.choice(incidentes_lista)
        logs.append(f"[ALERT] ALERTA CRITICA DETECTADA: ID {urgente.id} | Tipo: {urgente.tipo} en {urgente.ubicacion} (Prioridad: {urgente.prioridad:.2f})")
        
        logs.append(f"[PROCESSING] Calculando rutas optimas desde bases operativas por Dijkstra...")
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
            
        logs.append(f"[DISPATCH] Asignando base operativa: {centro_seleccionado.nombre}")
        logs.append(f"[DISPATCH] Unidad movil despachada. Tiempo estimado ETA: {ruta_op['costo']:.2f} min.")
        
        logs.append(f"[TELEMETRY] Iniciando trayecto telemétrico del vehículo...")
        ruta = ruta_op["ruta"]
        acumulado = 0.0
        for idx in range(len(ruta) - 1):
            u = ruta[idx]
            v = ruta[idx + 1]
            peso = red_vial_completa.obtener_peso(u, v)
            acumulado += peso
            logs.append(f"[UNIT] Transito {u} -> {v} (+{peso:.2f} min). Costo acumulado: {acumulado:.2f} min.")
            
        logs.append(f"[SUCCESS] Unidad llego a destino con exito. Incidente {urgente.id} atendido.")
        
        # Benchmarks de búsqueda
        res_bfs = bfs(red_vial_completa, nodo_inicio, urgente.ubicacion)
        res_astar = a_star(red_vial_completa, nodo_inicio, urgente.ubicacion)
        
        search_benchmarks = [
            {"algoritmo": "BFS", "visitados": len(res_bfs["visitados"]), "costo": res_bfs["costo"], "hops": len(res_bfs["ruta"]) - 1 if res_bfs["ruta"] else 0},
            {"algoritmo": "Dijkstra", "visitados": len(ruta_op["visitados"]), "costo": ruta_op["costo"], "hops": len(ruta) - 1},
            {"algoritmo": "A* (Euc.)", "visitados": len(res_astar["visitados"]), "costo": res_astar["costo"], "hops": len(res_astar["ruta"]) - 1 if res_astar["ruta"] else 0}
        ]
        
        # Benchmarks de ordenación (N=1000)
        random.seed(42)
        benchmark_data = [random.randint(1, 100000) for _ in range(1000)]
        
        # MergeSort
        data_copy = list(benchmark_data)
        inicio = time.perf_counter()
        merge_sort(data_copy)
        t_merge = time.perf_counter() - inicio
        
        # QuickSort
        data_copy = list(benchmark_data)
        inicio = time.perf_counter()
        quick_sort(data_copy)
        t_quick = time.perf_counter() - inicio
        
        sorting_benchmarks = {
            "mergesort": t_merge,
            "quicksort": t_quick
        }
        
        response_payload = {
            "urgente": {
                "id": urgente.id,
                "tipo": urgente.tipo,
                "ubicacion": urgente.ubicacion,
                "prioridad": urgente.prioridad
            },
            "assigned_center": centro_seleccionado.nombre,
            "route": ruta,
            "costo": ruta_op["costo"],
            "telemetry_logs": logs,
            "search_benchmarks": search_benchmarks,
            "sorting_benchmarks": sorting_benchmarks
        }
        self.send_json_response(response_payload)

    def servir_reportes(self):
        verificar_y_generar_datos()
        
        try:
            incidentes_lista = []
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
                    incidentes_lista.append(Incident(inc_id, zona, prioridad, tipo, timestamp))
                    
            # 1. Reporte críticos (QuickSort prioridad desc)
            criticos_ordenados = quick_sort(incidentes_lista, key=lambda x: x.prioridad, reverse=True)
            top_criticos = [{
                "id": x.id,
                "tipo": x.tipo,
                "ubicacion": x.ubicacion,
                "prioridad": x.prioridad
            } for x in criticos_ordenados[:10]]
            
            # 2. Reporte antiguos (MergeSort timestamp asc)
            antiguos_ordenados = merge_sort(incidentes_lista, key=lambda x: x.timestamp)
            top_antiguos = [{
                "id": x.id,
                "tipo": x.tipo,
                "ubicacion": x.ubicacion,
                "timestamp": x.timestamp
            } for x in antiguos_ordenados[:10]]
            
            self.send_json_response({
                "criticos": top_criticos,
                "antiguos": top_antiguos
            })
        except Exception as e:
            self.send_error(500, f"Error al procesar reportes: {str(e)}")

    def send_json_response(self, data):
        try:
            content = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Fallo al codificar JSON: {str(e)}")


def iniciar_servidor(puerto=8000):
    """Inicia el servidor HTTP en el puerto indicado y abre el navegador."""
    server_address = ('', puerto)
    httpd = http.server.HTTPServer(server_address, DashboardRequestHandler)
    
    print("\n[SERVER] Servidor web iniciado en http://localhost:8000/")
    print("[SERVER] Abra este enlace en su navegador para ver la interfaz grafica.")
    print("[SERVER] Presione Ctrl+C en esta terminal para detener el servidor.\n")
    
    # Abrir el navegador por defecto automáticamente después de una breve espera
    def abrir_navegador():
        time.sleep(0.5)
        webbrowser.open(f"http://localhost:{puerto}/")
        
    import threading
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SERVER] Deteniendo servidor web...")
        httpd.server_close()
        print("[SERVER] Servidor web apagado correctamente.")
