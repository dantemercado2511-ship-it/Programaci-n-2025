# -*- coding: utf-8 -*-
"""
ADT Thruster + Tank + Sensor
UNSAM - Actividad 2
"""

G0 = 9.80665  # gravedad estándar

class Tank:
    """Representa un tanque presurizado de gas frio.
    Mantiene masa y presión iniciales y actuales.
    """

    def __init__(self, nombre, masa_inicial, presion_inicial):
        assert masa_inicial > 0, "La masa inicial debe ser positiva"
        assert presion_inicial > 0, "La presión inicial debe ser positiva"

        self.nombre = nombre
        self.masa_inicial = float(masa_inicial)
        self.masa_actual = float(masa_inicial)
        self.presion_inicial = float(presion_inicial)
        self.presion_actual = float(presion_inicial)

    def extract(self, mdot, dt):
        """Extrae masa del tanque según mdot*dt.
        Devuelve masa realmente consumida.
        Actualiza masa y presión.
        """

        if mdot < 0 or dt <= 0:
            raise ValueError("mdot >= 0 y dt > 0 son requeridos")

        masa_requerida = mdot * dt

        # Si alcanza la masa:
        if masa_requerida <= self.masa_actual:
            masa_consumida = masa_requerida
            self.masa_actual -= masa_consumida
        else:
            # Solo consume lo que queda
            masa_consumida = self.masa_actual
            self.masa_actual = 0.0

        # Actualizar presión proporcionalmente (gas ideal)
        if self.masa_inicial > 0:
            self.presion_actual = self.presion_inicial * (self.masa_actual / self.masa_inicial)
        else:
            self.presion_actual = 0.0

        return masa_consumida

    def pressure_bar(self):
        """Devuelve la presión actual del tanque."""
        return self.presion_actual

    def get_mass(self):
        """Retorna masa actual."""
        return self.masa_actual


class Thruster:
    """Micropropulsor de gas frío.
    Consume masa del tanque según throttle y genera empuje.
    """

    def __init__(self, nombre, empuje_max, isp, tanque):
        assert empuje_max > 0, "Empuje máximo debe ser positivo"
        assert isp > 0, "ISP debe ser positivo"

        self.nombre = nombre
        self.F_max = float(empuje_max)
        self.Isp = float(isp)
        self.tanque = tanque
        self.throttle = 0.0   # entre 0 y 1
        self.on = False

    def set_throttle(self, valor):
        """Define la apertura entre 0 y 1."""
        if not (0 <= valor <= 1):
            raise ValueError("Throttle debe estar entre 0 y 1")
        self.throttle = float(valor)
        self.on = (self.throttle > 0)

    def get_thrust(self):
        """Devuelve empuje actual según throttle."""
        if not self.on or self.throttle == 0:
            return 0.0
        return self.F_max * self.throttle

    def fire(self, dt):
        """Enciende durante dt segundos.
        Devuelve el impulso realizado.
        Puede cortarse si no hay suficiente masa.
        """

        if dt <= 0:
            raise ValueError("El tiempo debe ser positivo")

        if self.throttle == 0:
            return 0.0

        F = self.get_thrust()

        # mdot max en kg/s
        mdot_max = self.F_max / (G0 * self.Isp)
        mdot = mdot_max * self.throttle

        # Intento extraer mdot*dt del tanque
        masa_consumida = self.tanque.extract(mdot, dt)

        # Tiempo efectivo si no hay suficiente masa
        dt_eff = masa_consumida / mdot if mdot > 0 else 0.0

        # Impulso: I = F * dt_eff
        I = F * dt_eff

        return I

    def shutdown(self):
        """Apaga el propulsor."""
        self.throttle = 0.0
        self.on = False


class Sensor:
    """Sensor de presión con offset, gain y chequeo de rango."""

    def __init__(self, nombre, unidad, minimo, maximo):
        assert minimo < maximo, "Rango inválido"
        self.nombre = nombre
        self.unidad = unidad
        self.min = float(minimo)
        self.max = float(maximo)
        self._raw = None
        self.offset = 0.0
        self.gain = 1.0

    def set_raw(self, valor):
        """Guarda la lectura cruda."""
        self._raw = float(valor)

    def calibrate(self, offset=0.0, gain=1.0):
        """Define offset y ganancia."""
        self.offset = float(offset)
        self.gain = float(gain)

    def read(self):
        """Devuelve valor calibrado o None si no hay datos o fuera de rango."""
        if self._raw is None:
            return None

        valor = self.gain * (self._raw + self.offset)

        if not (self.min <= valor <= self.max):
            return None

        return valor
