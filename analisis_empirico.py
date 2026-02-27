"""
Análisis Empírico de la Máquina de Turing - Fibonacci

Este script realiza un análisis empírico del rendimiento de la máquina de Turing
que calcula la sucesión de Fibonacci.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import os

# Importar módulos del proyecto
from parser.loader import MTConfigLoader
from core.turing_machine import TuringMachine
from core.simulation import Simulator


def medir_tiempo_ejecucion(machine, input_str, repeticiones=5):
    """
    Mide el tiempo de ejecución de la máquina de Turing para una entrada dada.
    
    Args:
        machine: Instancia de TuringMachine
        input_str: Cadena de entrada en notación unaria
        repeticiones: Número de veces a repetir la medición
    
    Returns:
        tuple: (tiempo_promedio, tiempo_min, tiempo_max, pasos, resultado)
    """
    tiempos = []
    simulator = Simulator(machine)
    
    # Realizar mediciones
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        accepted, log_lines, final_tape = simulator.run_string(input_str)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    
    # Contar pasos (número de transiciones)
    _, log_lines, _ = simulator.run_string(input_str)
    pasos = sum(1 for line in log_lines if '⊢' in line)
    
    # Obtener resultado final
    accepted, _, final_tape = simulator.run_string(input_str)
    resultado_longitud = len([s for s in final_tape.tape if s == '1'])
    
    return (
        np.mean(tiempos),
        np.min(tiempos),
        np.max(tiempos),
        pasos,
        resultado_longitud
    )


def ajustar_regresion_polinomial(x, y, grado):
    """
    Ajusta un modelo de regresión polinomial a los datos.
    
    Args:
        x: Variable independiente (tamaño de entrada)
        y: Variable dependiente (tiempo o pasos)
        grado: Grado del polinomio
    
    Returns:
        tuple: (modelo, poly_features, r2, mse, y_pred)
    """
    X = x.reshape(-1, 1)
    
    # Crear características polinomiales
    poly_features = PolynomialFeatures(degree=grado)
    X_poly = poly_features.fit_transform(X)
    
    # Entrenar modelo
    modelo = LinearRegression()
    modelo.fit(X_poly, y)
    
    # Predecir
    y_pred = modelo.predict(X_poly)
    
    # Calcular métricas
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    
    return modelo, poly_features, r2, mse, y_pred


def obtener_ecuacion_polinomial(modelo, poly_features):
    """
    Genera la ecuación del polinomio ajustado.
    
    Args:
        modelo: Modelo LinearRegression entrenado
        poly_features: PolynomialFeatures usado
    
    Returns:
        str: Ecuación del polinomio
    """
    coefs = modelo.coef_
    intercept = modelo.intercept_
    
    terminos = []
    
    # Término constante
    if abs(intercept) > 1e-10:
        terminos.append(f"{intercept:.6f}")
    
    # Términos con x
    for i in range(1, len(coefs)):
        coef = coefs[i]
        if abs(coef) > 1e-10:
            if i == 1:
                terminos.append(f"{coef:.6f}*n")
            else:
                terminos.append(f"{coef:.6f}*n^{i}")
    
    ecuacion = " + ".join(terminos)
    ecuacion = ecuacion.replace("+ -", "- ")
    
    return ecuacion


def main():
    """Función principal del análisis empírico."""
    
    print("="*80)
    print("        ANÁLISIS EMPÍRICO - MÁQUINA DE TURING FIBONACCI")
    print("="*80)
    
    # Cargar la configuración de la máquina de Turing
    print("\n1. Cargando máquina de Turing...")
    loader = MTConfigLoader("machines/fibonacci_config.yaml")
    config = loader.load()
    machine = TuringMachine(config)
    print("   [OK] Máquina cargada exitosamente.")
    
    # Generar entradas de prueba (n = 0 a 15)
    print("\n2. Generando entradas de prueba...")
    entradas_prueba = []
    for n in range(0, 16):
        entrada = '1' * n if n > 0 else ''
        entradas_prueba.append((n, entrada))
    print(f"   [OK] Se ejecutarán {len(entradas_prueba)} pruebas (n = 0 a 15)")
    
    # Ejecutar mediciones
    print("\n3. Ejecutando mediciones...")
    print("="*80)
    print(f"{'n':<5} {'Entrada':<15} {'Tiempo (ms)':<15} {'Pasos':<10} {'Fib(n)':<10}")
    print("="*80)
    
    resultados = []
    for n, entrada in entradas_prueba:
        tiempo_prom, tiempo_min, tiempo_max, pasos, fib_n = medir_tiempo_ejecucion(
            machine, entrada, repeticiones=5
        )
        
        resultados.append({
            'n': n,
            'entrada': entrada if entrada else '(vacío)',
            'longitud_entrada': n,
            'tiempo_promedio': tiempo_prom,
            'tiempo_min': tiempo_min,
            'tiempo_max': tiempo_max,
            'pasos': pasos,
            'fibonacci_n': fib_n
        })
        
        print(f"{n:<5} {entrada if entrada else '(vacío)':<15} "
            f"{tiempo_prom*1000:<15.4f} {pasos:<10} {fib_n:<10}")
    
    print("="*80)
    print("   [OK] Mediciones completadas.")
    
    # Crear DataFrame
    df_resultados = pd.DataFrame(resultados)
    
    # Preparar datos para regresión
    x = df_resultados['longitud_entrada'].values
    y_tiempo = df_resultados['tiempo_promedio'].values * 1000  # ms
    y_pasos = df_resultados['pasos'].values
    
    # Análisis de regresión para tiempo
    print("\n4. Realizando regresión polinomial para TIEMPO DE EJECUCIÓN...")
    print("="*80)
    
    grados = [1, 2, 3, 4, 5]
    resultados_regresion = []
    
    for grado in grados:
        modelo, poly_features, r2, mse, y_pred = ajustar_regresion_polinomial(
            x, y_tiempo, grado
        )
        ecuacion = obtener_ecuacion_polinomial(modelo, poly_features)
        
        resultados_regresion.append({
            'grado': grado,
            'r2': r2,
            'mse': mse,
            'modelo': modelo,
            'poly_features': poly_features,
            'y_pred': y_pred,
            'ecuacion': ecuacion
        })
        
        print(f"\n   Grado {grado}:")
        print(f"   R² = {r2:.6f}")
        print(f"   MSE = {mse:.6f}")
        print(f"   Ecuación: y = {ecuacion}")
    
    mejor_modelo = max(resultados_regresion, key=lambda x: x['r2'])
    print(f"\n   MEJOR MODELO: Polinomio de grado {mejor_modelo['grado']}")
    print(f"      R² = {mejor_modelo['r2']:.6f}")
    print(f"      Ecuación: y = {mejor_modelo['ecuacion']}")
    
    # Análisis de regresión para pasos
    print("\n5. Realizando regresión polinomial para NÚMERO DE PASOS...")
    print("="*80)
    
    resultados_pasos = []
    for grado in grados:
        modelo, poly_features, r2, mse, y_pred = ajustar_regresion_polinomial(
            x, y_pasos, grado
        )
        ecuacion = obtener_ecuacion_polinomial(modelo, poly_features)
        
        resultados_pasos.append({
            'grado': grado,
            'r2': r2,
            'mse': mse,
            'modelo': modelo,
            'poly_features': poly_features,
            'y_pred': y_pred,
            'ecuacion': ecuacion
        })
        
        print(f"\n   Grado {grado}:")
        print(f"   R² = {r2:.6f}")
        print(f"   MSE = {mse:.6f}")
    
    mejor_modelo_pasos = max(resultados_pasos, key=lambda x: x['r2'])
    print(f"\n   MEJOR MODELO: Polinomio de grado {mejor_modelo_pasos['grado']}")
    print(f"      R² = {mejor_modelo_pasos['r2']:.6f}")
    
    # Crear visualizaciones
    print("\n6. Generando visualizaciones...")
    os.makedirs("outputs", exist_ok=True)
    
    # Configuración de estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Gráfico 1: Diagrama de dispersión
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Tiempo vs Tamaño
    ax1.scatter(x, y_tiempo, s=100, alpha=0.6, c='steelblue', 
                edgecolors='black', linewidth=1.5)
    ax1.set_xlabel('Tamaño de entrada (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tiempo de ejecución (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Tiempo de ejecución vs Tamaño de entrada', 
                fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Pasos vs Tamaño
    ax2.scatter(x, y_pasos, s=100, alpha=0.6, c='coral', 
                edgecolors='black', linewidth=1.5)
    ax2.set_xlabel('Tamaño de entrada (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Número de pasos (transiciones)', fontsize=12, fontweight='bold')
    ax2.set_title('Número de pasos vs Tamaño de entrada', 
                fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/diagrama_dispersion.png', dpi=300, bbox_inches='tight')
    print("   [OK] Guardado: outputs/diagrama_dispersion.png")
    
    # Gráfico 2: Regresiones polinomiales
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    x_smooth = np.linspace(x.min(), x.max(), 300)
    
    for i, resultado in enumerate(resultados_regresion):
        ax = axes[i]
        
        # Datos originales
        ax.scatter(x, y_tiempo, s=100, alpha=0.6, c='steelblue',
                edgecolors='black', linewidth=1.5, label='Datos reales', zorder=3)
        
        # Curva de regresión
        X_smooth = x_smooth.reshape(-1, 1)
        X_smooth_poly = resultado['poly_features'].transform(X_smooth)
        y_smooth = resultado['modelo'].predict(X_smooth_poly)
        
        ax.plot(x_smooth, y_smooth, 'r-', linewidth=2.5,
                label=f'Regresión grado {resultado["grado"]}', zorder=2)
        
        ax.set_xlabel('Tamaño de entrada (n)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Tiempo (ms)', fontsize=11, fontweight='bold')
        ax.set_title(f'Polinomio grado {resultado["grado"]} (R²={resultado["r2"]:.4f})',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=9)
    
    axes[5].axis('off')
    
    plt.tight_layout()
    plt.savefig('outputs/regresiones_polinomiales.png', dpi=300, bbox_inches='tight')
    print("   [OK] Guardado: outputs/regresiones_polinomiales.png")
    
    # Resumen final
    print("\n" + "="*80)
    print("                        RESUMEN DEL ANÁLISIS")
    print("="*80)
    
    print("\nESTADÍSTICAS GENERALES:")
    print(f"   - Rango de prueba: n = 0 a {max(x)}")
    print(f"   - Tiempo mínimo: {min(y_tiempo):.4f} ms")
    print(f"   - Tiempo máximo: {max(y_tiempo):.4f} ms")
    print(f"   - Pasos mínimos: {min(y_pasos)}")
    print(f"   - Pasos máximos: {max(y_pasos)}")
    
    print("\nMEJOR AJUSTE PARA TIEMPO:")
    print(f"   - Grado: {mejor_modelo['grado']}")
    print(f"   - R²: {mejor_modelo['r2']:.6f}")
    print(f"   - Complejidad: O(n^{mejor_modelo['grado']})")
    
    print("\nMEJOR AJUSTE PARA PASOS:")
    print(f"   - Grado: {mejor_modelo_pasos['grado']}")
    print(f"   - R²: {mejor_modelo_pasos['r2']:.6f}")
    print(f"   - Complejidad: O(n^{mejor_modelo_pasos['grado']})")
    
    print("\n" + "="*80)
    print("[OK] Análisis empírico completado exitosamente.")
    print("="*80)
    
    # Guardar resultados en CSV
    df_resultados.to_csv('outputs/resultados_analisis.csv', index=False)
    print("\nResultados guardados en: outputs/resultados_analisis.csv")


if __name__ == "__main__":
    main()
