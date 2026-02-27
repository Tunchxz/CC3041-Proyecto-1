import os
from parser.loader import MTConfigLoader
from core.turing_machine import TuringMachine
from core.simulation import Simulator
from config import CONFIGURACION, OUTPUT_DIR, PRINT_RESULT, PRINT_LENGTH

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
    loader = MTConfigLoader(CONFIGURACION)
    config = loader.load()

    machine = TuringMachine(config)
    simulator = Simulator(machine)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    simulation_counter = 1

    def clean_tape_content(tape):
        """Extrae el contenido de la cinta sin blanks y sin símbolos de control."""
        # Eliminar B's que representan blanks
        content = ''.join([str(sym) for sym in tape.tape if sym is not None])
        # Calcular la longitud del string
        length = len(content)
        if PRINT_LENGTH:
            return content.strip() + f" = {length}"
        
        return content.strip()

    for s in config["simulation_strings"]:
        accepted, log_lines, final_tape = simulator.run_string(str(s))

        output_path = os.path.join(
            OUTPUT_DIR,
            f"simulation_{simulation_counter}.txt"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            for line in log_lines:
                f.write(line + "\n")

            f.write("\n" + "-"*40 + "\n")
            if PRINT_RESULT:
                final_content = clean_tape_content(final_tape)
                f.write(f"RESULTADO FINAL: {final_content}\n")
            else:
                f.write("RESULTADO FINAL:\n")
            
            if accepted:
                f.write("Cadena ACEPTADA ✔\n")
            else:
                f.write("Cadena RECHAZADA ✘\n")
            f.write("-"*40 + "\n")

        print(f"Archivo generado: {output_path}")
        simulation_counter += 1


if __name__ == "__main__":
    main()
