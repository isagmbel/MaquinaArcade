# games/torres_de_hanoi.py

# se inicializa el juego con n discos
class TorresHanoi:
    def __init__(self, n_discos=3):

        self.n_discos = n_discos
        # se inicializan las torres (0, 1, 2)
        self.torres = [list(range(n_discos, 0, -1)), [], []]
        self.movimientos_realizados = []
        self.contador_movimientos = 0
    
    #si es valido, se mueve un disco entre las torres
    def mover_disco(self, origen, destino):

        # se verifican los índices
        if not (0 <= origen <= 2 and 0 <= destino <= 2):
            return False
        
        # se verifica que haya discos en la torre origen
        if not self.torres[origen]:
            return False
            
        # se verifica que el movimiento sea válido
        if self.torres[destino] and self.torres[origen][-1] > self.torres[destino][-1]:
            return False
            
        # movemos el disco
        disco = self.torres[origen].pop()
        self.torres[destino].append(disco)
        self.movimientos_realizados.append((origen, destino, disco))
        self.contador_movimientos += 1
        return True
    

    #verifica si el juego esta resuelto
    def esta_resuelto(self):
        return len(self.torres[2]) == self.n_discos
    
    # devuelve el estado actual de las torres (copia)
    def obtener_estado(self):
        return [torre.copy() for torre in self.torres]
    
    # reinicia el juego al estado inicial
    def reiniciar(self):
        self.torres = [list(range(self.n_discos, 0, -1)), [], []]
        self.movimientos_realizados = []
        self.contador_movimientos = 0
    
    #devuelve una lista de movimientos para resolver el problema
    def resolver(self):
        movimientos = []
        
        def mover(n, origen, destino, auxiliar):
            if n == 1:
                movimientos.append((origen, destino))
            else:
                mover(n-1, origen, auxiliar, destino)
                movimientos.append((origen, destino))
                mover(n-1, auxiliar, destino, origen)
                
        mover(self.n_discos, 0, 2, 1)
        return movimientos
    
    #convierte el estado actual a formato JSON
    def estado_a_json(self):
        import json
        estado = {
            "torres": self.torres,
            "movimientos": self.movimientos_realizados,
            "contador": self.contador_movimientos
        }
        return json.dumps(estado)