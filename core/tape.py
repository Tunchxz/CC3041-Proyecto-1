class Tape:
    """
    Modela la cinta de la Máquina de Turing.
    
    Esta clase representa una cinta infinita que se expande dinámicamente
    según sea necesario. La cinta contiene símbolos y mantiene un cabezal
    de lectura/escritura que puede moverse en ambas direcciones.
    
    Attributes:
        blank_symbol: Símbolo que representa las celdas vacías de la cinta.
        tape (list): Lista de símbolos en la cinta.
        head (int): Posición actual del cabezal de lectura/escritura.
    """

    def __init__(self, input_string: str, blank_symbol=None):
        """
        Inicializa la cinta con una cadena de entrada.
        
        Args:
            input_string (str): Cadena inicial que se cargará en la cinta.
            blank_symbol: Símbolo que representa espacios en blanco (por defecto None).
        """
        self.blank_symbol = blank_symbol
        self.tape = list(input_string)
        self.head = 0


    def read(self):
        """
        Lee el símbolo en la posición actual del cabezal.
        
        Si el cabezal está fuera de los límites de la cinta, ésta se expande
        automáticamente añadiendo símbolos en blanco.
        
        Returns:
            Símbolo en la posición actual del cabezal.
        """
        if self.head < 0:
            self._expand_left()
        if self.head >= len(self.tape):
            self.tape.append(self.blank_symbol)
        return self.tape[self.head]


    def write(self, symbol):
        """
        Escribe un símbolo en la posición actual del cabezal.
        
        Si el cabezal está fuera de los límites de la cinta, ésta se expande
        automáticamente antes de escribir.
        
        Args:
            symbol: Símbolo a escribir en la posición actual.
        """
        if self.head < 0:
            self._expand_left()
        if self.head >= len(self.tape):
            self.tape.append(self.blank_symbol)

        self.tape[self.head] = symbol


    def move(self, direction):
        """
        Mueve el cabezal en la dirección especificada.
        
        Args:
            direction (str): Dirección del movimiento:
                - "L": Izquierda (decrementa la posición del cabezal)
                - "R": Derecha (incrementa la posición del cabezal)
                - "S": Sin movimiento (el cabezal permanece en su lugar)
        
        Raises:
            ValueError: Si la dirección no es válida (L, R o S).
        """
        if direction == "L":
            self.head -= 1
        elif direction == "R":
            self.head += 1
        elif direction == "S":
            pass
        else:
            raise ValueError(f"Movimiento no válido: {direction}")


    def _expand_left(self):
        """
        Expande la cinta hacia la izquierda.
        
        Añade un símbolo en blanco al inicio de la cinta y ajusta
        la posición del cabezal. Método privado usado internamente
        cuando el cabezal intenta acceder a posiciones negativas.
        """
        self.tape.insert(0, self.blank_symbol)
        self.head = 0


    def snapshot(self, current_state):
        """
        Genera una descripción instantánea (ID) del estado actual de la cinta.
        
        Crea una representación visual de la cinta mostrando los símbolos,
        la posición del cabezal (con un marcador ^) y el estado actual.
        
        Args:
            current_state: Estado actual de la máquina de Turing.
        
        Returns:
            str: Representación en texto del estado de la cinta con formato:
                - Primera línea: contenido de la cinta
                - Segunda línea: marcador de posición del cabezal
                - Tercera línea: estado actual
        """
        tape_str = "".join(symbol if symbol is not None else "_" for symbol in self.tape)
        head_marker = " " * self.head + "^"
        return f"{tape_str}\n{head_marker}\nEstado: {current_state}\n"
