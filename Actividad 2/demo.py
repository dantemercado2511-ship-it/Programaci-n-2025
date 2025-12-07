from Thruster import Thruster
from Tank import Tank
from Sensor import Sensor

tank = Tank('tank',1000,10)
thruster = Thruster('thruster', 3, 0.5, tank)
sensor = Sensor("sensor",'Bar',100,200)

thruster.set_throttle(0.3)
sensor.calibrate(10, 10)

print("Emp del motor:",thruster.get_thrust())
print("Impulso del motor:",thruster.fire(8))

sensor.set_raw(tank.get_preassure())
print(tank.get_preassure())
print(sensor.read())
