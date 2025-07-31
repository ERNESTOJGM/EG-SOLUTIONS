import numpy as np
import matplotlib.pyplot as plt

# Parámetros del pozo
p_res = 3000  # Presión del yacimiento (psi)
tasa_corte = 300  # Producción mínima rentable (bpd)

# Tasas de declinación y sus producciones máximas
tasas_declinacion = [0.15, 0.25, 0.35, 0.55, 0.75]
producciones_maximas = [5000, 4500, 4000, 3500, 3000]  # Producción inicial para cada tasa de declinación

# Gráfica del perfil IPR
plt.figure(figsize=(10, 6))
plt.axhline(y=tasa_corte, color='r', linestyle='--', label=f'Tasa de corte: {tasa_corte} bpd')

# Iterar sobre cada tasa de declinación con su producción máxima correspondiente
for tasa, q_max in zip(tasas_declinacion, producciones_maximas):
    # Cálculo del perfil IPR con la producción máxima específica
    p_wf_values = np.linspace(0, p_res, 50)
    q_values = q_max * (1 - 0.2 * (p_wf_values / p_res) - 0.8 * (p_wf_values / p_res) ** 2)

    # Calcular el límite económico del pozo
    tiempo = 0
    produccion_actual = q_max
    produccion_vs_tiempo = [produccion_actual]

    while produccion_actual > tasa_corte:
        tiempo += 1
        produccion_actual *= (1 - tasa)  # Declinación exponencial
        produccion_vs_tiempo.append(produccion_actual)

    plt.plot(range(tiempo + 1), produccion_vs_tiempo, label=f'Declinación {int(tasa * 100)}% - q_max {q_max} bpd')

# Configuración del gráfico
plt.xlabel('Años')
plt.ylabel('Producción (bpd)')
plt.title('Curvas de Declinación del Pozo con Diferentes Producciones Máximas')
plt.legend()
plt.grid(True)
plt.show()
