import random
from cola import Cola

class Flood:
    """
    Clase para administrar un tablero de N colores.
    """

    def __init__(self, alto, ancho):
        """
        Genera un nuevo Flood de un mismo color con las dimensiones dadas.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla.
        """
    
        self.alto = alto
        self.ancho = ancho
        self.colores_usados = set() #Me va a permitir guardar los colores sin que se repitan
        self.tablero = [[0 for _ in range(ancho)] for _ in range(alto)] #Lista por compresion del tablero

    def mezclar_tablero(self, n_colores):

        """
        Asigna de forma completamente aleatoria hasta `n_colores` a lo largo de
        las casillas del tablero.

        Argumentos:
            n_colores (int): Cantidad maxima de colores a incluir en la grilla.
        """
        
        for fil in range(self.alto):
            for col in range(self.ancho):
                color = random.randint(1, n_colores)
                self.tablero[fil][col] = color
                self.colores_usados.add(color)


    def obtener_color(self, fil, col):
        """
        Devuelve el color que se encuentra en las coordenadas solicitadas.

        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.

        Devuelve:
            Color asignado.
        """

        return self.tablero[fil][col]


    def obtener_posibles_colores(self):
        """
        Devuelve una secuencia ordenada de todos los colores posibles del juego.
        La secuencia tendrá todos los colores posibles que fueron utilizados
        para generar el tablero, sin importar cuántos de estos colores queden
        actualmente en el tablero.

        Devuelve:
            iterable: secuencia ordenada de colores.
        """
        
        return sorted(self.colores_usados) #Ordenados de manera ascendente

    def dimensiones(self) -> tuple:
        """
        Dimensiones de la grilla (filas y columnas)

        Devuelve:
            (int, int): alto y ancho de la grilla en ese orden.
        """
        return self.alto, self.ancho


    def cambiar_color(self, color_nuevo):
        """
        Asigna el nuevo color al Flood de la grilla. Es decir, a todas las
        coordenadas que formen un camino continuo del mismo color comenzando
        desde la coordenada origen en (0, 0) se les asignará `color_nuevo`

        Argumentos:
            color_nuevo: Valor del nuevo color a asignar al Flood.
        """
        
        color_actual = self.obtener_color(0,0)

        if color_actual == color_nuevo:
            return

        return self._cambiar_color(0, 0, color_actual, color_nuevo)
    

    def _cambiar_color(self, fil, col, color_actual, color_nuevo):

        if fil < 0 or fil >= self.alto or col < 0 or col >= self.ancho:
            return
        
        if self.obtener_color(fil, col) != color_actual:
            return
        
        self.tablero[fil][col] = color_nuevo

        self._cambiar_color(fil + 1, col, color_actual, color_nuevo) 
        self._cambiar_color(fil - 1, col, color_actual, color_nuevo) 
        self._cambiar_color(fil , col + 1, color_actual, color_nuevo) 
        self._cambiar_color(fil , col - 1, color_actual, color_nuevo)


    def clonar(self):
        """
        Devuelve:
            Flood: Copia del Flood actual
        """
     
        copia_flood = Flood(self.alto, self.ancho)
        copia_flood.colores_usados = set(self.colores_usados)
        copia_flood.tablero = []
        for fila in self.tablero:
            nueva_fila = list(fila)
            copia_flood.tablero.append(nueva_fila)

        return copia_flood

    def esta_completado(self):
        """
        Indica si todas las coordenadas de grilla tienen el mismo color

        Devuelve:
            bool: True si toda la grilla tiene el mismo color
        """

        color_actual = self.obtener_color(0, 0)
        
        for fil in range(self.alto):
            for col in range(self.ancho):
                if self.obtener_color(fil, col) != color_actual:
                    return False
                
        return True

    
    def seleccionar_color_optimo(self):
        """
        Selecciona el color óptimo, que es el color que más casilleros abarca.  

        Devuelve:
            Color óptimo a seleccionar.
        """
        colores_posibles = self.obtener_posibles_colores()
        max_cantidad_casilleros = 0
        color_optimo = None
   
        for color in colores_posibles:
            aux = self.clonar()
            aux.cambiar_color(color)
            cantidad_casilleros = aux.area_actual(0, 0, {})

            if cantidad_casilleros > max_cantidad_casilleros:
                max_cantidad_casilleros = cantidad_casilleros
                color_optimo = color
                
        return color_optimo
    
    def area_actual(self, fil, col, casilleros_recorridos):
        """
        Argumentos:
            fil, col (int): Posiciones de la fila y columna en la grilla.
            casilleros_recorridos(dict): Casilleros que se van revisando

        Devuelve: 
            Cantidad de casilleros que abarca el color
        """
        
        color_actual = self.tablero[0][0]

        if 0 <= fil < self.alto and 0 <= col < self.ancho:
            if self.tablero[fil][col] == color_actual and (fil, col) not in casilleros_recorridos:
                casilleros_recorridos[(fil, col)] = 1
                return 1 + self.area_actual(fil, col + 1, casilleros_recorridos) + self.area_actual(fil + 1, col, casilleros_recorridos) + self.area_actual(fil, col - 1, casilleros_recorridos) + self.area_actual(fil - 1, col, casilleros_recorridos)

        return 0