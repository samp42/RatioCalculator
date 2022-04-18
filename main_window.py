import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from mpl_canva import MplCanva
from physics import Physics
import data


def update_plot(canva, data_points):
    # data_points[][] with [[dist0, spd0, acc0, cur0], ...]
    df = pd.DataFrame(data_points, columns=['Distance', 'Speed', 'Acceleration'], index=data.kXValues)
    distance = canva.axes.twinx()
    speed = canva.axes.twinx()
    acceleration = canva.axes.twinx()
    df.plot(ax=canva.axes)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(200, 200, 1400, 840)
        self.setWindowTitle("Improved Ratio Calculator")
        self.setWindowIcon(QIcon('assets/T4K_RGB_round[colour]_transparent.png'))

        # motor choice
        motor_choice_label = QLabel()
        motor_choice_label.setText("Motor")

        self.motorComboBox = QComboBox()
        for i in data.motors:
            self.motorComboBox.addItem(i.name)
        self.motorComboBox.setMinimumWidth(150)
        # initialize motor choice
        self.motorChoice = data.motors[0]
        self.motorComboBox.currentTextChanged.connect(self.update_motor)

        # wheel choice
        wheel_choice_label = QLabel()
        wheel_choice_label.setText("Wheel")
        wheel_choice_label.move(120, 15)

        self.wheelComboBox = QComboBox()
        for i in data.wheels:
            self.wheelComboBox.addItem(i.name)
        self.wheelComboBox.move(120, 45)
        self.wheelComboBox.setMinimumWidth(200)
        # Initialize wheel choice
        self.wheelChoice = data.wheels[0]
        self.wheelComboBox.currentTextChanged.connect(self.update_wheel)

        # transmission choice
        transmission_choice_label = QLabel()
        transmission_choice_label.setText("Transmission")

        self.transmissionComboBox = QComboBox()
        for i in data.transmissions:
            self.transmissionComboBox.addItem(i.name)
        self.transmissionComboBox.setMinimumWidth(150)
        # Initialize transmission choice
        self.transmissionChoice = data.transmissions[0]
        self.transmissionComboBox.currentTextChanged.connect(self.update_transmission)

        drivetrain_config_layout = QGridLayout()
        drivetrain_config_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(motor_choice_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(self.motorComboBox, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(wheel_choice_label, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(self.wheelComboBox, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(transmission_choice_label, 0, 2, 1, 1, Qt.AlignmentFlag.AlignLeft)
        drivetrain_config_layout.addWidget(self.transmissionComboBox, 1, 2, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # Transmission info
        reduction_loss_label = QLabel()
        reduction_loss_label.setText("Loss per Gearbox Stage: {:.1f}%".format(data.kGearboxStageLoss * 100))
        reduction_loss_label.setMinimumWidth(250)
        self.transmission_loss_label = QLabel()
        self.transmission_loss_label.setText(
            "Loss in Transmission: {:.1f}%".format((1 - self.transmissionChoice.loss) * 100))
        self.transmission_loss_label.setMinimumWidth(250)

        transmission_info_layout = QVBoxLayout()
        transmission_info_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        transmission_info_layout.addWidget(reduction_loss_label)
        transmission_info_layout.addWidget(self.transmission_loss_label)

        # robot mass
        self.robotMass = 154
        robot_mass_label = QLabel()
        robot_mass_label.setText("Robot Mass (lbs)")

        self.robotMassInput = QLineEdit()
        self.robotMassInput.setPlaceholderText("Robot Mass (lbs)")
        self.robotMassInput.textChanged.connect(self.update_mass)
        self.robotMassInput.setText(str(data.kRobotMass))

        # battery voltage
        self.batteryVoltge = data.kNominalBatteryVoltage
        battery_voltage_label = QLabel()
        battery_voltage_label.setText("Battery Voltage (V)")

        self.batteryVoltageInput = QLineEdit()
        self.batteryVoltageInput.setPlaceholderText("Battery Voltage (V)")
        self.batteryVoltageInput.textChanged.connect(self.update_voltage)
        self.batteryVoltageInput.setText(str(data.kNominalBatteryVoltage))

        # gearbox information
        self.numMotors = 0
        # num gearboxes
        gearbox_number_label = QLabel()
        gearbox_number_label.setText("Number of Gearboxes")
        gearbox_number_label.setMinimumWidth(200)
        # num motors per gearbox
        num_motor_label = QLabel()
        num_motor_label.setText("Number of Motors per Gearbox")
        num_motor_label.setMinimumWidth(240)

        self.gearboxNumber = QLineEdit()
        self.gearboxNumber.setPlaceholderText("# of Gearboxes")
        self.gearboxNumber.textChanged.connect(self.update_num_motors)
        self.motorsPerGearbox = QLineEdit()
        self.motorsPerGearbox.setPlaceholderText("Motors per Gearbox")
        self.motorsPerGearbox.textChanged.connect(self.update_num_motors)
        self.gearboxNumber.setText("2")
        self.gearboxNumber.setMinimumWidth(150)
        self.motorsPerGearbox.setText("2")
        self.motorsPerGearbox.setMinimumWidth(150)

        motor_input_layout = QGridLayout()
        motor_input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(robot_mass_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(self.robotMassInput, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(battery_voltage_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(self.batteryVoltageInput, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(gearbox_number_label, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(self.gearboxNumber, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(num_motor_label, 3, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        motor_input_layout.addWidget(self.motorsPerGearbox, 3, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # Gear ratio
        self.numStages = 1

        ratio_label = QLabel()
        ratio_label.setText("Gear Stages")
        ratio_label.move(10, 210)

        self.driveGear1 = QLineEdit()
        self.drivenGear1 = QLineEdit()
        self.driveGear2 = QLineEdit()
        self.drivenGear2 = QLineEdit()
        self.driveGear3 = QLineEdit()
        self.drivenGear3 = QLineEdit()
        self.driveGear4 = QLineEdit()
        self.drivenGear4 = QLineEdit()
        self.stagesValues = [1, 4, 1, 1, 1, 1, 1, 1]
        self.stages = [
            self.driveGear1, self.drivenGear1, self.driveGear2, self.drivenGear2,
            self.driveGear3, self.drivenGear3, self.driveGear4, self.drivenGear4
        ]
        self.constantRatio = 0.0

        for i in range(len(self.stages)):
            self.stages[i].setText(str(self.stagesValues[i]))

        self.driveGear1.setPlaceholderText("Drive Gear 1")
        self.drivenGear1.setPlaceholderText("Driven Gear 1")
        self.driveGear2.setPlaceholderText("Drive Gear 2")
        self.drivenGear2.setPlaceholderText("Driven Gear 2")
        self.driveGear3.setPlaceholderText("Drive Gear 3")
        self.drivenGear3.setPlaceholderText("Driven Gear 3")
        self.driveGear4.setPlaceholderText("Drive Gear 4")
        self.drivenGear4.setPlaceholderText("Driven Gear 4")
        self.driveGear1.textChanged.connect(lambda stage=0: self.update_stage(0))
        self.drivenGear1.textChanged.connect(lambda stage=1: self.update_stage(1))
        self.driveGear2.textChanged.connect(lambda stage=2: self.update_stage(2))
        self.drivenGear2.textChanged.connect(lambda stage=3: self.update_stage(3))
        self.driveGear3.textChanged.connect(lambda stage=4: self.update_stage(4))
        self.drivenGear3.textChanged.connect(lambda stage=5: self.update_stage(5))
        self.driveGear4.textChanged.connect(lambda stage=6: self.update_stage(6))
        self.drivenGear4.textChanged.connect(lambda stage=7: self.update_stage(7))

        self.constantRatioLabel = QLabel()
        self.constantRatioLabel.setMinimumWidth(200)

        ratio_input_layout = QGridLayout()
        ratio_input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ratio_input_layout.addWidget(ratio_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        gears_input_layout = QFormLayout()
        gears_input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        gears_input_layout.addRow(self.driveGear1, self.drivenGear1)
        gears_input_layout.addRow(self.driveGear2, self.drivenGear2)
        gears_input_layout.addRow(self.driveGear3, self.drivenGear3)
        gears_input_layout.addRow(self.driveGear4, self.drivenGear4)
        ratio_input_layout.addLayout(gears_input_layout, 1, 0, 3, 2, Qt.AlignmentFlag.AlignLeft)

        ratio_input_layout.addWidget(self.constantRatioLabel, 4, 1, 1, 2, Qt.AlignmentFlag.AlignRight)

        # shifter stage
        self.lowGearValues = [34, 40]
        self.highGearValues = [40, 34]

        self.lowGearRatio = 0.0
        self.highGearRatio = 0.0

        shifter_label = QLabel()
        shifter_label.setText("Shifter Stage Gears")

        low_gear_label = QLabel()
        low_gear_label.setText("Low Gear")
        high_gear_label = QLabel()
        high_gear_label.setText("High Gear")

        self.lowDriveGear = QLineEdit()
        self.lowDrivenGear = QLineEdit()
        self.highDriveGear = QLineEdit()
        self.highDrivenGear = QLineEdit()

        self.lowGearStage = [self.lowDriveGear, self.lowDrivenGear]
        self.highGearStage = [self.highDriveGear, self.highDrivenGear]

        self.lowDriveGear.setPlaceholderText("Low Drive Gear")
        self.lowDrivenGear.setPlaceholderText("Low Driven Gear")
        self.highDriveGear.setPlaceholderText("High Drive Gear")
        self.highDrivenGear.setPlaceholderText("High Driven Gear")
        self.lowDriveGear.setText(str(self.lowGearValues[0]))
        self.lowDrivenGear.setText(str(self.lowGearValues[1]))
        self.highDriveGear.setText(str(self.highGearValues[0]))
        self.highDrivenGear.setText(str(self.highGearValues[1]))

        self.lowDriveGear.textChanged.connect(
            lambda gear=data.Gears.LOW, stage=0: self.update_shifter_stage(data.Gears.LOW, 0)
        )
        self.lowDrivenGear.textChanged.connect(
            lambda gear=data.Gears.LOW, stage=1: self.update_shifter_stage(data.Gears.LOW, 1)
        )
        self.highDriveGear.textChanged.connect(
            lambda gear=data.Gears.HIGH, stage=0: self.update_shifter_stage(data.Gears.HIGH, 0)
        )
        self.highDrivenGear.textChanged.connect(
            lambda gear=data.Gears.HIGH, stage=1: self.update_shifter_stage(data.Gears.HIGH, 1)
        )

        self.lowGearRatioLabel = QLabel()
        self.lowGearRatioLabel.setMinimumWidth(200)

        self.highGearRatioLabel = QLabel()
        self.highGearRatioLabel.setMinimumWidth(200)

        shifter_input_layout = QGridLayout()
        shifter_input_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(shifter_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(low_gear_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.lowDriveGear, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.lowDrivenGear, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(high_gear_label, 3, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.highDriveGear, 4, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.highDrivenGear, 4, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.lowGearRatioLabel, 5, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        shifter_input_layout.addWidget(self.highGearRatioLabel, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # simulation
        # kinematics

        # low gear
        max_low_velocity_label = QLabel()
        max_low_velocity_label.setText("Max Low Gear Velocity in {}s (ft/s)".format(data.kTimeRange))

        max_low_acceleration_label = QLabel()
        max_low_acceleration_label.setText("Max Low Gear Acceleration in {}s (ft/s^2)".format(data.kTimeRange))

        max_low_torque_label = QLabel()
        max_low_torque_label.setText("Max Low Gear Motor Torque in {}s (Nm)".format(data.kTimeRange))

        max_low_current_label = QLabel()
        max_low_current_label.setText("Max Low Gear Motor Current in {}s (A)".format(data.kTimeRange))

        max_low_elec_power_label = QLabel()
        max_low_elec_power_label.setText("Max Low Gear Electrical Motor Power in {}s (W)".format(data.kTimeRange))

        max_low_mech_power_label = QLabel()
        max_low_mech_power_label.setText("Max Low Gear Mechanical Motor Power in {}s (W)".format(data.kTimeRange))

        self.maxLowVelocityValueLabel = QLabel()
        self.maxLowAccelerationValueLabel = QLabel()
        self.maxLowTorqueValueLabel = QLabel()
        self.maxLowCurrentValueLabel = QLabel()
        self.maxLowElecPowerValueLabel = QLabel()
        self.maxLowMechPowerValueLabel = QLabel()

        # high gear
        max_high_velocity_label = QLabel()
        max_high_velocity_label.setText("Max High Gear Velocity in {}s (ft/s)".format(data.kTimeRange))

        max_high_acceleration_label = QLabel()
        max_high_acceleration_label.setText("Max High Gear Acceleration in {}s (ft/s^2)".format(data.kTimeRange))

        max_high_torque_label = QLabel()
        max_high_torque_label.setText("Max High Gear Motor Torque in {}s (Nm)".format(data.kTimeRange))

        max_high_current_label = QLabel()
        max_high_current_label.setText("Max High Gear Motor Current in {}s (A)".format(data.kTimeRange))

        max_high_elec_power_label = QLabel()
        max_high_elec_power_label.setText("Max High Gear Electrical Motor Power in {}s (W)".format(data.kTimeRange))

        max_high_mech_power_label = QLabel()
        max_high_mech_power_label.setText("Max High Gear Mechanical Motor Power in {}s (W)".format(data.kTimeRange))

        self.maxHighVelocityValueLabel = QLabel()
        self.maxHighAccelerationValueLabel = QLabel()
        self.maxHighTorqueValueLabel = QLabel()
        self.maxHighCurrentValueLabel = QLabel()
        self.maxHighElecPowerValueLabel = QLabel()
        self.maxHighMechPowerValueLabel = QLabel()

        kinematics_layout = QGridLayout()
        kinematics_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # low gear
        kinematics_layout.addWidget(max_low_velocity_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowVelocityValueLabel, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_low_acceleration_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowAccelerationValueLabel, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_low_torque_label, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowTorqueValueLabel, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_low_current_label, 3, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowCurrentValueLabel, 3, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_low_elec_power_label, 4, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowElecPowerValueLabel, 4, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_low_mech_power_label, 5, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxLowMechPowerValueLabel, 5, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        # high gear
        kinematics_layout.addWidget(max_high_velocity_label, 6, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighVelocityValueLabel, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_high_acceleration_label, 7, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighAccelerationValueLabel, 7, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_high_torque_label, 8, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighTorqueValueLabel, 8, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_high_current_label, 9, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighCurrentValueLabel, 9, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_high_elec_power_label, 10, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighElecPowerValueLabel, 10, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(max_high_mech_power_label, 11, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        kinematics_layout.addWidget(self.maxHighMechPowerValueLabel, 11, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # cycle time
        cycle_distance_label = QLabel()
        cycle_distance_label.setText("Cycle Distance (ft)")

        self.cycleDistanceInput = QLineEdit()
        self.cycleDistanceInput.setPlaceholderText("Cycle Distance (ft)")
        self.cycleDistanceInput.textChanged.connect(self.update_cycle_time)
        self.cycleDistanceInput.setText(str(54))

        low_gear_cycle_time_label = QLabel()
        low_gear_cycle_time_label.setText("Cycle Time in Low Gear (s)")

        self.timeToDistanceLowGear = self.update_cycle_time(data.Gears.LOW)

        self.timeToDistanceLowGearLabel = QLabel()
        self.timeToDistanceLowGearLabel.setText(str(self.timeToDistanceLowGear))

        high_gear_cycle_time_label = QLabel()
        high_gear_cycle_time_label.setText("Cycle Time in High Gear (s)")

        self.timeToDistanceHighGear = self.update_cycle_time(data.Gears.HIGH)

        self.timeToDistanceHighGearLabel = QLabel()
        self.timeToDistanceHighGearLabel.setText(str(self.timeToDistanceHighGear))

        cycle_time_layout = QGridLayout()
        cycle_time_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(cycle_distance_label, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(self.cycleDistanceInput, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(low_gear_cycle_time_label, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(self.timeToDistanceLowGearLabel, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(high_gear_cycle_time_label, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        cycle_time_layout.addWidget(self.timeToDistanceHighGearLabel, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes
        self.lowGearCanva = MplCanva(self, width=20, height=4, dpi=100)
        self.highGearCanva = MplCanva(self, width=20, height=4, dpi=100)

        self.update_ratio()

        input_section_layout = QVBoxLayout()
        input_section_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_section_layout.addLayout(drivetrain_config_layout)
        input_section_layout.addLayout(transmission_info_layout)
        input_section_layout.addLayout(motor_input_layout)
        input_section_layout.addLayout(ratio_input_layout)
        input_section_layout.addLayout(shifter_input_layout)
        input_section_layout.addLayout(kinematics_layout)
        input_section_layout.addLayout(cycle_time_layout)

        right_section_layout = QVBoxLayout()
        right_section_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_section_layout.addWidget(self.lowGearCanva)
        right_section_layout.addWidget(self.highGearCanva)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(input_section_layout)
        main_layout.addLayout(right_section_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.show()

    # Methods
    def update_motor(self):
        self.motorChoice = data.motors[self.motorComboBox.currentIndex()]

    def update_wheel(self):
        self.wheelChoice = data.wheels[self.wheelComboBox.currentIndex()]

    def update_transmission(self):
        self.transmissionChoice = data.transmissions[self.transmissionComboBox.currentIndex()]
        self.transmission_loss_label.setText(
            "Loss in Transmission: {:.1f}%".format((1 - self.transmissionChoice.loss) * 100))

    def update_mass(self):
        try:
            value = int(self.robotMassInput.text())
            if value < 0:
                return
            # update
            self.robotMass = value
        except ValueError:
            pass

    def update_voltage(self):
        try:
            value = int(self.batteryVoltageInput.text())
            if value < 0:
                return
            # update
            self.batteryVoltageInput = value
        except ValueError:
            pass

    def update_num_motors(self):
        try:
            value = int(self.gearboxNumber.text()) * int(self.motorsPerGearbox.text())
            if value < 0:
                return
            # update
            self.numMotors = value
        except ValueError:
            pass

    def set_ratio_label(self):
        self.constantRatioLabel.setText("Constant Ratio: {:.2f} : 1".format(self.constantRatio))

    def update_stage(self, index):
        try:
            value = int(self.stages[index].text())
            if value < 0:
                return
            # update
            self.stagesValues[index] = value
            self.update_ratio()
            self.set_ratio_label()
        except ValueError:
            pass

    def update_shifter_stage(self, gear, stage):
        try:
            try:
                if gear == data.Gears.LOW:
                    value = int((self.lowGearStage[stage]).text())
                elif gear == data.Gears.HIGH:
                    value = int((self.highGearStage[stage]).text())
                else:
                    return
                if value < 0:
                    return
            except AttributeError:
                return
            # update
            if gear == data.Gears.LOW:
                self.lowGearValues[stage] = value
            elif gear == data.Gears.HIGH:
                self.highGearValues[stage] = value
            self.update_ratio()
            self.set_shifter_ratio_label(gear)
        except ValueError:
            pass

    def set_shifter_ratio_label(self, gear):
        if gear == data.Gears.LOW:
            self.lowGearRatioLabel.setText("Low Gear Ratio {:.2f} : 1".format(self.lowGearRatio))
        elif gear == data.Gears.HIGH:
            self.highGearRatioLabel.setText("High Gear Ratio {:.2f} : 1".format(self.highGearRatio))
        else:
            return

    def update_ratio(self):
        """Update ratio values and labels, kinematics, and simulation"""

        drive = 1
        driven = 1
        stages = 0
        for i in range(0, 4):
            drive *= self.stagesValues[2 * i]
            driven *= self.stagesValues[2 * i + 1]
            if self.stagesValues[2 * i + 1] != 1:
                stages += 1
        self.constantRatio = driven / drive
        self.lowGearRatio = self.constantRatio * (self.lowGearValues[1] / self.lowGearValues[0])
        self.highGearRatio = self.constantRatio * (self.highGearValues[1] / self.highGearValues[0])
        self.set_ratio_label()
        self.set_shifter_ratio_label(data.Gears.LOW)
        self.set_shifter_ratio_label(data.Gears.HIGH)

        # number of driven gears not 1
        self.numStages = stages
        if self.lowGearValues[1] != 1 or self.highGearValues[1] != 1:
            self.numStages += 1

        # update simulation
        model_low_gear = Physics(
            self.motorChoice, self.wheelChoice, self.transmissionChoice, self.robotMass, data.kNominalBatteryVoltage,
            self.numStages, data.kGearboxStageLoss, self.numMotors, self.lowGearRatio
        )
        model_high_gear = Physics(
            self.motorChoice, self.wheelChoice, self.transmissionChoice, self.robotMass, data.kNominalBatteryVoltage,
            self.numStages, data.kGearboxStageLoss, self.numMotors, self.highGearRatio
        )

        model_low_gear.iterate()
        model_high_gear.iterate()

        update_plot(self.lowGearCanva, model_low_gear.get_data_frame())
        update_plot(self.highGearCanva, model_high_gear.get_data_frame())

        self.update_kinematics(model_low_gear, model_high_gear)

    def update_kinematics(self, low_gear_model, high_gear_model):
        low_vel, low_acc, low_torque, low_current, low_elec_power, low_mech_power = low_gear_model \
            .get_max_kinematics_values()
        high_vel, high_acc, high_torque, high_current, high_elec_power, high_mech_power = high_gear_model \
            .get_max_kinematics_values()

        self.maxLowVelocityValueLabel.setText("{:.2f}".format(low_vel))
        self.maxLowAccelerationValueLabel.setText("{:.2f}".format(low_acc))
        self.maxLowTorqueValueLabel.setText("{:.2f}".format(low_torque))
        self.maxLowCurrentValueLabel.setText("{:.2f}".format(low_current))
        self.maxLowElecPowerValueLabel.setText("{:.2f}".format(low_elec_power))
        self.maxLowMechPowerValueLabel.setText("{:.2f}".format(low_mech_power))

        self.maxHighVelocityValueLabel.setText("{:.2f}".format(high_vel))
        self.maxHighAccelerationValueLabel.setText("{:.2f}".format(high_acc))
        self.maxHighTorqueValueLabel.setText("{:.2f}".format(high_torque))
        self.maxHighCurrentValueLabel.setText("{:.2f}".format(high_current))
        self.maxHighElecPowerValueLabel.setText("{:.2f}".format(high_elec_power))
        self.maxHighMechPowerValueLabel.setText("{:.2f}".format(high_mech_power))
        
    def update_plot(self, canva, data_points):
        # data_points[][] with [[dist0, spd0, acc0, cur0], ...]
        df = pd.DataFrame(data_points, columns=['Distance'], index=data.kXValues)
        distance = canva.axes.twinx()
        speed = canva.axes.twinx()
        acceleration = canva.axes.twinx()
        df.plot(ax=canva.axes)

    def update_cycle_time(self, gear):
        """Update cycle time for given gear"""
        try:
            if gear == data.Gears.LOW:
                value = int(self.cycleDistanceInput.text())
            elif gear == data.Gears.HIGH:
                value = int(self.cycleDistanceInput.text())
            else:
                return
            if value < 0:
                return
            # update
            # TODO
            return 4.2
        except ValueError:
            pass
