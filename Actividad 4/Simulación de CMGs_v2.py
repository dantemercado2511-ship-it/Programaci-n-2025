import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CMG:

    """
    Clase que representa un Controlador de Momento Giroscópico (CMG).

    Atributos:
    1. h : float. El momento angular del CMG.
    2. angulo : float. El ángulo de orientación del CMG respecto al eje de rotación.
    """

    # Constructor
    def __init__(self, h, angulo):

        """
        Inicializa un objeto CMG con su momento angular y ángulo de orientación.

        Parámetros:
        1. h : float. Momento angular del CMG.
        2. angulo : float. Ángulo de orientación del CMG.
        """

        self.h = h
        self.angulo = angulo

class Microsatelite:

    """
    Clase que representa un microsatélite con sus propiedades físicas y su control.

    Atributos:
    1. matriz_inercia : array. Matriz de inercia del microsatélite.
    2. velocidad_ang : array. Velocidad angular actual del microsatélite.
    3. orientacion : array. Orientación actual del microsatélite (vector unitario).
    4. cmgs : list. Lista de objetos CMG que controlan la orientación del microsatélite.
    5. orientacion_anterior : array. Orientación anterior utilizada para calcular el error derivativo.
    6. error_integral : array. Error integral utilizado en el control PD.
    """

    # Constructor
    def __init__(self, matriz_inercia, velocidad_ang, orientacion_inicial, cmgs, debug):

        """
        Inicializa un microsatélite con las propiedades físicas y los CMGs asociados.

        Parámetros:
        1. matriz_inercia : array. Matriz de inercia del microsatélite.
        2. velocidad_ang : array. Velocidad angular inicial del microsatélite.
        3. orientacion_inicial : array. Orientación inicial del microsatélite.
        4. cmgs : list. Lista de objetos CMG que controlan la orientación del microsatélite.
        5. debug: bool. Valor booleano que define el modo debug
        """

        self.matriz_inercia = np.array(matriz_inercia)
        self.velocidad_ang = np.array(velocidad_ang)
        self.orientacion = np.array(orientacion_inicial)
        self.cmgs = cmgs
        self.orientacion_anterior = np.array(orientacion_inicial)  # Para el control derivativo
        self.error_integral = np.zeros(3)  # Inicializamos el error integral
        self.debug = debug

    # Calcular una "escala" de las coordenadas de orientación para ajustar las ganancias
    def Calcular_Escala_Orientacion(self, orientacion_inicial, orientacion_final):

        """
        Calcula una "escala" para las ganancias del controlador basada en la diferencia angular.

        Parámetros:
        1. orientacion_inicial : array. Orientación inicial del microsatélite.
        2. orientacion_final : array. Orientación final objetivo.

        Retorna:
        float
            Un factor de escala para ajustar las ganancias del controlador.
        """

        # Medir la diferencia entre las orientaciones (distancia angular)
        diferencia = np.linalg.norm(orientacion_final - orientacion_inicial)
        escala = max(1.0, diferencia * 2.0)
        if self.debug:
            print(f"[DEBUG] Diferencia angular: {diferencia}, Escala: {escala}")

        # Ajuste proporcional para la ganancia según la distancia angular
        return escala  # Ajuste según la diferencia

    # Calcular las componentes por eje del momento angular total
    def Calcular_Momento_Angular_Total(self):

        """
        Calcula el momento angular total del microsatélite considerando los CMGs.

        Retorna:
        1. array. El vector del momento angular total calculado.
        """

        hT_x = -self.cmgs[0].h * np.sin(self.cmgs[0].angulo) + self.cmgs[1].h * np.sin(self.cmgs[1].angulo) + self.cmgs[4].h * np.cos(self.cmgs[4].angulo) - self.cmgs[5].h * np.cos(self.cmgs[5].angulo)
        hT_y = self.cmgs[0].h * np.cos(self.cmgs[0].angulo) - self.cmgs[1].h * np.cos(self.cmgs[1].angulo) - self.cmgs[2].h * np.sin(self.cmgs[2].angulo) + self.cmgs[3].h * np.cos(self.cmgs[3].angulo)
        hT_z = self.cmgs[2].h * np.cos(self.cmgs[2].angulo) + self.cmgs[3].h * np.cos(self.cmgs[3].angulo) - self.cmgs[4].h * np.sin(self.cmgs[4].angulo) + self.cmgs[5].h * np.cos(self.cmgs[5].angulo)

        hT = np.array([hT_x, hT_y, hT_z])

        if self.debug:
            print(f"[DEBUG] Momento angular total: {hT}")

        return hT

    # Calcular cada componente de B
    def Calcular_B(self):

        """
        Calcula la matriz B utilizada en el cálculo del cambio del momento angular.

        Retorna:
        1. array. La matriz B de dimensiones 3x6.
        """

        B = np.zeros((3,6))

        B[0, 0] = -self.cmgs[0].h * np.cos(self.cmgs[0].angulo)
        B[0, 1] = -self.cmgs[1].h * np.cos(self.cmgs[1].angulo)
        B[0, 4] = -self.cmgs[4].h * np.cos(self.cmgs[4].angulo)
        B[0, 5] = -self.cmgs[5].h * np.cos(self.cmgs[5].angulo)

        B[1, 0] = -self.cmgs[0].h * np.cos(self.cmgs[0].angulo)
        B[1, 1] = -self.cmgs[1].h * np.cos(self.cmgs[1].angulo)
        B[1, 2] = -self.cmgs[2].h * np.cos(self.cmgs[2].angulo)
        B[1, 3] = self.cmgs[3].h * np.cos(self.cmgs[3].angulo)

        B[2, 2] = -self.cmgs[2].h * np.cos(self.cmgs[2].angulo)
        B[2, 3] = -self.cmgs[3].h * np.cos(self.cmgs[3].angulo)
        B[2, 4] = -self.cmgs[4].h * np.cos(self.cmgs[4].angulo)
        B[2, 5] = -self.cmgs[5].h * np.cos(self.cmgs[5].angulo)

        return B

    # Calcular la tasa de cambio del momento angular total
    def Calcular_Tasa_Cambio_Momento_Angular(self, d_angulos_gimbal):

        """
        Calcula la tasa de cambio del momento angular total.

        Parámetros:
        1. d_angulos_gimbal : array. Los cambios en los ángulos de los gimbals.

        Retorna:
        1. array. La tasa de cambio del momento angular.
        """

        B = self.Calcular_B()
        d_hT = B @ d_angulos_gimbal
        return d_hT

    # Calcular el torque de control requerido
    def Calcular_Torque_Control(self, d_angulos_gimbal):

        """
        Calcula el torque de control requerido para el control de orientación.

        Parámetros:
        1. d_angulos_gimbal : array. Los cambios en los ángulos de los gimbals.

        Retorna:
        1. array. El torque de control calculado.
        """

        hT = self.Calcular_Momento_Angular_Total()
        prod_Cruz = np.cross(self.velocidad_ang, hT)

        d_hT = self.Calcular_Tasa_Cambio_Momento_Angular(d_angulos_gimbal)
        u = -d_hT - prod_Cruz
        return u

    # Calcular si hay un error de orientación
    def Calcular_Error_Orientacion(self, orientacion_final):

        """
        Calcula el error de orientación entre la orientación actual y la final.

        Parámetros:
        1. orientacion_final : array. La orientación final objetivo.

        Retorna:
        1. array. El error de orientación calculado.
        """

        error_orientacion = orientacion_final - self.orientacion
        return error_orientacion

    # Control Proporcional-Derivativo (PD) con ajuste dinámico de ganancias
    def Control_PD(self, orientacion_final, k_p_base=3.0, k_d_base=0.2, k_i_base=0.1):

        """
        Aplica un control proporcional-derivativo (PD) para ajustar la orientación del microsatélite.

        Parámetros:
        1. orientacion_final : array. La orientación objetivo que el microsatélite debe alcanzar.
        2. k_p_base : float. Ganancia proporcional base.
        3. k_d_base : float. Ganancia derivativa base.
        4. k_i_base : float. Ganancia integral base.
        """

        # Calcular el error de orientación
        error_orientacion = self.Calcular_Error_Orientacion(orientacion_final)

        # Ajustar las ganancias dinámicamente según la escala de la diferencia angular
        escala = self.Calcular_Escala_Orientacion(self.orientacion, orientacion_final)
        k_p = k_p_base * escala
        k_d = k_d_base * escala
        k_i = k_i_base * escala

        # Calcular el error integral
        self.error_integral += error_orientacion * 0.1  # 0.1 es el intervalo de tiempo

        # Calcular el error derivativo
        error_derivada = (error_orientacion - self.orientacion_anterior)

        # Generar el torque de control
        torque_control = k_p * error_orientacion + k_d * error_derivada + k_i * self.error_integral

        if self.debug:
            print(f"[DEBUG] Error orientación: {error_orientacion}, Torque de control: {torque_control}")

        # Actualizar orientación
        self.Actualizar_Orientacion(torque_control, 0.2)
        self.orientacion_anterior = self.orientacion.copy()

    # Asegurar que la orientación es unitaria
    def Normalizar_Orientacion(self):

        """
        Normaliza la orientación para asegurarse de que sea unitaria.
        """

        self.orientacion = self.orientacion / np.linalg.norm(self.orientacion)

    # Actualizo la orientación del microsatélite
    def Actualizar_Orientacion(self, u, d_tiempo):

        """
       Actualiza la orientación del microsatélite en función del torque de control.

       Parámetros:
       1. u : array. El torque de control.
       2. d_tiempo : float. El intervalo de tiempo en el que se actualiza la orientación.
       """

        d_velocidad_ang = np.linalg.inv(self.matriz_inercia) @ (u - np.cross(self.velocidad_ang, self.matriz_inercia @ self.velocidad_ang))
        self.velocidad_ang += d_velocidad_ang * d_tiempo
        self.orientacion += self.velocidad_ang * d_tiempo

# Variables predefinidas
matriz_inercia = [[1.0, 0.0, 0.0],
                  [0.0, 1.5, 0.0],
                  [0.0, 0.0, 2.0]]

velocidad_ang = [0.01, 0.02, 0.03]
orientacion_inicial = [1.0, 0.0, 0.0]

# Momentos angulares y ángulos de gimbal iniciales para los CMGs
hx, hy, hz = 0.1, 0.2, 0.3
ang_x, ang_y, ang_z = 0.1, 0.2, 0.3

# Instanciación de los CMGs para cada eje
cmg_X1, cmg_X2 = CMG(hx, ang_x), CMG(-hx, -ang_x)
cmg_Y1, cmg_Y2 = CMG(hy, ang_y), CMG(-hy, -ang_y)
cmg_Z1, cmg_Z2 = CMG(hz, ang_z), CMG(-hz, -ang_z)

cmgs = [cmg_X1, cmg_X2, cmg_Y1, cmg_Y2, cmg_Z1, cmg_Z2]

debug = True

# Instanciación del microsatélite
microsatelite = Microsatelite(matriz_inercia, velocidad_ang, orientacion_inicial, cmgs, debug)

# Coordenadas finales indicadas por el usuario
orientacion_final = np.array([0.0, 1.0, 1.0])
orientacion_final = orientacion_final / np.linalg.norm(orientacion_final)  # Normalizar

# Umbral de error para detener el bucle (tolerancia)
umbral_error = 0.01  # Un valor pequeño para tolerancia

# Inicialización de la lista para almacenar las orientaciones
orientaciones = []

# Inicialización de la figura para la animación 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Función de animación para actualizar las orientaciones
def Actualizar(frame):

    """
    Actualiza la orientación del microsatélite en cada cuadro de la animación.

    Parámetros:
    1. frame : int. El número del cuadro de la animación.
    """

    global orientaciones
    microsatelite.Control_PD(orientacion_final)
    orientaciones.append(microsatelite.orientacion.copy())

    # Asegurarse de que la orientación es unitaria
    microsatelite.Normalizar_Orientacion()

    # Calcular el nuevo punto y la dirección de la flecha
    ax.cla()  # Limpiar el gráfico

    # Dibujar una flecha más grande
    ax.quiver(0, 0, 0,
              microsatelite.orientacion[0],
              microsatelite.orientacion[1],
              microsatelite.orientacion[2],
              length=0.5,
              color='darkorchid',
              linewidth=2,
              arrow_length_ratio=0.1)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

# Crear la animación
ani = FuncAnimation(fig, Actualizar, frames=100, interval=50)

plt.show()
