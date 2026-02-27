"""
Módulo para la simulación de Máquinas de Turing.

Este módulo proporciona la clase Simulator que ejecuta simulaciones
de Máquinas de Turing y genera registros detallados de cada transición.
"""

from core.tape import Tape


class Simulator:
    """
    Ejecuta la simulación de la Máquina de Turing con registro detallado.
    
    Esta clase se encarga de simular la ejecución de una Máquina de Turing,
    registrando cada transición en formato formal y generando descripciones
    instantáneas (ID) del estado de la máquina en cada paso.
    
    Attributes:
        machine (TuringMachine): Instancia de la Máquina de Turing a simular.
    """

    def __init__(self, machine):
        """
        Inicializa el simulador con una Máquina de Turing.
        
        Args:
            machine (TuringMachine): Máquina de Turing configurada que se va a simular.
        """
        self.machine = machine


    def format_id(self, tape, state, cache):
        """
        Construye la descripción instantánea (ID) formal de la configuración actual.
        
        Genera una representación formal del estado de la máquina mostrando
        el contenido de la cinta con la notación del estado y cache en la
        posición del cabezal.
        
        Args:
            tape (Tape): Cinta actual de la máquina.
            state (str): Estado actual de la máquina.
            cache: Valor actual de la memoria cache (None representa B).
        
        Returns:
            str: ID formal con formato [estado,cache]símbolo...
                Ejemplo: [q0,B]aab#aab (cuando el cabezal está al inicio)
        """
        symbols = tape.tape
        head = tape.head

        mem_display = cache if cache is not None else "B"

        id_str = ""

        for i, sym in enumerate(symbols):
            s = sym if sym is not None else "B"

            if i == head:
                id_str += f"[{state},{mem_display}]{s}"
            else:
                id_str += s

        return id_str


    def run_string(self, input_str):
        """
        Ejecuta la simulación de la Máquina de Turing sobre una cadena de entrada.
        
        Simula paso a paso la ejecución de la máquina sobre la cadena proporcionada,
        registrando cada transición con su función delta, ID antes y después.
        La simulación continúa hasta alcanzar el estado final o hasta que no
        exista una transición válida.
        
        Args:
            input_str (str): Cadena de entrada a procesar por la máquina.
        
        Returns:
            tuple: (aceptada, log, tape) donde:
                - aceptada (bool): True si la cadena fue aceptada (llegó al estado final) / False si fue rechazada (no hay transición válida).
                - log (list): Lista de strings con el registro detallado de la simulación, incluyendo cada transición en formato formal.
                - tape (Tape): Estado final de la cinta después de la simulación.
        """
        tape = Tape(input_str, blank_symbol=self.machine.blank_symbol)
        state = self.machine.initial_state
        cache = None

        log = []  # Lista de líneas formateadas para el archivo

        log.append("-"*50 + f"\nSimulación para la cadena: {input_str}\n" + "-"*50 + "\n")
        log.append("Para esta cadena, las transiciones son:\n")

        step = 0

        while True:
            id_before = self.format_id(tape, state, cache)

            symbol = tape.read()
            key = (state, cache, symbol)

            if key not in self.machine.delta:
                return False, log, tape

            new_state, new_cache, tape_output, movement = self.machine.delta[key]

            # Cambiar representación B
            sym_in = symbol if symbol is not None else "B"
            sym_out = tape_output if tape_output is not None else "B"

            mem_before = cache if cache is not None else "B"
            mem_after = new_cache if new_cache is not None else "B"

            # Regla formal:
            rule_str = (
                f"δ([{state}, {mem_before}], {sym_in}) = "
                f"([{new_state}, {mem_after}], {sym_out}, {movement})"
            )

            # Aplicar transición
            tape.write(tape_output)
            cache = new_cache
            tape.move(movement)
            state = new_state

            id_after = self.format_id(tape, state, cache)

            # Registrar transición formal
            log.append(f"{rule_str:<40} {id_before:<20} ⊢   {id_after}")

            if state == self.machine.final_state:
                return True, log, tape

            step += 1
