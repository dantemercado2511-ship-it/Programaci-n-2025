# -*- coding: utf-8 -*-

from adt_thruster_sensor import Tank, Thruster, Sensor, G0

print("=== DEMO UNSAM ===")

# 1) Defino tanque y sensor
PV1 = Tank("Tanque1", masa_inicial=0.05, presion_inicial=250.0)  # 50 g, 250 bar
p_sens = Sensor("PS1", "bar", 0.0, 300.0)

# calibro sensor
p_sens.calibrate(offset=-35, gain=0.074)

# leo presión antes
p_sens.set_raw(PV1.pressure_bar())
print("Presión antes:", p_sens.read())

assert p_sens.read() is not None

# 2) Defino propulsor
T1 = Thruster("TH1", empuje_max=0.20, isp=60.0, tanque=PV1)

# 3) Orden: throttle=0.5
T1.set_throttle(0.5)
F = T1.get_thrust()
print("Empuje generado:", F)

assert abs(F - 0.10) < 1e-9  # chequeo interno

# 4) Fire durante 1 s
I = T1.fire(1.0)
print("Impulso:", I)

assert I <= 0.10 + 1e-9

# 5) Actualizo presión post-fire
p_sens.set_raw(PV1.pressure_bar())
after = p_sens.read()
print("Presión después:", after)

assert after is not None and after < 250.0

# 6) Apago el propulsor
T1.shutdown()
assert T1.on is False and T1.throttle == 0.0

print("=== FIN DEMO ===")
