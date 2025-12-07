import astropy.units as u
from astropy.constants import GM_earth
from astropy.constants import R_earth

class Vehiculo_e:
    count = 1
    def __init__(self, masa_kg: float, h_km: float, nombre: str | None = None):
        if nombre is None:
            self.nombre = str(Vehiculo_e.count).zfill(4)
        else:
            self.nombre = nombre

        self.m = masa_kg * u.kg
        self.h = h_km * u.km
        self.v = (GM_earth / self.h.to(u.m))**(1/2)
        self.e = 1
        self.a = R_earth + self.h
        self.b = R_earth + self.h

        Vehiculo_e.count += 1

    def cambiar_orbita(self, nueva_h_km: float) -> float:
        """
        Calcula los delta-V de una transferencia de Hohmann hacia una nueva órbita circular.

        Parámetros:
            nueva_h_km : float
                Radio de la órbita de destino (km)
        Retorna:
            dv1 : Delta-V del primer impulso (m/s)
            dv2 : Delta-V del segundo impulso (m/s)
            dv_total : Suma de ambos delta-V (m/s)
        """

        h_destino = (nueva_h_km * u.km).si
        v_destino = (GM_earth / h_destino)**(1/2)

        #Orbita transferencia
        a_t = (self.h + h_destino) / 2
        v_peri = (GM_earth * (2/self.h - 1/a_t))**(1/2)
        v_apo  = (GM_earth * (2/h_destino - 1/a_t))**(1/2)

        # Delta-V
        dv1 = v_peri - self.v
        dv2 = v_destino - v_apo
        dv_total = abs(dv1) + abs(dv2)

        self.dv = dv_total
        self.f = v_destino / self.v

        self.h = h_destino
        self.v = v_destino

        return dv_total

    def __str__(self):
        return f'VE: {self.m}, {self.h}, {self.e}, {self.a.to(u.km)}'

    def __repr__(self):
        return f"{self.nombre} (masa={self.m})"

    def __eq__(self, other):
        if not isinstance(other,Vehiculo_e):
            return NotImplemented
        return True if self.h == other.h else False

    def __lt__(self, other):
        if not isinstance(other,Vehiculo_e):
            return NotImplemented
        return self.m < other.m

    def __le__(self, other):
        if not isinstance(other,Vehiculo_e):
            return NotImplemented
        return self.m <= other.m

    def __gt__(self, other):
        if not isinstance(other,Vehiculo_e):
            return NotImplemented
        return self.m > other.m

    def __ge__(self, other):
        if not isinstance(other,Vehiculo_e):
            return NotImplemented
        return self.m >= other.m


if __name__ == '__main__':
    v = Vehiculo_e(120, 100)
    v1 = Vehiculo_e(150, 100)

    l = [v1,v]
    v > 10

    v1.cambiar_orbita(150000)

    print(l)
    print(sorted(l))
