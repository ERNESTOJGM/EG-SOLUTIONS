import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def calcular_declinacion_exponencial(q_inicial, tasa_declinacion_anual, tasa_corte, paso_tiempo=1/12):
   
   
    # Se aplica la fórmula de declinación exponencial hasta alcanzar una tasa de corte
   
    tiempo = 0
    produccion_actual = q_inicial
    resultados = {'tiempo': [0], 'produccion': [produccion_actual]}
    
    while produccion_actual > tasa_corte:
        tiempo += paso_tiempo
        produccion_actual = q_inicial * np.exp(-tasa_declinacion_anual * tiempo)
        resultados['tiempo'].append(tiempo)
        resultados['produccion'].append(produccion_actual)
    
    return resultados

def plot_curvas_declinacion(tasas_declinacion, producciones_maximas, p_yac, tasa_corte):
   
    # Generación de los gráficos de las curvas de declinación
   
    plt.figure(figsize=(12, 7))
    ax = plt.gca()
    
    # Diseño del estilo para los gráficos
    
    plt.axhline(y=tasa_corte, color='r', linestyle='--', 
                linewidth=1.5, label=f'Tasa de corte: {tasa_corte} bpd')
    
    # Colores para una mejor visualización de las curvas
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(tasas_declinacion)))
    
    for i, (tasa, q_max) in enumerate(zip(tasas_declinacion, producciones_maximas)):
        
        # Calcular curva de declinación
        resultados = calcular_declinacion_exponencial(q_max, tasa, tasa_corte)
        
        # Cáculo del límite económico del pozo
        
        lim_econ = resultados['tiempo'][-1]
        prod_acumulada = np.trapz(resultados['produccion'], resultados['tiempo'])
        
        # Gráficos
        label = (f'Declinación {tasa*100:.0f}% - q_max {q_max} bpd\n'
                 f'Límite Econóico: {lim_econ:.1f} años')
        plt.plot(resultados['tiempo'], resultados['produccion'], 
                color=colors[i], linewidth=2, label=label)
        
        # Mostrar los puntos en la gráfica
        plt.scatter(lim_econ, tasa_corte, color=colors[i], s=80, zorder=5)
    
    # Descripción de los ejes del gráfico
    plt.title('Curvas de Declinación de Producción\n', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo: Años', fontsize=12)
    plt.ylabel('Producción:BPD', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    
    # Configuración de los ejes
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    ax.grid(which='minor', linestyle='-', linewidth='0.5', color='lightgray')
    
    plt.tight_layout()
    plt.show()

# Colocar los parámetros del pozo:
p_yac = 3000  # Es Presión del yacimiento (psi)
tasa_corte = 180  # Producción mínima rentable (bpd)

# Tasas de declinación y sus producciones máximas
tasas_declinacion = [0.17, 0.28, 0.34, 0.59, 0.84]
producciones_maximas = [2500, 2100, 1800, 1200, 650]

# Validamos los Datos
if len(tasas_declinacion) != len(producciones_maximas):
    raise ValueError("Para cada Tasa de Declinación debe Existir una Tasa de Producción Máxima")

# Generar gráfico
plot_curvas_declinacion(tasas_declinacion, producciones_maximas, p_yac, tasa_corte)