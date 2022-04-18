import enum

from motor import Motor
from wheel import Wheel
from transmission import Transmission

# Motors
Falcon500 = Motor("Falcon500", 6380, 4.69, 257, 783)
NEO = Motor("NEO", 5676, 2.60, 105, 406)
CIM = Motor("CIM", 5330, 2.41, 131, 336.29)
MiniCIM = Motor("Mini CIM", 5840, 1.41, 89, 215.58)
RS775pro = Motor("775pro", 18730, 0.71, 134, 348.15)
BAG = Motor("BAG", 13180, 0.43, 53, 148.37)

motors = [Falcon500, NEO, CIM, MiniCIM, RS775pro, BAG]

# Wheels
Colson4 = Wheel("4in Colson", 4, 1)
Pneumatic6 = Wheel("6in WCP Pneumatic", 6, 1.27)
Pneumatic8 = Wheel("8in Andymark Pneumatic", 8, 1.27)
PerformanceNitrile = Wheel("4in Blue Nitrile Tread", 4, 1.19)

wheels = [Colson4, Pneumatic6, Pneumatic8, PerformanceNitrile]

# Transmission
Chain = Transmission("Chain", .92)
Belt = Transmission("Belt", .98)

transmissions = [Chain, Belt]


# gears
class Gears(enum.Enum):
    LOW = 0
    HIGH = 1


kRobotMass = 154.0  # lbs
kGearboxStageLoss = 0.05  # %
kDefaultNumGearbox = 2
kDefaultMotorsPerGearbox = 2

kNominalBatteryVoltage = 12.0
kAverageBatteryVoltage = 11.0

# simulation
# time step of 0.001 second
# plotting range of 5.0 seconds
kTimeStep = 0.001  # s
kTimeRange = 5.0

kXValues = [0.0]
i = 1
x_value = i * kTimeStep
while x_value <= kTimeRange:
    kXValues.append(x_value)
    i += 1
    x_value = i * kTimeStep
