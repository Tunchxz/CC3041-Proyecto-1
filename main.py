import os
from parser.loader import MTConfigLoader
from core.turing_machine import TuringMachine
from core.simulation import Simulator

def main():
    """
    Función principal que ejecuta el simulador de Máquinas de Turing.
    
    Esta función:
    1. Carga la configuración de la Máquina de Turing desde un archivo YAML
    2. Inicializa la máquina y el simulador
    3. Ejecuta simulaciones para cada cadena especificada en la configuración
    4. Genera archivos de salida con los resultados en el directorio 'outputs'
    
    Raises:
        FileNotFoundError: Si el archivo de configuración no existe.
        ValueError: Si la configuración es inválida o incompleta.
    """
    # Cambiar el nombre del archivo para usar una configuración diferente
    loader = MTConfigLoader("machines/config2.yaml")
    config = loader.load()

    machine = TuringMachine(config)
    simulator = Simulator(machine)

    os.makedirs("outputs", exist_ok=True)

    simulation_counter = 1

    for s in config["simulation_strings"]:
        accepted, log_lines = simulator.run_string(s)

        output_path = os.path.join(
            "outputs",
            f"simulation_{simulation_counter}.txt"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            for line in log_lines:
                f.write(line + "\n")

            f.write("\n" + "-"*30 + "\n")
            f.write("RESULTADO FINAL:\n")
            if accepted:
                f.write("Cadena ACEPTADA ✔\n")
            else:
                f.write("Cadena RECHAZADA ✘\n")
            f.write("-"*30 + "\n")

        print(f"Archivo generado: {output_path}")
        simulation_counter += 1


if __name__ == "__main__":
    main()
