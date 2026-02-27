# Análisis Empírico - Máquina de Turing Fibonacci

Este directorio contiene scripts para realizar un análisis empírico del rendimiento de la Máquina de Turing que calcula la sucesión de Fibonacci.


## Características del Análisis

El análisis incluye:

1. **Listado de entradas de prueba**: Cadenas en notación unaria de diferentes tamaños (n = 0 a 15)
2. **Medición de tiempos**: Tiempo de ejecución promedio, mínimo y máximo para cada entrada
3. **Diagrama de dispersión**: Visualización de tiempos vs tamaño de entrada
4. **Regresión polinomial**: Ajuste de modelos polinomiales (grados 1-5) para predecir tiempos
5. **Análisis de complejidad**: Determinación de la complejidad computacional basada en el mejor ajuste

## Cómo Ejecutar

Instala las dependencias necesarias:

```bash
pip install numpy matplotlib pandas scikit-learn
```

Corre el script con:

```bash
python analisis_empirico.py
```

## Resultados Generados

El análisis genera los siguientes archivos en el directorio `outputs/`:

1. **diagrama_dispersion.png**
   - Gráfico de tiempo vs tamaño de entrada
   - Gráfico de pasos vs tamaño de entrada

2. **regresiones_polinomiales.png**
   - Comparación de 5 modelos de regresión polinomial (grados 1-5)
   - Curvas de ajuste superpuestas a los datos reales

3. **resultados_analisis.csv**
   - Tabla completa con todos los datos medidos

## Interpretación de Resultados

### Coeficiente R² (R-squared)
- Mide qué tan bien el modelo explica la variabilidad de los datos
- Rango: 0 a 1
- **Interpretación**:
  - R² ≈ 1.0: Excelente ajuste
  - R² ≈ 0.9: Buen ajuste
  - R² < 0.7: Ajuste pobre

### Error Cuadrático Medio (MSE)
- Mide el error promedio de las predicciones
- Valores más bajos = mejor ajuste
- Unidades: (millisegundos)²

### Complejidad Computacional
- Si el mejor modelo es de grado **d**, la complejidad es **O(n^d)**
- Ejemplos:
  - Grado 1 → O(n) - Lineal
  - Grado 2 → O(n²) - Cuadrática
  - Grado 3 → O(n³) - Cúbica

## Personalización

### Cambiar el rango de entradas

En el script modifica:

```python
# Original: n = 0 a 15
for n in range(0, 16):

# Nuevo: n = 0 a 20
for n in range(0, 21):
```

### Cambiar el número de repeticiones

```python
# Original: 5 repeticiones
medir_tiempo_ejecucion(machine, entrada, repeticiones=5)

# Nuevo: 10 repeticiones (más preciso pero más lento)
medir_tiempo_ejecucion(machine, entrada, repeticiones=10)
```

### Cambiar los grados de polinomio a probar

```python
# Original: grados 1-5
grados = [1, 2, 3, 4, 5]

# Nuevo: grados 1-7
grados = [1, 2, 3, 4, 5, 6, 7]
```

## Ejemplo de Salida

```
================================================================================
n     Entrada         Tiempo (ms)     Pasos      Fib(n)    
================================================================================
0     (vacío)         0.1234          45         1         
1     1               0.2456          89         1         
2     11              0.4321          156        2         
3     111             0.8765          278        3         
...
================================================================================

MEJOR MODELO: Polinomio de grado 3
   R² = 0.998765
   Ecuación: y = 0.123456*n + 0.234567*n^2 + 0.345678*n^3
```

## Notas Importantes

1. **Tiempo de ejecución**: El análisis completo puede tomar varios minutos dependiendo del rango de entradas
2. **Memoria**: Entradas grandes (n > 20) pueden consumir mucha memoria
3. **Precisión**: Los tiempos de ejecución pueden variar según la carga del sistema
4. **Gráficos**: Se requieren las librerías matplotlib para generar visualizaciones
