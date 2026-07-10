document.addEventListener('DOMContentLoaded', () => {
    let graphData = null;
    let nodePositions = {}; // Mapea ID de nodo a coordenadas SVG escaladas
    let isSimulating = false;

    const svgMap = document.getElementById('svg-map');
    const tooltip = document.getElementById('map-tooltip');
    
    // Elementos de UI
    const btnDispatch = document.getElementById('btn-dispatch');
    const btnReports = document.getElementById('btn-reports');
    const dispatchLogs = document.getElementById('dispatch-logs');
    const alertList = document.getElementById('incident-alerts-list');
    const telEta = document.getElementById('tel-eta');
    const telCost = document.getElementById('tel-cost');
    const searchBenchmarksBody = document.getElementById('search-benchmarks-body');
    const barMergeSort = document.getElementById('bar-mergesort');
    const barQuickSort = document.getElementById('bar-quicksort');
    const valMergeSort = document.getElementById('val-mergesort');
    const valQuickSort = document.getElementById('val-quicksort');

    // Cargar mapa vial inicial
    cargarMapa();

    // Tabuladores de reportes
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Eventos
    btnDispatch.addEventListener('click', simularDespacho);
    btnReports.addEventListener('click', generarReportes);

    function cargarMapa() {
        fetch('/api/mapa')
            .then(res => res.json())
            .then(data => {
                graphData = data;
                renderizarGrafo(data);
            })
            .catch(err => console.error("Error al cargar mapa vial:", err));
    }

    function renderizarGrafo(data) {
        svgMap.innerHTML = ''; // Limpiar
        
        const paddingX = 4;
        const paddingY = 4;
        const svgW = 100;
        const svgH = 50;

        // Calcular límites de las coordenadas originales
        const xs = data.nodos.map(n => n.x);
        const ys = data.nodos.map(n => n.y);
        const minX = Math.min(...xs);
        const maxX = Math.max(...xs);
        const minY = Math.min(...ys);
        const maxY = Math.max(...ys);

        // Función de escalado lineal
        const scaleX = (x) => {
            if (maxX === minX) return svgW / 2;
            return paddingX + ((x - minX) / (maxX - minX)) * (svgW - 2 * paddingX);
        };
        const scaleY = (y) => {
            if (maxY === minY) return svgH / 2;
            // Invertir Y para que coordenadas cartesianas se vean bien en SVG
            return svgH - paddingY - ((y - minY) / (maxY - minY)) * (svgH - 2 * paddingY);
        };

        // Guardar posiciones escaladas
        nodePositions = {};
        data.nodos.forEach(n => {
            nodePositions[n.id] = {
                x: scaleX(n.x),
                y: scaleY(n.y)
            };
        });

        // 1. Dibujar aristas
        data.aristas.forEach(a => {
            const posU = nodePositions[a.origen];
            const posV = nodePositions[a.destino];
            if (posU && posV) {
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', posU.x);
                line.setAttribute('y1', posU.y);
                line.setAttribute('x2', posV.x);
                line.setAttribute('y2', posV.y);
                line.setAttribute('class', 'map-edge');
                line.setAttribute('id', `edge-${a.origen}-${a.destino}`);
                
                // Eventos de hover para rutas
                line.addEventListener('mousemove', (e) => {
                    tooltip.classList.remove('hidden');
                    tooltip.innerHTML = `Ruta: ${a.origen} - ${a.destino}<br>Tiempo: ${a.peso.toFixed(2)} min`;
                    tooltip.style.left = `${e.pageX + 10}px`;
                    tooltip.style.top = `${e.pageY + 10}px`;
                });
                line.addEventListener('mouseleave', () => tooltip.classList.add('hidden'));

                svgMap.appendChild(line);
            }
        });

        // 2. Dibujar nodos
        data.nodos.forEach(n => {
            const pos = nodePositions[n.id];
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', pos.x);
            circle.setAttribute('cy', pos.y);
            circle.setAttribute('r', '0.7');
            circle.setAttribute('class', 'map-node');
            circle.setAttribute('id', `node-${n.id}`);

            // Resaltar bases operativas si coinciden con los nombres
            if (n.id === 'Nodo_0_0' || n.id === 'Nodo_4_9') {
                circle.classList.add('base-node');
            }

            // Evento hover
            circle.addEventListener('mousemove', (e) => {
                tooltip.classList.remove('hidden');
                let rol = '';
                if (n.id === 'Nodo_0_0') rol = ' (Base Alfa)';
                if (n.id === 'Nodo_4_9') rol = ' (Base Beta)';
                tooltip.innerHTML = `Distrito: ${n.id}${rol}<br>Coord: (${n.x}, ${n.y})`;
                tooltip.style.left = `${e.pageX + 10}px`;
                tooltip.style.top = `${e.pageY + 10}px`;
            });
            circle.addEventListener('mouseleave', () => tooltip.classList.add('hidden'));

            svgMap.appendChild(circle);
        });
    }

    function simularDespacho() {
        if (isSimulating) return;
        isSimulating = true;
        btnDispatch.disabled = true;
        btnReports.disabled = true;

        // Resetear visualización
        cargarMapa(); // Recargar mapa limpio
        dispatchLogs.innerHTML = '';
        appendLog('[SYSTEM] Conectando con centrales de satelite...', 'info');

        fetch('/api/simular')
            .then(res => res.json())
            .then(data => {
                ejecutarAnimacionSimulacion(data);
            })
            .catch(err => {
                console.error(err);
                appendLog('[ERROR] Error en la conexión con el servidor.', 'alert');
                isSimulating = false;
                btnDispatch.disabled = false;
                btnReports.disabled = false;
            });
    }

    function ejecutarAnimacionSimulacion(data) {
        let stepIndex = 0;
        const logs = data.telemetry_logs;

        // Desplegar logs de forma secuencial
        function runLogStep() {
            if (stepIndex < logs.length) {
                const line = logs[stepIndex];
                let type = 'info';
                if (line.includes('[ALERT]') || line.includes('ALERTA')) type = 'alert';
                if (line.includes('[SUCCESS]') || line.includes('arribo')) type = 'success';
                if (line.includes('[PROCESSING]')) type = 'processing';
                appendLog(line, type);
                
                // Eventos visuales gatillados por logs
                if (line.includes('ALERTA DE EMERGENCIA DETECTADA')) {
                    // Resaltar nodo del incidente
                    const incNode = document.getElementById(`node-${data.urgente.ubicacion}`);
                    if (incNode) incNode.classList.add('incident-node');
                }

                stepIndex++;
                setTimeout(runLogStep, 350);
            } else {
                // Iniciar animación del vehículo y ruta
                animarRutaVehiculo(data);
            }
        }
        runLogStep();
    }

    function animarRutaVehiculo(data) {
        const ruta = data.route;
        if (!ruta || ruta.length === 0) {
            finalizarSimulacion(data);
            return;
        }

        // 1. Resaltar aristas en la ruta
        for (let i = 0; i < ruta.length - 1; i++) {
            const u = ruta[i];
            const v = ruta[i+1];
            // Buscar línea en ambas direcciones
            let line = document.getElementById(`edge-${u}-${v}`) || document.getElementById(`edge-${v}-${u}`);
            if (line) {
                line.classList.add('route-highlight');
            }
        }

        // 2. Crear vehículo
        const vehicle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        const posInicio = nodePositions[ruta[0]];
        vehicle.setAttribute('cx', posInicio.x);
        vehicle.setAttribute('cy', posInicio.y);
        vehicle.setAttribute('class', 'vehicle-marker');
        svgMap.appendChild(vehicle);

        // 3. Animar deslizamiento de nodo a nodo
        let hopIndex = 0;
        const stepsPerHop = 15; // Velocidad de interpolación
        
        function deslizarVehiculo() {
            if (hopIndex < ruta.length - 1) {
                const pStart = nodePositions[ruta[hopIndex]];
                const pEnd = nodePositions[ruta[hopIndex + 1]];
                let step = 0;

                function interpolar() {
                    if (step <= stepsPerHop) {
                        const t = step / stepsPerHop;
                        const currX = pStart.x + (pEnd.x - pStart.x) * t;
                        const currY = pStart.y + (pEnd.y - pStart.y) * t;
                        vehicle.setAttribute('cx', currX);
                        vehicle.setAttribute('cy', currY);
                        step++;
                        requestAnimationFrame(interpolar);
                    } else {
                        hopIndex++;
                        setTimeout(deslizarVehiculo, 100);
                    }
                }
                interpolar();
            } else {
                // Fin del viaje
                finalizarSimulacion(data);
            }
        }
        deslizarVehiculo();
    }

    function finalizarSimulacion(data) {
        // Actualizar telemetrías
        telEta.textContent = `${data.costo.toFixed(2)} min`;
        telCost.textContent = `${data.costo.toFixed(2)} min`;

        // Agregar alerta al panel de alertas recientes
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item`;
        alertItem.innerHTML = `
            <div class="header">
                <span>ID: ${data.urgente.id}</span>
                <span class="status-indicator">ATENDIDO</span>
            </div>
            <div class="meta">Tipo: ${data.urgente.tipo}</div>
            <div class="meta">Distrito: ${data.urgente.ubicacion} | Urgencia: ${data.urgente.prioridad.toFixed(2)}</div>
        `;
        // Insertar al inicio de la lista de alertas
        if (alertList.querySelector('.empty-text')) {
            alertList.innerHTML = '';
        }
        alertList.insertBefore(alertItem, alertList.firstChild);

        // Llenar tabla comparativa de algoritmos
        searchBenchmarksBody.innerHTML = '';
        data.search_benchmarks.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${row.algoritmo}</strong></td>
                <td>${row.visitados}</td>
                <td>${row.costo.toFixed(2)} min</td>
                <td>${row.hops}</td>
            `;
            searchBenchmarksBody.appendChild(tr);
        });

        // Actualizar barra de benchmarks de ordenamiento
        const tMerge = data.sorting_benchmarks.mergesort;
        const tQuick = data.sorting_benchmarks.quicksort;
        
        valMergeSort.textContent = `${tMerge.toFixed(6)}s`;
        valQuickSort.textContent = `${tQuick.toFixed(6)}s`;

        // Calcular porcentaje visual (máximo ancho de barra es 100%)
        const maxVal = Math.max(tMerge, tQuick, 0.0001);
        barMergeSort.style.width = `${(tMerge / maxVal) * 100}%`;
        barQuickSort.style.width = `${(tQuick / maxVal) * 100}%`;

        // Habilitar controles
        isSimulating = false;
        btnDispatch.disabled = false;
        btnReports.disabled = false;
        appendLog('[SYSTEM] Simulacion e investigacion finalizada. Enlace estable.', 'success');
    }

    function generarReportes() {
        if (isSimulating) return;
        
        fetch('/api/reportes')
            .then(res => res.json())
            .then(data => {
                const listCriticos = document.getElementById('list-criticos');
                const listAntiguos = document.getElementById('list-antiguos');

                // Llenar críticos
                listCriticos.innerHTML = '';
                data.criticos.forEach((inc, idx) => {
                    const item = document.createElement('div');
                    item.className = 'report-item critical';
                    item.innerHTML = `
                        <div class="header">
                            <span>${idx + 1}. ID: ${inc.id}</span>
                            <span style="color:var(--accent-primary)">Prioridad: ${inc.prioridad.toFixed(2)}</span>
                        </div>
                        <div class="meta">Tipo: ${inc.tipo} | Distrito: ${inc.ubicacion}</div>
                    `;
                    listCriticos.appendChild(item);
                });

                // Llenar antiguos
                listAntiguos.innerHTML = '';
                data.antiguos.forEach((inc, idx) => {
                    const item = document.createElement('div');
                    item.className = 'report-item';
                    const hora = new Date(inc.timestamp * 1000).toLocaleTimeString();
                    item.innerHTML = `
                        <div class="header">
                            <span>${idx + 1}. ID: ${inc.id}</span>
                            <span>Hora: ${hora}</span>
                        </div>
                        <div class="meta">Tipo: ${inc.tipo} | Distrito: ${inc.ubicacion}</div>
                    `;
                    listAntiguos.appendChild(item);
                });

                // Llenar zonas con mas incidentes
                const listZonas = document.getElementById('list-zonas');
                listZonas.innerHTML = '';
                if (data.zonas) {
                    data.zonas.forEach((z, idx) => {
                        const item = document.createElement('div');
                        item.className = 'report-item';
                        const maxCant = data.zonas[0].cantidad;
                        const pct = maxCant > 0 ? (z.cantidad / maxCant * 100) : 0;
                        item.innerHTML = `
                            <div class="header">
                                <span>${idx + 1}. ${z.zona}</span>
                                <span style="color:var(--accent-primary)">${z.cantidad} incidentes</span>
                            </div>
                            <div class="chart-bar-wrapper" style="margin-top:4px">
                                <div class="chart-bar" style="width: ${pct}%; background: ${idx < 3 ? 'var(--danger-color)' : 'var(--accent-primary)'}"></div>
                            </div>
                        `;
                        listZonas.appendChild(item);
                    });
                }

                // Llenar tabla de heap benchmarks
                const heapBody = document.getElementById('heap-benchmarks-body');
                heapBody.innerHTML = '';
                if (data.heap_benchmarks) {
                    data.heap_benchmarks.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><strong>${row.tamano}</strong></td>
                            <td>${row.insercion_s.toFixed(6)}</td>
                            <td>${row.extraccion_s.toFixed(6)}</td>
                        `;
                        heapBody.appendChild(tr);
                    });
                }

                appendLog('[SYSTEM] Reportes analíticos generados con éxito.', 'success');
            })
            .catch(err => {
                console.error(err);
                appendLog('[ERROR] Fallo al generar reportes.', 'alert');
            });
    }

    function appendLog(message, type) {
        const p = document.createElement('p');
        p.className = `log-${type}`;
        p.textContent = message;
        dispatchLogs.appendChild(p);
        dispatchLogs.scrollTop = dispatchLogs.scrollHeight;
    }
});
