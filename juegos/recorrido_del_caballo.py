# games/recorrido_del_caballo.py

class RecorridoCaballo:

    # Validación del tamaño mínimo, hay soluciones para tableros de n ≥ 5
    # Para n = 1, 3, 4 no se puede recorrer completo, 2x2 tampoco tiene solución porque no hay espacio suficiente para los movimientos en L.
    def __init__(self, dimension):
        if dimension < 5:
            raise ValueError("El tamaño mínimo del tablero debe ser 5x5.")
            
        self.dimension = dimension
        self.tablero = [[-1 for _ in range(dimension)] for _ in range(dimension)]
        self.desplazamientos = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
    
    # Verifica si una posición está dentro del tablero y no ha sido visitada.
    def posicion_valida(self, fila, columna): #coordenada fila, coordenada columna
        # devuelve True si la posición es válida, False en caso contrario
        return (0 <= fila < self.dimension and 
                0 <= columna < self.dimension and 
                self.tablero[fila][columna] == -1)
    
    # Cuenta los movimientos válidos posibles desde una posición determinada. Usado por la heurística de Warnsdorff.
    def contar_movimientos_posibles(self, fila, columna): #coordenada fila, coordenada columna
        contador = 0
        for df, dc in self.desplazamientos:
            nueva_fila, nueva_columna = fila + df, columna + dc
            if self.posicion_valida(nueva_fila, nueva_columna):
                contador += 1
        return contador # devuelve el número de movimientos posibles
    
    # Busca un recorrido completo usando backtracking y la heurística de Warnsdorff. devuelve True si se encontró una solución, False en caso contrario
    def buscar_solucion(self, fila, columna, movimientos=0): #fila actual, columna actual, contador de movs realizados
        # Marcamos la posición actual
        self.tablero[fila][columna] = movimientos
        
        # Caso base: se ha completado el recorrido
        if movimientos == self.dimension * self.dimension - 1:
            return True
        
        # Se aplica la regla de Warnsdorff
        proximos_movimientos = []
        for df, dc in self.desplazamientos:
            nueva_fila, nueva_columna = fila + df, columna + dc
            if self.posicion_valida(nueva_fila, nueva_columna):
                # Calculamos la accesibilidad
                accesibilidad = self.contar_movimientos_posibles(nueva_fila, nueva_columna)
                proximos_movimientos.append((accesibilidad, nueva_fila, nueva_columna))
        
        # se ordena según la heurística de Warnsdorff (menor número de opciones primero)
        proximos_movimientos.sort()
        
        # se intenta cada movimiento en orden
        for _, nueva_fila, nueva_columna in proximos_movimientos:
            if self.buscar_solucion(nueva_fila, nueva_columna, movimientos + 1):
                return True
        
        # Si ningún movimiento lleva a solución, backtracking
        self.tablero[fila][columna] = -1
        return False
    
    # Inicia la búsqueda del recorrido desde una posición específica. devuelve la matriz con el recorrido o none si no hay solucion
    def obtener_recorrido(self, inicio_fila=0, inicio_columna=0): #fila inicial, columna inicial
        # Validar posición inicial
        if not (0 <= inicio_fila < self.dimension and 0 <= inicio_columna < self.dimension):
            raise ValueError(f"La posición inicial ({inicio_fila},{inicio_columna}) está fuera del tablero")
            
        # Se reinicia el tablero por si se había usado previamente
        self.tablero = [[-1 for _ in range(self.dimension)] for _ in range(self.dimension)]
        
        if self.buscar_solucion(inicio_fila, inicio_columna):
            return self.tablero
        return None
    
    # devuelve es estado actual del tablero
    def obtener_estado_actual(self):
        return self.tablero