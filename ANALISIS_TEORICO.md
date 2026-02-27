# Análisis Teórico de Complejidad: Máquina de Turing - Fibonacci

Esta Máquina de Turing (MT) calcula el n-ésimo término de la sucesión de Fibonacci en **notación unaria**, donde:  

- **Entrada:** n repeticiones del símbolo '1' (representa el número n)  

- **Salida:** F(n) repeticiones del símbolo '1' (representa el número de Fibonacci F(n))  

La salida no es un valor numérico tradicional, sino una secuencia de símbolos cuya longitud es el Fibonacci deseado.

## Sobre el Algoritmo

La idea detrás de esta máquina es simular el cálculo secuencial de la serie de Fibonacci usando grupos de símbolos en la cinta para representar los términos de la serie que ya se han producido. Para mantener un registro de los valores previos y generar el siguiente, la solución usa símbolos con distintos significados:  

- El símbolo `Z` se usa como un indicador de casos base.  

- Los símbolos `A`, `V`, `C` en la cinta representan longitudes parciales de la serie de Fibonacci generada hasta ese momento.  

- Los símbolos `X` y `Y` se usan temporalmente como marcas para saber qué partes de esos grupos ya se han copiado en el proceso de generar el siguiente término.

### Pseudocódigo

```
Algoritmo Fibonacci_Unario(cadenaEntrada)

    // Paso 1: determinar n (longitud de la entrada unaria)
    n ← longitud(cadenaEntrada)

    // Casos base según definición estándar
    si n = 1 entonces
        retornar "1"

    si n = 2 entonces
        retornar "1"

    // Paso 2: inicializar los dos primeros términos reales
    F_prev2 ← "1"   // F(1)
    F_prev1 ← "1"   // F(2)

    // Paso 3: iterar desde 3 hasta n
    para i desde 3 hasta n hacer

        // Suma en unario = concatenación
        F_actual ← concatenar(F_prev1, F_prev2)

        // Desplazar ventana
        F_prev2 ← F_prev1
        F_prev1 ← F_actual

    fin para

    retornar F_prev1

Fin Algoritmo
```

### Explicación  

El ciclo principal procede así:

#### 1. Inicialización

El primer y segundo ciclo (cuando el contador todavía no ha generado nada) simplemente escribe `Z`, que luego se transforma en `1`, para representar $ F(1) = 1 $ y $ F(2) = 1 $.  

#### 2. Ciclo general (a partir del tercero)

En la cinta se tiene un patrón parecido a `Z11AAVVV`, donde:  

   - `Z` es el inicio,
   - el grupo de `A`s representa el término anterior $ F_{k-2} $,
   - el grupo de `V`'s representa el término anterior inmediato $ F_{k-1}) $.  

Los subíndices `A` y `V` no importan por sí mismos sino porque su cantidad refleja la longitud de las cifras previas. 

Para generar $ F_{k} = F_{k-1} + F_{k-2} $, la máquina:    

- copia todos las `A`s y `V`s en la cinta al final de la secuencia actual para formar un nuevo grupo de `C`s de longitud igual a la suma de los tamaños de los dos grupos anteriores;  

- Luego usa marcas `X` y `Y` para indicar qué símbolos ya se han leído y copiado.  

- Después de terminar la copia, transforma esos marcadores `(X,Y)` de vuelta a sus valores originales.  

- Finalmente decrementa o ‘normaliza’ los símbolos `A`, `V`, `C` a la base `1` para representar de forma uniforme la nueva secuencia.  

#### 3. Terminación

- Este ciclo se repite tantas veces como unos haya en la entrada original (cada uno de esos representa un incremento del índice de Fibonacci).  

- Cuando se han procesado todos los unos de la entrada original, la máquina reemplaza todos los símbolos intermedios `(A,V)` por `1`s, obteniendo la salida unaria final cuyo tamaño total es el número Fibonacci deseado.

## Análisis de Complejidad

### 1. Observación preliminar importante

La entrada es un número en notación unaria. Si la cadena tiene longitud `n`, entonces el algoritmo calcula `F(n)`.  

En representación unaria:  

    longitud(F(k) en unario) = F(k)

Y sabemos que la sucesión de Fibonacci crece exponencialmente ([Marshall, 2024](https://www.baeldung.com/cs/fibonacci-computational-complexity)).  

Esto afecta directamente el costo de la concatenación.

### 2. Asignación de costos

Sea:

- Determinar longitud → costo `c1`
- Comparaciones de casos base → costo `c2`
- Inicializaciones → costo `c3`
- Control del ciclo → costo `c4`
- Asignaciones simples → costo `c5`
- Copiar un símbolo en concatenación → costo `c6`

### 3. Conteo de ejecuciones

**Paso 1**  

Se ejecuta una vez: $ c_{1} $.

**Casos base**

Dos comparaciones: $ 2c_{2} $

**Inicializaciones**

Dos asignaciones: $ 2c_{3} $

### 4. Análisis del ciclo principal

El ciclo va desde `i = 3` hasta `n`.

Número de iteraciones:

    n - 2

En cada iteración se ejecutan:

- Una concatenación
- Dos asignaciones simples
- Control del ciclo

### 5. Costo de la concatenación

En la iteración `i`:

- `F_prev1` contiene `F(i-1)`
- `F_prev2` contiene `F(i-2)`

La longitud del resultado es:

    F(i-1) + F(i-2) = F(i)

Por lo tanto, el costo de concatenar en la iteración `i` es:

    c6 * F(i)

### 6. Tiempo total

El tiempo total es:

    T(n) =
        c1 + 2c2 + 2c3
        + Σ(i=3 hasta n) ( c4 + 2c5 + c6 F(i) )

Separando términos:

    T(n) =
        C
        + C'(n-2)
        + c6 Σ(i=3 hasta n) F(i)

El término dominante es:

    Σ F(i)

### 7. Evaluación de la suma de Fibonacci

Propiedad conocida:

    Σ(i=1 hasta n) F(i) = F(n+2) - 1

Por lo tanto:

    Σ(i=3 hasta n) F(i) ≤ F(n+2) - 1

Entonces:

    T(n) = O(F(n))

### 8. Crecimiento de Fibonacci

Se sabe que:

    F(n) = Θ(2^n)

Por lo tanto:

    T(n) = Θ(2^n)

# Conclusión Final

El algoritmo tiene complejidad: $ Θ(2^n) $

Aunque el algoritmo es iterativo y contiene un solo ciclo, el tamaño de los datos crece exponencialmente en notación unaria.

El costo dominante proviene de la concatenación de cadenas cuyo tamaño es exponencial.

Por lo tanto, el tiempo total también es exponencial.

## Referencias

1. **Computational complexity of Fibonacci sequence** - Baeldung on Computer Science: https://www.baeldung.com/cs/fibonacci-computational-complexity  

2. **Fibonacci Sequence** - Wikipedia: https://es.wikipedia.org/wiki/Sucesi%C3%B3n_de_Fibonacci

3. **Computational complexity of Fibonacci Sequence** - StackOverflow: https://stackoverflow.com/questions/360748/computational-complexity-of-fibonacci-sequence
