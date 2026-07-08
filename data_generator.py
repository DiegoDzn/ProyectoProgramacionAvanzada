import os
import json
import random
import math
import time

def generar_red_vial(ruta_json: str):
    """
    Genera una red vial ficticia de 50 nodos y 121 aristas distribuidos en una cuadrícula.
    Guarda el resultado en un archivo JSON con coordenadas y pesos.
    """
    nodos = []
    aristas = []
    
    # 1. Crear 50 nodos en una cuadrícula de 5 filas x 10 columnas
    filas = 5
    columnas = 10
    
    for r in range(filas):
        for c in range(columnas):
            nodo_id = f"Nodo_{r}_{c}"
            # Coordenadas (x, y) en kilómetros
            x = float(c * 10 + random.uniform(-1.5, 1.5))
            y = float(r * 10 + random.uniform(-1.5, 1.5))
            nodos.append({
                "id": nodo_id,
                "x": round(x, 2),
                "y": round(y, 2)
            })

    # Mapa rápido de ID a coordenadas para calcular distancias
    coord_map = {n["id"]: (n["x"], n["y"]) for n in nodos}

    def calcular_distancia(u, v):
        x1, y1 = coord_map[u]
        x2, y2 = coord_map[v]
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        # El peso es el tiempo de viaje (distancia / velocidad promedio + factor de tráfico)
        # Asumiendo 60 km/h promedio (1 km por minuto)
        peso = dist * random.uniform(0.9, 1.3)
        return round(peso, 2)

    # 2. Conectar nodos para garantizar conectividad y obtener al menos 100 aristas
    for r in range(filas):
        for c in range(columnas):
            u = f"Nodo_{r}_{c}"
            
            # Conexión horizontal derecha
            if c + 1 < columnas:
                v = f"Nodo_{r}_{c+1}"
                aristas.append({
                    "origen": u,
                    "destino": v,
                    "peso": calcular_distancia(u, v)
                })
            
            # Conexión vertical abajo
            if r + 1 < filas:
                v = f"Nodo_{r+1}_{c}"
                aristas.append({
                    "origen": u,
                    "destino": v,
                    "peso": calcular_distancia(u, v)
                })

            # Conexión diagonal abajo-derecha (para llegar a >100 aristas)
            if r + 1 < filas and c + 1 < columnas:
                v = f"Nodo_{r+1}_{c+1}"
                aristas.append({
                    "origen": u,
                    "destino": v,
                    "peso": calcular_distancia(u, v)
                })

    # Guardar en archivo JSON
    data = {
        "nodos": nodos,
        "aristas": aristas
    }
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"  [Generator] Creado grafo de red vial en '{ruta_json}' ({len(nodos)} nodos, {len(aristas)} aristas).")


def generar_incidentes(ruta_csv: str, nodos_disponibles: list, cantidad: int = 500):
    """
    Genera un dataset de incidentes en formato CSV.
    Cada incidente tiene: ID, Zona, Prioridad, Tipo, Fecha
    """
    tipos = ["Incendio", "Accidente Vial", "Emergencia Medica", "Derrumbe", "Inundacion", "Rescate", "Fuga de Gas", "Explosion"]
    
    with open(ruta_csv, "w", encoding="utf-8") as f:
        # Escribir cabecera
        f.write("ID,Zona,Prioridad,Tipo,Fecha\n")
        
        tiempo_base = time.time()
        for i in range(1, cantidad + 1):
            inc_id = f"I-{i}"
            zona = random.choice(nodos_disponibles)
            
            # Cálculo de prioridad: severidad * factor_tiempo
            severidad = random.uniform(1.0, 10.0)
            factor_tiempo = random.uniform(0.5, 2.0)
            prioridad = round(severidad * factor_tiempo, 2)
            
            tipo = random.choice(tipos)
            
            # Fecha como timestamp (algunos reportes ocurrieron hace horas)
            inc_timestamp = tiempo_base - random.randint(0, 7200)
            
            f.write(f"{inc_id},{zona},{prioridad},{tipo},{inc_timestamp:.2f}\n")
            
    print(f"  [Generator] Creado dataset de incidentes en '{ruta_csv}' ({cantidad} registros).")


def verificar_y_generar_datos():
    """Genera los archivos de datos si no existen."""
    random.seed(42)  # Fija semilla para reproducibilidad de los archivos generados
    
    ruta_json = "red_vial.json"
    ruta_csv = "incidentes.csv"
    
    # Generar red vial si no existe
    if not os.path.exists(ruta_json):
        generar_red_vial(ruta_json)
    
    # Cargar los nodos disponibles para poder asociarlos a los incidentes
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        nodos_disponibles = [n["id"] for n in data["nodos"]]
        
    # Generar incidentes si no existe
    if not os.path.exists(ruta_csv):
        generar_incidentes(ruta_csv, nodos_disponibles, cantidad=500)


if __name__ == "__main__":
    verificar_y_generar_datos()
