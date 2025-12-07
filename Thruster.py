from Tank import Tank

class Thruster:
    def __init__(self, name, max_thrust, Isp, tank):
        assert isinstance(max_thrust, (float,int))
        assert isinstance(Isp, (float,int))
        assert isinstance(tank, Tank)

        self.name = name
        self.escape_vel = 9.80665 * Isp
        self.max_mass_flow = max_thrust / self.escape_vel
        self.mass_flow = self.max_mass_flow
        self.thrust = self.escape_vel * self.mass_flow
        self.tank = tank

    def set_throttle(self, throttle):
        assert throttle > 0 and throttle < 1

        self.mass_flow = self.max_mass_flow * throttle
        self.thrust = self.escape_vel * self.mass_flow

    def get_thrust(self):
        return self.thrust

    def fire(self,time):
        boost = self.thrust * time
        self.tank.extract(self.mass_flow, time)
        return boost

    def shutdown(self):
        self.throttle = 0

