# Para mas información visite el siguiente enlace: https://github.com/xdf-modules/pyxdf

import pyxdf
import matplotlib.pyplot as plt
import numpy as np
import pprint
import configparser

# Estilo de visualización de gráficos en matplotlib
plt.style.use('classic')

# Fichero de configuración, lectura de parámetros
CONFIG_FILE = 'config.conf'
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
# Variables de lectura
ob_delay = float(config['DEFAULT']['period'])  # Periodo de marcadores
n = int(config['DEFAULT']['samples'])          # Numero de muestras a visualizar

# Lectura de fuentes y asignación de variables 
m_data, m_header = pyxdf.load_xdf('./test_files/markers/test.xdf')
# t_data, t_header = pyxdf.load_xdf('./test_files/triggers/test.xdf')

# Contenido del fichero de datos .xdf (en caso de existir un archivo de)
content_name = 'data_content.md'
with open('./out_files/'+ content_name, 'w') as fp:
    pprint.pprint(m_data, stream = fp)


# LSL Markers
#  ---------------------------------------------------------------------------------------
m_delay = [] # Lista de retardos entre pares de valores en alto (LSL Markers)

for stream in m_data:
    m_y = stream['time_series']
    m_t = stream['time_stamps']
    HIGH_V = np.where(m_y == 1)

    for index in range(len(HIGH_V[0])-1):
        m_marker = [m_t[HIGH_V[0][index+1]] - m_t[HIGH_V[0][index]]]
        m_delay.append(m_marker)

    # Parámetros temporales de análisis
    m_delay = np.array(m_delay)
    m_jitter = np.mean(m_delay - ob_delay)
    m_delay_var = np.var(m_delay)

    # Resultados
    print("[LSL Markers] Retardo: {}s".format(np.mean(m_delay)))
    print("[LSL Markers] Varianza (retardo): {}".format(m_delay_var))
    print("[LSL Markers] Jitter: {}s".format(m_jitter))


# Hardware Triggers
#  ---------------------------------------------------------------------------------------
t_delay = [] # Lista de retardos entre pares de valores en alto (Hardware Triggers)

for stream in m_data:
    t_y = stream['time_series']
    t_t = stream['time_stamps']
    HIGH_V = np.where(t_y == 1)

    for index in range(len(HIGH_V[0])-1):
        t_marker = [t_t[HIGH_V[0][index+1]] - t_t[HIGH_V[0][index]]]
        t_delay.append(t_marker)

    # Parámetros temporales de análisis
    t_delay = np.array(t_delay)
    t_jitter = np.mean(t_delay - ob_delay)
    t_delay_var = np.var(t_delay)

    # Resultados
    print("[Hardware Triggers] Retardo: {}s".format(np.mean(t_delay)))
    print("[Hardware Triggers] Varianza (retardo): {}".format(t_delay_var))
    print("[Hardware Triggers] Jitter: {}s".format(t_jitter))

# Resultados gráficos
plt.plot(m_t[0:n], m_y[0:n],t_t[0:n], t_y[0:n])
plt.xlabel('TimeStamp (s)')
plt.ylabel('Received signal level')
plt.show()