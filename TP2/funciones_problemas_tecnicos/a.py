import copy

class ring():
    '''
    Representa una ronda
    '''
    def __init__(self, items:list):
        self.items = items

    def pop(self, index):
        index = self.calculate_index(index)
        return self.items.pop(index)

    def calculate_index(self, index):
        lenght = len(self.items)
        while index > lenght - 1:
            index -= lenght
        return index

    def __repr__(self):
        return self.items.__repr__()

    def __str__(self):
        return self.items.__str__()

    def __len__(self):
        return self.items.__len__()

    def __getitem__(self,index):
        index = self.calculate_index(index)
        return self.items[index]

def suicidio(R:ring, first:int = 0, jump:int = 1, first_call = True):
    if first_call:
        R = copy.deepcopy(R)

    R.pop(first+jump)
    if len(R) < 2:
        return R[0]
    return suicidio(R, first + jump, jump, False)

def suicidio_gen(R:ring, first:int = 0, jump:int = 1, first_call = True):
    if first_call:
        R = copy.deepcopy(R)

    yield R, R[first], R[first + jump]
    R.pop(first + jump)
    if len(R) < 2:
        return
    yield from suicidio_gen(R, first + jump, jump, False)


if __name__ == '__main__':
    L = ring(list(range(41)))
    show_steps = False
    jumps = [1,3]

    for jump in jumps:
        last_one = suicidio(L, jump = jump)
        if show_steps:
            for ring, killer, killed in suicidio_gen(L, jump=jump):
                print(ring)
                print(f'{killer} kills {killed}')
        print(f'Josefo deberia estar en la posición {last_one} si el salto es de {jump}')



