"""
Módulo para la carga y validación de configuraciones de Máquinas de Turing.

Este módulo proporciona la clase MTConfigLoader que permite cargar archivos
YAML con las especificaciones de una Máquina de Turing y validar su estructura.
"""

import yaml


class MTConfigLoader:
    """
    Carga y valida la configuración YAML para la Máquina de Turing.
    
    Esta clase se encarga de leer archivos de configuración en formato YAML
    y validar que contengan todos los elementos necesarios para la definición
    formal de una Máquina de Turing.
    
    Attributes:
        path (str): Ruta al archivo YAML de configuración.
    """

    def __init__(self, path: str):
        """
        Inicializa el cargador de configuración.
        
        Args:
            path (str): Ruta completa al archivo YAML de configuración de la
                Máquina de Turing.
        """
        self.path = path


    def load(self):
        """
        Carga y valida el archivo de configuración YAML.
        
        Lee el archivo YAML especificado en la ruta y valida que contenga
        todos los campos requeridos para definir una Máquina de Turing.
        
        Returns:
            dict: Diccionario con la configuración completa de la Máquina de
                Turing, incluyendo estados, alfabetos, función de transición
                y cadenas de simulación.
        
        Raises:
            FileNotFoundError: Si el archivo especificado no existe.
            yaml.YAMLError: Si el archivo no tiene un formato YAML válido.
            ValueError: Si la configuración no contiene todos los campos
                requeridos o si falta el estado inicial o final.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._validate_structure(data)
        return data


    def _validate_structure(self, data):
        """
        Valida que la estructura de datos contenga todos los campos requeridos.
        
        Verifica que el diccionario de configuración contenga las claves
        necesarias para definir una Máquina de Turing: estados, alfabetos,
        función de transición y cadenas de simulación. También valida que
        se especifiquen los estados inicial y final.
        
        Args:
            data (dict): Diccionario con la configuración cargada del archivo YAML.
        
        Raises:
            ValueError: Si falta algún campo requerido o si no se especifican
                el estado inicial y/o final.
        """
        required = [
            "q_states", "alphabet", "tape_alphabet",
            "delta", "simulation_strings"
        ]

        for key in required:
            if key not in data:
                raise ValueError(f"La configuración no contiene '{key}'")

        if "initial" not in data["q_states"] or "final" not in data["q_states"]:
            raise ValueError("Debe especificar estado inicial y final.")
