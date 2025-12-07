# -*- coding: utf-8 -*-
  # act3_maxq.py

  import numpy as np
  import matplotlib.pyplot as plt


  # 1. FUNCIONES MÍNIMAS (OBLIGATORIAS)

  def densidad(h):
      """
      Devuelve densidad del aire (kg/m^3) según la Atmósfera Estándar
      en tres tramos: 0–11 km, 11–25 km, 25–47 km
      """
      h_km = h / 1000.0

      # Troposfera 0–11 km
      if 0 <= h_km <= 11:
          T = 288.15 - 6.5 * h_km          # K
          p = 101325 * (T / 288.15)**5.256 # Pa
          rho = p / (287 * T)
          return rho

      # Estrato isoterma 11–25 km
      elif 11 < h_km <= 25:
          T = 216.65
          p11 = 101325 * (216.65 / 288.15)**5.256
          p = p11 * np.exp(-(h - 11000) / 6341.6)
          rho = p / (287 * T)
          return rho

      # Estratosfera 25–47 km
      elif 25 < h_km <= 47:
          T = 216.65 + (h_km - 25) * 3   # gradiente +3 K/km
          p25 = (101325 * (216.65 / 288.15)**5.256 *
                np.exp(-(25000 - 11000) / 6341.6))
          p = p25 * (T / 216.65)**(-9.473)
          rho = p / (287 * T)
          return rho

      else:
          return 0.0


  def velocidad(t, a):
      """Velocidad v(t) = a t"""
      return a * t


  def altitud(t, a):
      """Altitud h(t) = ½ a t²"""
      return 0.5 * a * t**2


  def q_dinamica(t, a):
      """Presión dinámica q = ½ ρ(h) v²"""
      h = altitud(t, a)
      v = velocidad(t, a)
      rho = densidad(h)
      return 0.5 * rho * v**2



  # 2–3. SIMULACIÓN + GRAFICADO

  def simular_y_graficar():
      aceleraciones = [6.1, 9.8, 15.7]
      dt = 0.1

      plt.figure(figsize=(10,6))

      for a in aceleraciones:
          t = 0
          tiempos = []
          qs = []

          # Simulación hasta caída debajo del 30% del máximo
          q_max = 0
          t_max = 0

          while True:
              q = q_dinamica(t, a)
              tiempos.append(t)
              qs.append(q)

              if q > q_max:
                  q_max = q
                  t_max = t

              # Si ya pasó el pico y baja del 30%, cortar
              if t > 1 and q < 0.30 * q_max:
                  break

              t += dt

          # Graficar curva
          plt.plot(tiempos, qs, label=f"a = {a} m/s²")

          # Anotar Max Q
          plt.text(
              t_max, q_max,
              f"Max Q={q_max:.2f}\n t={t_max:.2f}s",
              fontsize=9
          )

      # Estética
      plt.xlabel("Tiempo (s)")
      plt.ylabel("q(t)  [Pa]")
      plt.title("Presión Dinámica vs Tiempo (Max Q)")
      plt.legend()
      plt.grid(True)
      plt.tight_layout()
      plt.show()

  # 3.5. BLOQUE DE DEMOSTRACIÓN

  if __name__ == "__main__":
      simular_y_graficar()
