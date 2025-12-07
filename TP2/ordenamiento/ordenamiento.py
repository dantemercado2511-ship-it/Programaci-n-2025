import copy
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def swap(L:list ,i:int ,j:int):
    tmp = L[i]
    L[i] = L[j]
    L[j] = tmp

def bubble_sort(L:list) -> list:
    S = copy.copy(L)
    for i in range(len(S)-1):
        for j in range(len(S)-1):
            if S[j] > S[j+1]:
                swap(S,j,j+1)
    return S

def bubble_sort_gen(L:list):
    S = copy.copy(L)
    for i in range(len(S)-1):
        for j in range(len(S)-1):
            if S[j] > S[j+1]:
                swap(S,j,j+1)
                yield S

def insertion_sort(L:list) -> list:
    S = copy.copy(L)
    for i in range(1, len(S)):
        j = i-1
        val = S[i]
        while j > -1  and val < S[j]:
            S[j+1] = S[j]
            j -= 1
        S[j + 1] = val
    return S

def insertion_sort_gen(L:list):
    S = copy.copy(L)
    for i in range(1, len(S)):
        j = i-1
        val = S[i]
        while j > -1  and val < S[j]:
            S[j+1] = S[j]
            j -= 1
        S[j + 1] = val
        yield S

def selection_sort(L:list) -> list:
    S = copy.copy(L)
    for i in range(len(L)):
        minimo = S[i]
        minindex = i
        for j in range(i+1, len(L)):
            if S[j] < minimo:
                minimo = S[j]
                minindex = j
        swap(S,i,minindex)
    return S

def selection_sort_gen(L:list):
    S = copy.copy(L)
    for i in range(len(L)):
        minimo = S[i]
        minindex = i
        for j in range(i+1, len(L)):
            if S[j] < minimo:
                minimo = S[j]
                minindex = j
        swap(S,i,minindex)
        yield S

def merge(L1:list, L2:list) -> list:
    C1 = copy.copy(L1)
    C2 = copy.copy(L2)
    M = list()
    while len(C1) > 0 and len(C2) > 0:
        if C1[0] < C2[0]:
            M.append(C1[0])
            C1.pop(0)
        else:
            M.append(C2[0])
            C2.pop(0)
    if len(C1) > 0:
        M += C1
    else:
        M += C2
    return M


def merge_sort(L:list) -> list:
    lenght = len(L)
    if lenght <= 1:
        return L
    S = copy.copy(L)
    left = merge_sort(S[:int(lenght/2)])
    right = merge_sort(S[int(lenght/2):])
    S = merge(left,right)
    return S

def merge_gen(L: list, I1: tuple, I2: tuple):
    """
    Une dos intervalos ordenados de una Lista L.
    I1 e I2 son tuplas (start, end) inclusivas.
    """
    M = []
    len1 = I1[1] - I1[0] + 1
    len2 = I2[1] - I2[0] + 1

    i, j = 0, 0
    while i < len1 and j < len2:
        if L[I1[0] + i] <= L[I2[0] + j]:   # <= para estabilidad
            M.append(L[I1[0] + i])
            i += 1
        else:
            M.append(L[I2[0] + j])
            j += 1

    if i < len1:
        M.extend(L[I1[0] + i : I1[1] + 1])
    else:
        M.extend(L[I2[0] + j : I2[1] + 1])

    j = 0
    for i in range(I1[0], I2[1] + 1):
        L.pop(L.index(M[j],I1[0], I2[1]+1))
        L.insert(i,M[j])
        j += 1
        yield L.copy()


def merge_sort_gen(L: list, left=0, right=None):
    if left == 0 and right is None:
        S = copy.copy(L)
    else:
        S = L

    if right is None:
        right = len(S) - 1

    if left >= right:
        return

    mid = (left + right) // 2

    yield from merge_sort_gen(S, left, mid)
    yield from merge_sort_gen(S, mid + 1, right)

    yield from merge_gen(S, (left, mid), (mid + 1, right))


def quick_sort(L:list) -> list:
    if len(L) < 2:
        return L
    S = copy.copy(L)
    pivot = L[-1]
    div = 0
    for i in range(len(S)):
        if S[i] <= pivot:
            if i > div:
                swap(S,i,div)
            div += 1
    return quick_sort(S[:div-1]) + quick_sort(S[div-1:])


def quick_sort_gen(L:list, left=0, right=None):
    if left == 0 and right is None:
        S = copy.copy(L)
    else:
        S = L

    if right is None:
        right = len(S) - 1

    if left >= right:
        return

    pivot = S[right]
    div = left

    for i in range(left, right):
        if S[i] <= pivot:
            if i > div:
                swap(S,i,div)
                yield S
            div += 1

    if div != right:
       swap(S,div,right)
       yield S

    yield from quick_sort_gen(S,left, div-1)
    yield from quick_sort_gen(S,div+1, right)


def is_sorted(L:list) -> bool:
    for i in range(len(L) - 1):
        if L[i] > L[i+1]:
            return False
    return True



if __name__ == '__main__':
    L1 = [1,7,3,2,4,8]
    L2 = [22,36,6,79,26,45,75,13]
    L3 = random.sample(range(0, 100), 50)

    lista_plotear = L2

    print('bubble sort')
    for i in bubble_sort_gen(L1):
        print(i)

    print('selection sort')
    for i in selection_sort_gen(L1):
        print(i)

    print('insertion sort')
    for i in insertion_sort_gen(L1):
        print(i)

    print('merge sort')
    for i in merge_sort_gen(L2):
        print(i)

    print('quick sort')
    for i in quick_sort_gen(L2):
        print(i)

    #fig, ax = plt.subplots()
    #bars = ax.bar(range(len(lista_plotear)), lista_plotear)

    #def init():
    #    for bar, h in zip(bars.patches, lista_plotear):
    #        bar.set_height(h)
    #    return bars.patches

    #def update(frame):
    #    for height, bar in zip(frame, bars.patches):
    #        bar.set_height(height)
    #    return bars.patches

    #ani = animation.FuncAnimation(
    #    fig,
    #    update,
    #    frames=merge_sort_gen(lista_plotear),
    #    init_func=init,
    #    interval=1,
    #    blit=True,
    #    cache_frame_data=False,
    #    repeat=False
    #)

    #ani.save("mp4/L2/merge.mp4", writer="ffmpeg", fps=3)

