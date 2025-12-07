import math
from astropy import constants as c
from astropy import units as u
import numpy as np

def calcular_velocidades(ha_km: float, phi_deg:float, hb_km:float):
    '''
    args:
    ha_km: altura inicial en km
    phi_deg: ángulo de ingreso con respecto a la dirección radial terrestre
    hb_km: altura de órbita de aterrizaje en km
    '''
    ha = (ha_km * u.km).to(u.m) + c.R_earth
    hb = (hb_km * u.km).to(u.m) + c.R_earth
    phi = phi_deg * u.deg
    vaf = (2 * c.GM_earth * (ha**(-1) - hb**(-1)) * (1 - (ha / (hb * np.sin(phi)))**2)**(-1))**(1/2)
    vbf = ha / (hb * np.sin(phi)) * vaf
    return vaf.value, vbf.value

if __name__ == '__main__':
    print(calcular_velocidades(362.1,60,67.37))

