import numpy as np
import matplotlib.pyplot as plt
import statistics as stt
from act3_maxq import *

if __name__== '__main__':
    n = 300 # numero de corridas por aceleración
    e = np.random.normal(0, 0.05, n)
    a_arr = [6.1,9.8,15.7]
    t = np.arange(0, 130, 0.1)

    a_dev_arr = list()
    for i in range(len(a_arr)):
        a_dev_arr.append(a_arr[i] * (1+e))

    maximos = list()
    for a_dev in a_dev_arr:
        q_maxs = list()
        t_maxs = list()
        for a in a_dev:
            q_t = value(fix_variable(q_dinamica, a), t)
            index = q_t.argmax()
            t_maxs.append(t[index])
            q_maxs.append(q_t[index])
        maximos.append([t_maxs, q_maxs])

    mean = list()
    stdev = list()
    for i in maximos:
        tmp = (stt.mean(i[0]), stt.mean(i[1]))
        mean.append(tmp)
        tmp = (stt.stdev(i[0]), stt.stdev(i[1]))
        stdev.append(tmp)


    fig, axes = plt.subplots(1,len(maximos))
    fig.suptitle(f'Histogramas de MaxQ para aceleraciones con desviación. Simulaciones: {n}', fontsize=16)

    for i in range(len(maximos)):
        axes[i].set_xlabel('Presión dinámica [pa]')
        axes[i].set_ylabel('Repeticiones [veces]')
        axes[i].hist(maximos[i][1], label=f'MaxQ = {mean[i][1]:.3} ± {stdev[i][1]:.3f}\nt_MaxQ = {mean[i][0]:.3} ± {stdev[i][0]:.3f}')
        axes[i].legend()
    plt.show()

