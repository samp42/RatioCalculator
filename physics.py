import pandas as pd
import data


def m_to_ft(value):
    return 3.2808399 * value


def ft_to_m(value):
    return value / 3.2808399


def lbs_to_kg(value):
    return 0.45359237 * value


def maximum(f1, f2):
    return f1 if f1 >= f2 else f2


class Physics:
    # equation
    # V = A*(ang_acc) + B*(ang_vel)
    def __init__(self, motor, wheel, transmission, mass, voltage, num_stages, stage_loss, num_motor, ratio):
        self.motor = motor
        self.wheel = wheel
        self.transmission = transmission
        self.mass = mass # lbs_to_kg(mass)
        self.batteryVoltage = voltage
        self.numStages = num_stages
        self.stageLoss = stage_loss
        self.numMotor = num_motor
        self.ratio = ratio
        # efficiency
        self.gearboxEfficiency = (1 + self.stageLoss) ** self.numStages
        # kinematics
        self.torque = 0.0
        self.current = 0.0
        self.acceleration = 0.0
        self.velocity = 0.0
        self.distance = 0.0
        self.dataFrame = []
        self.maxVelocity = -1
        self.maxAcceleration = -1
        self.maxCurrent = -1
        self.maxTorque = -1
        self.maxElectricalPower = -1
        self.maxMechanicalPower = -1

    # get acceleration and current for given speed
    # find speed given acceleration
    # find distance traveled given acceleration
    # generate data_frame for current iteration
    # append to data_frame
    # repeat
    def iterate(self):
        for _ in data.kXValues:
            # update kinematics
            self.torque = self.get_motor_torque()
            self.current = self.torque_to_current(self.torque)
            self.acceleration = self.get_acceleration()
            self.velocity += self.acceleration * data.kTimeStep
            self.distance += self.velocity * data.kTimeStep
            # update current
            self.current = self.torque_to_current(self.get_motor_torque() * self.numMotor)
            # add data to data frame
            self.add_to_data_frame(self.distance, self.velocity, self.acceleration)
            # self.add_to_data_frame(self.distance, self.velocity, self.acc, self.current)
            # update max kinematics
            self.maxAcceleration = maximum(ft_to_m(self.acceleration), self.maxAcceleration)
            self.maxVelocity = maximum(ft_to_m(self.velocity), self.maxVelocity)
            self.maxTorque = maximum(self.torque, self.maxTorque)
            self.maxCurrent = maximum(self.current, self.maxCurrent)
            self.maxElectricalPower = maximum(self.current * self.batteryVoltage, self.maxElectricalPower)
            self.maxMechanicalPower = maximum(ft_to_m(ft_to_m(self.velocity * self.acceleration))
                                              * self.mass, self.maxMechanicalPower)

    def get_acceleration(self):
        return m_to_ft(self.get_a_coefficient() * (self.batteryVoltage - self.get_b_coefficient() * self.velocity))

    # motor_torque =
    # (mass * wheel_radius^2 * ang_vel) / (gear_ratio * n_motors) *
    # ( 1 + transmission_loss ) * ( 1 + stage_loss) ^ n_stages
    def get_motor_torque(self):
        # (kt) / (m * r * u)
        return (2 * self.motor.kT) / (self.mass * self.wheel.diameterM * self.get_losses())

    # I = T / kT
    def torque_to_current(self, torque):
        return torque / self.motor.kT

    # A = resistance * motor_torque / kT
    def get_a_coefficient(self):
        # (motor_torque * G * n) / R
        return (self.get_motor_torque() * self.ratio * self.numMotor) / \
               (data.kNominalBatteryVoltage / self.motor.stallCurrent)

    # B = 1 / kV
    def get_b_coefficient(self):
        # 1 / (kv * r)
        return 2 / (self.motor.kV * self.wheel.diameterM)

    def get_losses(self):
        # gearbox losses * transmission losses
        return self.gearboxEfficiency * (1 + self.transmission.loss)

    def add_to_data_frame(self, distance, speed, acceleration):
        self.dataFrame.append([distance, speed, acceleration])

    def get_time_to_distance(self, distance):
        """Get time taken to travel given distance in ft"""
        pass

    def get_data_frame(self):
        """Return the pandas data frame: [[dist0, spd0, acc0, cur0], ...]"""
        df = pd.DataFrame(self.dataFrame)
        # df.to_excel("data.xlsx")
        return self.dataFrame

    def get_max_kinematics_values(self):
        """Return max velocity, acceleration, torque, current, electrical power, and mechanical power"""
        return [self.maxVelocity, self.maxAcceleration, self.maxTorque, self.maxCurrent,
                self.maxElectricalPower, self.maxMechanicalPower]
