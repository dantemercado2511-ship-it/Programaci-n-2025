class Tank:
    def __init__(self, name, mass, preassure):
        assert isinstance(mass, (float, int))
        assert isinstance(preassure, (float,int))

        self.name = name
        self.INIT_MASS = mass
        self.INIT_PREASSURE = preassure
        self.mass = mass
        self._preassure = preassure

    def extract(self, mass_flow, time):
        assert isinstance(mass_flow,(float,int))
        assert isinstance(time,(float,int))

        mass = mass_flow * time

        if self.mass > mass:
            self.mass -= mass
            self._preassure = self.INIT_PREASSURE * (self.mass / self.INIT_MASS)
            return mass
        else:
            return None

    def get_mass(self):
        return self.mass

    def get_init_Mass(self):
        return self.INIT_MASS

    def get_preassure(self):
        return self._preassure

    def get_init_preassure(self):
        return self.INIT_PREASSURE
