def merge_sort(arr: list, key=None, reverse=False) -> list:
    """
    Ordenamiento MergeSort.
    Algoritmo de dividir y vencerás estable.
    
    Complejidad:
        - Tiempo: O(N log N) en el mejor, peor y promedio de los casos.
        - Espacio: O(N) memoria auxiliar.

    Parámetros:
        arr (list): La lista a ordenar.
        key (callable): Función para extraer la clave de comparación.
        reverse (bool): Si es True, ordena de forma descendente.

    Retorna:
        list: Una nueva lista con los elementos ordenados.
    """
    if len(arr) <= 1:
        return list(arr)

    if key is None:
        key = lambda x: x

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)

    return _merge(left, right, key, reverse)


def _merge(left: list, right: list, key, reverse: bool) -> list:
    """Combina dos listas ordenadas manteniendo la estabilidad del ordenamiento."""
    merged = []
    i = j = 0
    n_left, n_right = len(left), len(right)

    while i < n_left and j < n_right:
        val_left = key(left[i])
        val_right = key(right[j])

        # Comparación según dirección del ordenamiento
        if not reverse:
            # Ascendente (estable: <=)
            if val_left <= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            # Descendente (estable: >=)
            if val_left >= val_right:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    # Agregar elementos restantes
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr: list, key=None, reverse=False) -> list:
    """
    Ordenamiento QuickSort.
    Algoritmo de dividir y vencerás in-place (encapsulado para retornar una nueva lista).
    
    Optimización:
        - Utiliza el elemento del medio como pivote para evitar la degradación a O(N^2)
          en arreglos pre-ordenados.
          
    Complejidad:
        - Tiempo: O(N log N) promedio, O(N^2) en el peor caso.
        - Espacio: O(log N) espacio auxiliar recursivo.

    Parámetros:
        arr (list): La lista a ordenar.
        key (callable): Función para extraer la clave de comparación.
        reverse (bool): Si es True, ordena de forma descendente.

    Retorna:
        list: Una nueva lista con los elementos ordenados.
    """
    temp_arr = list(arr)
    if len(temp_arr) <= 1:
        return temp_arr

    if key is None:
        key = lambda x: x

    _quick_sort_helper(temp_arr, 0, len(temp_arr) - 1, key, reverse)
    return temp_arr


def _quick_sort_helper(arr: list, low: int, high: int, key, reverse: bool):
    """Función auxiliar recursiva para QuickSort."""
    if low < high:
        pivot_idx = _partition(arr, low, high, key, reverse)
        _quick_sort_helper(arr, low, pivot_idx - 1, key, reverse)
        _quick_sort_helper(arr, pivot_idx + 1, high, key, reverse)


def zone_frequency_report(incidentes: list) -> list:
    """
    Genera un reporte de frecuencia de incidentes por zona/ubicacion.

    Recorre la lista de incidentes, cuenta cuantos hay en cada zona
    y retorna una lista de tuplas (zona, cantidad) ordenada por frecuencia
    descendente usando MergeSort.

    Complejidad:
        - Tiempo: O(N + Z log Z) donde N es el numero de incidentes y Z el numero de zonas unicas.
        - Espacio: O(Z) para el conteo de frecuencias.

    Parametros:
        incidentes (list): Lista de objetos Incident.

    Retorna:
        list: Lista de tuplas (zona, cantidad) ordenada por cantidad descendente.
    """
    frecuencias = {}
    for inc in incidentes:
        zona = inc.ubicacion
        if zona in frecuencias:
            frecuencias[zona] += 1
        else:
            frecuencias[zona] = 1

    lista_frecuencias = [(zona, cant) for zona, cant in frecuencias.items()]
    return merge_sort(lista_frecuencias, key=lambda x: x[1], reverse=True)


def _partition(arr: list, low: int, high: int, key, reverse: bool) -> int:
    """Particiona el subarreglo y retorna el índice final del pivote."""
    # Selección de pivote: elemento medio para mitigar peor caso de pre-ordenado
    mid = (low + high) // 2
    # Mover el pivote al final
    arr[mid], arr[high] = arr[high], arr[mid]
    
    pivot = arr[high]
    pivot_key = key(pivot)
    
    i = low - 1
    for j in range(low, high):
        val_j = key(arr[j])
        
        if not reverse:
            # Ascendente
            if val_j <= pivot_key:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        else:
            # Descendente
            if val_j >= pivot_key:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
    # Colocar pivote en su posición final
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
