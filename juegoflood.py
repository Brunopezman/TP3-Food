from flood import Flood
from pila import Pila
from cola import Cola


class JuegoFlood:
    """
    Clase para administrar un Flood, junto con sus estados y acciones
    """

    def __init__(self, alto, ancho, n_colores):
        """
        Genera un nuevo JuegoFlood, el cual tiene un Flood y otros
        atributos para realizar las distintas acciones del juego.

        Argumentos:
            alto, ancho (int): Tamaño de la grilla del Flood.
            n_colores: Cantidad maxima de colores a incluir en la grilla.
        """
        self.flood = Flood(alto, ancho)
        self.flood.mezclar_tablero(n_colores)
        self.mejor_n_movimientos, _ = self._calcular_movimientos()
        self.n_movimientos = 0
        self.pasos_solucion = Cola()
        self.historial_movimientos = Pila()
        self.historial_deshacer = Pila()
        self.historial_rehacer = Pila()
        
    def cambiar_color(self, color):
        """
        Realiza la acción para seleccionar un color en el Flood, sumando a la
        cantidad de movimientos realizados y manejando las estructuras para
        deshacer y rehacer

        Argumentos:
            color (int): Nuevo color a seleccionar
        """
   
        self.n_movimientos += 1
        estado_ant = self.flood.clonar()                       # Almaceno el estado anterior (IMPORTANTISIMO) 
        self.historial_movimientos.apilar((estado_ant, color)) # antes de cambiar el color
        self.historial_rehacer = Pila() #Como realice un movimiento nuevo, vuelvo a inicializar el historial de rehacer
                                                              
        if not self.pasos_solucion.esta_vacia() and self.pasos_solucion.ver_frente() == color:
            self.pasos_solucion.desencolar()
        else:
            self.pasos_solucion = Cola()

        self.flood.cambiar_color(color)
        self._calcular_movimientos()

    def deshacer(self):
        """
        Deshace el ultimo movimiento realizado si existen pasos previos,
        manejando las estructuras para deshacer y rehacer.
        """

        if not self.historial_movimientos.esta_vacia():
      
            estado_ant, _ = self.historial_movimientos.desapilar()
            self.historial_rehacer.apilar((self.flood.clonar(), self.flood.obtener_color(0, 0)))
            self.flood = estado_ant
            self.n_movimientos -= 1
    
    def rehacer(self):
        """
        Rehace el movimiento que fue deshecho si existe, manejando las
        estructuras para deshacer y rehacer.
        """
        
        if not self.historial_rehacer.esta_vacia():
   
            estado_prox, color = self.historial_rehacer.desapilar()
            self.historial_movimientos.apilar((self.flood.clonar(), color))
            self.flood = estado_prox
            self.n_movimientos += 1

    def _calcular_movimientos(self):
        """
        Realiza una solución de pasos contra el Flood actual (en una Cola)
        y devuelve la cantidad de movimientos que llevó a esa solución.

        Criterio de la solucion: Llegar a la solucion de forma que la cantidad de casilleros agregados 
        para cambiar el color, sea la mayor posible.

        Devuelve:
            int: Cantidad de movimientos que llevó a la solución encontrada.
            Cola: Pasos utilizados para llegar a dicha solución
        """
        aux = self.flood.clonar()
        cantidad_movimientos = 0
        pasos_solucion = Cola()

        while not aux.esta_completado():
            color_optimo = aux.seleccionar_color_optimo()
            aux.cambiar_color(color_optimo)
            pasos_solucion.encolar(color_optimo)
            cantidad_movimientos += 1

        return cantidad_movimientos, pasos_solucion


    def hay_proximo_paso(self):
        """
        Devuelve un booleano indicando si hay una solución calculada
        """
        return not self.pasos_solucion.esta_vacia()


    def proximo_paso(self):
        """
        Si hay una solución calculada, devuelve el próximo paso.
        Caso contrario devuelve ValueError

        Devuelve:
            Color del próximo paso de la solución
        """
        return self.pasos_solucion.ver_frente()


    def calcular_nueva_solucion(self):
        """
        Calcula una secuencia de pasos que solucionan el estado actual
        del flood, de tal forma que se pueda llamar al método `proximo_paso()`
        """
        _, self.pasos_solucion = self._calcular_movimientos()


    def dimensiones(self):
        return self.flood.dimensiones()


    def obtener_color(self, fil, col):
        return self.flood.obtener_color(fil, col)


    def obtener_posibles_colores(self):
        return self.flood.obtener_posibles_colores()


    def esta_completado(self):
        return self.flood.esta_completado()


