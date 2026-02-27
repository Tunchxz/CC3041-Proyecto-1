class TuringMachine:
    """
    Representa la Máquina de Turing según la configuración cargada.
    
    Esta clase modela una Máquina de Turing formal con sus componentes:
    estados, alfabetos, función de transición y configuración inicial.
    Incluye soporte para memoria cache adicional.
    
    Attributes:
        states (list): Lista de todos los estados de la máquina.
        initial_state (str): Estado inicial de la máquina.
        final_state (str): Estado de aceptación/final.
        alphabet (list): Alfabeto de entrada.
        tape_alphabet (list): Alfabeto de la cinta (incluye símbolos adicionales).
        delta_raw (list): Representación cruda de la función de transición desde YAML.
        simulation_strings (list): Cadenas a simular.
        blank_symbol: Símbolo que representa espacios en blanco en la cinta.
        delta (dict): Función de transición procesada como diccionario.
    """

    def __init__(self, config):
        """
        Inicializa la Máquina de Turing con la configuración proporcionada.
        
        Procesa la configuración cargada desde un archivo YAML y construye
        la función de transición (delta) como un diccionario para acceso eficiente.
        
        Args:
            config (dict): Diccionario con la configuración completa de la máquina,
                que debe incluir: q_states, alphabet, tape_alphabet,
                delta y simulation_strings.
        """
        states = config["q_states"]
        self.states = states["q_list"]
        self.initial_state = states["initial"]
        self.final_state = states["final"]

        self.alphabet = config["alphabet"]
        self.tape_alphabet = config["tape_alphabet"]
        self.delta_raw = config["delta"]
        self.simulation_strings = config["simulation_strings"]

        self.blank_symbol = None  # YAML blank

        # Construir diccionario de transiciones
        self.delta = {}
        for rule in self.delta_raw:
            p = rule["params"]
            o = rule["output"]

            key = (
                p["initial_state"],
                p["mem_cache_value"],
                p["tape_input"]
            )

            self.delta[key] = (
                o["final_state"],
                o["mem_cache_value"],
                o["tape_output"],
                o["tape_displacement"]
            )
