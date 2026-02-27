# Proyecto 1: Simulador de Máquina de Turing para la Sucesión de Fibonacci

Este proyecto implementa una simulación de una Máquina de Turing determinista de una cinta que calcula la sucesión de Fibonacci. Dada una entrada en notación unaria que representa un número natural *n*, la máquina computa el *n*-ésimo término de la sucesión de Fibonacci y lo retorna en notación unaria.

## Funcionalidades

- **Cálculo de la Sucesión de Fibonacci** usando una Máquina de Turing determinista
- **Entrada/salida en notación unaria** para representación natural de números
- **Carga de configuración YAML** con validación de estructura completa
- **Simulación con memoria cache adicional** para operaciones intermedias
- **Cinta infinita dinámica** que se expande automáticamente según necesidad
- **Registro detallado de transiciones** en notación formal matemática
- **Generación de descripciones instantáneas (ID)** en cada paso de la simulación
- **Archivos de salida individuales** para cada número calculado
- **Configuración centralizada** mediante archivo `config.py`

## Diseño de la Aplicación

### Arquitectura del Sistema

#### 1. **Módulo de Carga** (`parser/loader.py`)

- **Propósito**: Cargar y validar configuraciones de Máquinas de Turing desde archivos YAML

- **Funcionalidades**:
  - Lectura de archivos YAML con encoding UTF-8
  - Validación de estructura completa (estados, alfabetos, función de transición)
  - Verificación de estados inicial y final
  - Manejo de errores descriptivos para configuraciones inválidas

#### 2. **Módulo de Máquina de Turing** (`core/turing_machine.py`)

- **Propósito**: Representar formalmente una Máquina de Turing con sus componentes

- **Componentes modelados**:
  1. **Conjunto de estados (Q)**: Lista de todos los estados posibles
  2. **Estado inicial (q₀)**: Estado de inicio de la computación
  3. **Estado final (F)**: Estado(s) de aceptación
  4. **Alfabeto de entrada (Σ)**: Símbolos válidos en la entrada
  5. **Alfabeto de la cinta (Γ)**: Todos los símbolos que pueden aparecer en la cinta
  6. **Función de transición (δ)**: Diccionario optimizado para acceso rápido
  7. **Memoria cache**: Estado adicional para cálculos complejos

#### 3. **Módulo de Cinta** (`core/tape.py`)

- **Propósito**: Modelar la cinta infinita de la Máquina de Turing

- **Funcionalidades**:
  - **Expansión dinámica**: La cinta crece automáticamente hacia izquierda y derecha
  - **Cabezal de lectura/escritura**: Posición actual en la cinta
  - **Operaciones básicas**: `read()`, `write()`, `move()`
  - **Símbolo blanco**: Representa celdas vacías (configurable)
  - **Movimientos**: Izquierda (L), Derecha (R), Sin movimiento (S)

#### 4. **Módulo de Simulación** (`core/simulation.py`)

- **Propósito**: Ejecutar la simulación y generar registros detallados

- **Funcionalidades**:
  - **Ejecución paso a paso**: Aplica transiciones secuencialmente
  - **Notación formal**: Registra cada transición como δ([q, c], a) = ([q', c'], b, D)
  - **Descripciones instantáneas**: Genera IDs mostrando configuración completa
  - **Detección de aceptación**: Identifica cuando se alcanza el estado final
  - **Detección de rechazo**: Identifica configuraciones sin transición válida
  - **Logging estructurado**: Genera archivos de salida con formato legible

#### 5. **Módulo de Configuración** (`config.py`)

- **Propósito**: Centralizar parámetros y constantes del sistema

- **Parámetros configurables**:
  - `CONFIGURACION`: Ruta al archivo YAML de la máquina
  - `OUTPUT_DIR`: Directorio donde se guardan los resultados
  - `PRINT_RESULT`: Mostrar el resultado final en la cinta
  - `PRINT_LENGTH`: Mostrar la longitud del resultado (útil para verificar Fibonacci)

#### 6. **Módulo Principal** (`main.py`)

- **Propósito**: Punto de entrada y orquestación del sistema

- **Flujo de ejecución**:
  1. Carga la configuración desde el archivo especificado en `config.py`
  2. Inicializa la Máquina de Turing
  3. Crea el simulador
  4. Ejecuta cada número de entrada (en notación unaria)
  5. Genera archivos de salida con el cálculo de cada término
  6. Opcionalmente muestra el resultado y su longitud

## Estructura del Proyecto

```bash
CC3041-Proyecto-1/
│
├── machines/                 # Archivos de configuración de máquinas
│   ├── fibonacci_config.yaml # MT para calcular la sucesión de Fibonacci
│   ├── config1.yaml          # MT alternativa 1
│   └── config2.yaml          # MT alternativa 2
│
├── core/                     # Módulos principales del simulador
│   ├── __init__.py           # Inicialización del paquete
│   ├── turing_machine.py     # Definición formal de la MT
│   ├── tape.py               # Implementación de la cinta infinita
│   └── simulation.py         # Motor de simulación y logging
│
├── parser/                   # Módulo de carga de configuración
│   ├── __init__.py           # Inicialización del paquete
│   └── loader.py             # Carga y validación de archivos YAML
│
├── outputs/                  # Directorio de salida (generado automáticamente)
│   ├── simulation_1.txt      # Fibonacci(1) = 1
│   ├── simulation_2.txt      # Fibonacci(2) = 1
│   ├── simulation_3.txt      # Fibonacci(3) = 2
│   └── ...                   # Más resultados
│
├── config.py                 # Configuración centralizada del sistema
├── main.py                   # Punto de entrada principal
└── README.md                 # Documentación del proyecto
```

## Formato de Configuración YAML

La Máquina de Turing para Fibonacci se define mediante un archivo YAML con la siguiente estructura:

```yaml
---
# Definición de estados
q_states:
  q_list:                     # Lista de todos los estados (0-9)
    - '0'
    - '1'
    - '2'
    # ... estados intermedios
    - '9'
  initial: '0'                # Estado inicial
  final: '9'                  # Estado de aceptación

# Alfabeto de entrada (notación unaria)
alphabet:
  - '1'                       # Representa números en unario

# Alfabeto de la cinta (incluye símbolos auxiliares)
tape_alphabet:
  - '1'                       # Unidades
  - Z                         # Separador de secciones
  - A                         # Marcador auxiliar 1
  - B                         # Marcador auxiliar 2
  - C                         # Marcador auxiliar 3
  - X                         # Marcador temporal 1
  - Y                         # Marcador temporal 2
  -                           # Símbolo blanco (vacío)

# Función de transición δ
delta:
  - params:                   # Configuración actual
      initial_state: '0'
      mem_cache_value:        # Valor en cache (null = B)
      tape_input: '1'         # Símbolo leído
    output:                   # Nueva configuración
      final_state: '1'
      mem_cache_value:        # Nuevo valor en cache
      tape_output:            # Símbolo a escribir (null = B)
      tape_displacement: R    # Movimiento: L, R, S

  # ... más transiciones (380+ líneas) ...

# Números de Fibonacci a calcular (en notación unaria)
simulation_strings:
  - 1                         # F(1) = 1
  - 11                        # F(2) = 1
  - 111                       # F(3) = 2
  - 1111                      # F(4) = 3
  - 11111                     # F(5) = 5
  - 111111                    # F(6) = 8
```

## Ejecución del Programa

### Instalación y Configuración

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/Tunchxz/CC3041-Proyecto-1.git
cd CC3041-Proyecto-1
```

#### 2. Instalar Dependencias

```bash
# Instalar PyYAML para procesamiento de archivos de configuración
pip install pyyaml
```

#### 3. Configurar Parámetros (Opcional)

Puedes editar [config.py](config.py) para ajustar el comportamiento del simulador:

```python
# Ruta del archivo de configuración de la Máquina de Turing
CONFIGURACION = "machines/fibonacci_config.yaml"

# Ruta del directorio de salida para los resultados
OUTPUT_DIR = "outputs"

# --- Configuraciones para máquinas que generan cadenas ---

# Imprimir cadena resultante en el archivo de salida
PRINT_RESULT = True

# Imprimir longitud de la cadena resultante (útil para verificar Fibonacci)
# Requiere PRINT_RESULT = True
PRINT_LENGTH = True
```

#### 4. Ejecutar el Simulador

```bash
# Ejecutar desde el directorio del proyecto
python main.py
```

#### 5. Revisar Resultados

Los archivos de salida se generan automáticamente en el directorio `outputs/`:

```bash
# Ver el resultado de la primera simulación
cat outputs/simulation_1.txt
```

## Formato de Salida

Cada archivo de simulación contiene:

1. **Encabezado**: Indica el número de entrada (en notación unaria) que se está calculando
2. **Transiciones**: Registro formal de cada paso con:
   - Función δ aplicada: `δ([estado, cache], símbolo) = ([nuevo_estado, nuevo_cache], escritura, movimiento)`
   - ID antes de la transición: Configuración completa de la máquina
   - ID después de la transición: Nueva configuración
3. **Resultado final**: Muestra el término de Fibonacci calculado y su longitud

### Ejemplo de Salida

Para calcular F(4) = 3:

```
--------------------------------------------------
Simulación para la cadena: 1111
--------------------------------------------------

Para esta cadena, las transiciones son:

δ([0, B], 1) = ([1, B], B, R)        [0,B]1111            ⊢   B[1,B]111
δ([1, B], 1) = ([1, B], 1, R)        B[1,B]111            ⊢   B1[1,B]11
δ([1, B], 1) = ([1, B], 1, R)        B1[1,B]11            ⊢   B11[1,B]1
...
δ([7, B], 1) = ([7, B], 1, R)        BBBB0[7,B]11B        ⊢   BBBB01[7,B]1B
δ([7, B], 1) = ([7, B], 1, R)        BBBB01[7,B]1B        ⊢   BBBB011[7,B]B
δ([8, B], B) = ([9, B], B, L)        BBBB011[8,B]B        ⊢   BBBB01[9,B]1B

----------------------------------------
RESULTADO FINAL: 1111 = 4

Cadena ACEPTADA ✔
----------------------------------------
```

## Solución de Problemas Comunes

### Error: "No module named 'yaml'"

```bash
# Instalar la dependencia faltante
pip install pyyaml
```

### **Error: "FileNotFoundError: machines/fibonacci_config.yaml"**

- Verifica que el archivo de configuración existe en el directorio `machines/`
- Revisa que el nombre del archivo en [config.py](config.py) sea correcto
- Asegurate de ejecutar desde el directorio raíz del proyecto

### **Error: "ValueError: La configuración no contiene 'delta'"**

- Revisa que tu archivo YAML tenga todos los campos requeridos:
  - `q_states` (con `initial` y `final`)
  - `alphabet`
  - `tape_alphabet`
  - `delta`
  - `simulation_strings`

### **Error: "ValueError: Movimiento no válido"**

- Los movimientos válidos en la función de transición son:
  - `L`: Izquierda
  - `R`: Derecha
  - `S`: Sin movimiento

## Sucesión de Fibonacci

La **sucesión de Fibonacci** se define como:

- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) para n ≥ 2

Los primeros términos son: **0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89...**

### Representación Unaria

La máquina utiliza notación unaria para representar números:

- `1` = 1 (un "1")
- `11` = 2 (dos "1"s)
- `111` = 3 (tres "1"s)
- `1111` = 4 (cuatro "1"s)
- Y así sucesivamente...

### Ejemplos de Cálculos

| Entrada | Representa | Fibonacci | Salida (longitud) |
|---------|------------|-----------|-------------------|
| `1`     | F(1)       | 1         | 1 "1"             |
| `11`    | F(2)       | 1         | 1 "1"             |
| `111`   | F(3)       | 2         | 2 "1"s            |
| `1111`  | F(4)       | 3         | 3 "1"s            |
| `11111` | F(5)       | 5         | 5 "1"s            |
| `111111`| F(6)       | 8         | 8 "1"s            |

### Modificando las Entradas

Para calcular diferentes términos de Fibonacci:

1. Edita [machines/fibonacci_config.yaml](machines/fibonacci_config.yaml)
2. Modifica la sección `simulation_strings` al final del archivo
3. Añade más cadenas unarias (ej: `1111111` para F(7) = 13)
4. Ejecuta el simulador y revisa los resultados en `outputs/`
