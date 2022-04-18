import math


class Motor:
    def __init__(self, name, max_rpm, stall_torque, stall_current, max_power):
        self.name = name
        self.maxRpm = max_rpm
        self.stallTorque = stall_torque
        self.stallCurrent = stall_current
        self.maxPower = max_power
        self.kT = stall_torque / stall_current
        self.kV = 12.0 / (max_rpm * math.pi / 30)  # rpm to rad/s
