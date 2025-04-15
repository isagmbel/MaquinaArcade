# games/n_reinas.py

class NReinas:
    def __init__(self, n):
        """Inicializa el problema de N-Reinas con un tablero de tamaño n x n"""
        self.tamano = n
        # Usamos una lista de enteros donde cada índice es una fila y su valor es la columna donde está la reina
        # -1 significa que no hay reina en esa fila
        self.reinas = [-1] * n
        self.mejor_solucion = None
    
    def posicion_valida(self, fila, columna):
        # Verifica si es válido colocar una reina en la posición dada
        # Verificamos cada reina ya colocada
        for f in range(fila):
            c = self.reinas[f]
            if c != -1:
                # Misma columna
                if c == columna:
                    return False
                # Diagonales
                if abs(fila - f) == abs(columna - c):
                    return False
        return True
    
    def colocar_reina(self, fila, columna):
        # Intenta colocar una reina en la posición específica
        if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
            if self.posicion_valida(fila, columna):
                self.reinas[fila] = columna
                return True
        return False
    
    def quitar_reina(self, fila):
        # Quita la reina de la fila indicada
        if 0 <= fila < self.tamano:
            self.reinas[fila] = -1
            return True
        return False
    
    def _buscar_solucion(self, fila=0):
        # Método recursivo para buscar una solución usando backtracking
        # Si llegamos al final, hemos encontrado una solución
        if fila >= self.tamano:
            # Guardamos la solución actual
            self.mejor_solucion = self.reinas.copy()
            return True
        
        # Intentar colocar una reina en cada columna de esta fila
        for col in range(self.tamano):
            if self.posicion_valida(fila, col):
                # Colocar reina
                self.reinas[fila] = col
                
                # Intentar con la siguiente fila
                if self._buscar_solucion(fila + 1):
                    return True
                
                # Si no funciona, quitar la reina (backtracking)
                self.reinas[fila] = -1
        
        # No se encontró solución desde esta configuración
        return False
    
    def resolver(self):
        # Busca una solución para el problema de las N-Reinas
        # Reiniciamos el tablero
        self.reinas = [-1] * self.tamano
        
        # Buscamos una solución
        encontrado = self._buscar_solucion()
        
        # Se devuelve la mejor solución encontrada
        return self.mejor_solucion if encontrado else None
    
    def obtener_tablero(self):
        tablero = [[0 for _ in range(self.tamano)] for _ in range(self.tamano)]
        
        for fila, col in enumerate(self.reinas):
            if col != -1:
                tablero[fila][col] = 1
                
        return tablero
    
    def estado_a_json(self):
        import json
        return json.dumps({
            "tamano": self.tamano,
            "reinas": self.reinas,
            "tablero": self.obtener_tablero()
        })