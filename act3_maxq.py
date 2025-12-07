import numpy as np
import matplotlib.pyplot as plt


def densidad(h: float) -> float: # kg/m3 (por tramos, 3 capas)
    '''
    Calcula la densidad atmosferica para una altura dada
    Utiliza el modelo de Nasa provisto en:
    https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/earth-atmosphere-equation-english/
    '''
    assert isinstance(h,float) or isinstance(h,np.int64)
    h = h*3.28084 # m to feet
    if h < 36156:
        T = 59 - .00356 * h
        p = 2116 * ((T + 459.7)/(518.6)) ** 5.256
    if h >= 36156 and h < 82345:
        T = -70
        p = 473.1 * np.exp(1.73 - 0.000048 * h)
    if h >= 82345:
        T = -205.05 + 0.00164 * h
        p = 51.97 * ((T + 459.7) /389.98)**(-11.388)

    rho = p / (1718*(T+459.7))
    return rho * 515.379 # imperial to SI

def velocidad(t: float, a: float) -> float: # m/s
    return a * t

def altitud(t: float, a: float) -> float: # m
    return a * t**2 / 2

def q_dinamica(t: float, a: float) -> float: # Pa
    return densidad(altitud(t,a)) * velocidad(t,a)**2 / 2

def fix_variable(f:callable, y: float) -> callable:
    '''
    para una función de dos variables f(x,y), devuelve una función
    identica g(x) con y fija.
    '''
    def g(x):
        return f(x,y)
    return g

def value(f: callable, var: np.array) -> np.array:
    '''
    Valua una función f(x) en los puntos var. Devuelve un np.array con los
    valores calculados.
    '''
    values = list()
    for i in var:
        values.append(f(i))
    return np.array(values)


if __name__== '__main__':
    a = [6.1,9.8,15.7]
    t = np.arange(0, 130, 0.1)
    atm_div = (11019.13, 25098.76)

    fig, axes = plt.subplots(2,2)

    #-------------------Ploteo de presión dinaica-------------------------------
    axes[0][0].set_title('Presión dinamica')
    axes[0][0].set_xlabel('Tiempo [s]')
    axes[0][0].set_ylabel('Presión dinámica [pa]')

    q = list()
    for j in a: #calcula los valores de q para las diferentes aceleraciones
        tmp = value(fix_variable(q_dinamica, j), t)
        q.append(tmp)

    for i in range(len(q)):
        index = q[i].argmax()
        t_max = t[index]
        q_max = q[i][index]
        axes[0][0].plot(t,q[i],label=f'a = {a[i]}')
        axes[0][0].plot(t_max,q_max,'ro')
        axes[0][0].text(t_max + 5,q_max + 8, f'({t_max:.2f},{q_max:.3e})')

    axes[0][0].legend()

    #-------------------Ploteo de altitud-------------------------------
    axes[1][0].set_title('Altitud')
    axes[1][0].set_xlabel('Tiempo [s]')
    axes[1][0].set_ylabel('Altura [m]')

    h = list()
    for j in a:
        tmp = value(fix_variable(altitud, j), t)
        h.append(tmp)

    for i in range(len(q)):
        axes[1][0].plot(t,h[i],label=f'a = {a[i]}')

    for i in atm_div:
        axes[1][0].hlines(i,t[0],t[-1], linestyle='dashed', color='c')
    axes[1][0].legend()

    #-------------------Ploteo de velocidad-------------------------------
    axes[1][1].set_title('Velocidad al cuadrado')
    axes[1][1].set_xlabel('Tiempo [s]')
    axes[1][1].set_ylabel('[(m/s)^2]')

    v = list()
    for j in a:
        tmp = value(fix_variable(velocidad, j), t)
        v.append(tmp)

    for i in range(len(q)):
        axes[1][1].plot(t,v[i]**2,label=f'a = {a[i]}')
    axes[1][1].legend()

    #-------------------Ploteo de densidad-------------------------------
    axes[0][1].set_title('Densidad atmosférica')
    axes[0][1].set_xlabel('Altura [m]')
    axes[0][1].set_ylabel('Densidad [kg/m^3]')

    h = np.arange(0, 47000, 100)

    axes[0][1].plot(h,value(densidad, h))
    for i in atm_div:
        axes[0][1].vlines(i,0,1.25, linestyle='dashed', color='c')

    for i in axes:
        for j in i:
            j.grid()
    plt.show()
