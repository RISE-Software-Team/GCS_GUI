from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPlainTextEdit
import random
from PyQt5.QtCore import QTimer, QDateTime
from telemetry import TelemetryReceiver
import serial

class LiveDataWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.layout = QVBoxLayout(self)

        # Create a QTimer to update data every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulate_data)
        self.timer.start(1000)  # Update every second
        
        # To connect to the telemetry receiver
        self._ser = serial.Serial("/dev/ttyUSB2", 57600, timeout=0.1) #IDK WHAT THIS SERIAL NEEDS TO BEs
        self._receiver = TelemetryReceiver(self._ser.fileno())

        # Create the outermost groupbox to wrap all sections
        self.main_group = QGroupBox("Live Data", self)
        self.main_group_layout = QVBoxLayout(self.main_group)

        # Create horizontal layout for IMU
        imu_layout = QHBoxLayout()

        # Create sections for IMU, Barometer, 2nd IMU, GNSS, and Radio
        self.create_imu_section()
        self.create_second_imu_section()
        self.create_barometer_section()
        self.create_terminal_section()
        self.create_radio_section()

        # Add IMUs to the horizontal layout
        imu_layout.addWidget(self.imu_group)
        imu_layout.addWidget(self.second_imu_group)

        # Create a horizontal layout for Barometer and GNSS
        barometer_terminal_layout = QHBoxLayout()
        barometer_terminal_layout.addWidget(self.barometer_group)
        barometer_terminal_layout.addWidget(self.terminal_group)

        # Add all sections inside the main group box
        self.main_group_layout.addLayout(imu_layout)
        self.main_group_layout.addLayout(barometer_terminal_layout)
        self.main_group_layout.addWidget(self.radio_group)

        self.main_group.setLayout(self.main_group_layout)
        self.layout.addWidget(self.main_group)

        self.setLayout(self.layout)

        # Set the large font for the Live Data label using stylesheets
        self.main_group.setStyleSheet("""
            QGroupBox {
                font-size: 24px;  /* Make the font large */
                font-weight: bold;  /* Make the text bold */
            }
        """)

    def create_imu_section(self):
        self.imu_group = QGroupBox("IMU", self)
        imu_layout = QVBoxLayout(self.imu_group)

        # IMU section labels
        self.imu_roll_label = QLabel("Roll: Waiting...", self)
        self.imu_pitch_label = QLabel("Pitch: Waiting...", self)
        self.imu_yaw_label = QLabel("Yaw: Waiting...", self)
        self.imu_accel_label = QLabel("Acceleration (XYZ): Waiting...", self)

        # Add labels to IMU layout
        imu_layout.addWidget(self.imu_roll_label)
        imu_layout.addWidget(self.imu_pitch_label)
        imu_layout.addWidget(self.imu_yaw_label)
        imu_layout.addWidget(self.imu_accel_label)

        self.imu_group.setLayout(imu_layout)

    def create_barometer_section(self):
        self.barometer_group = QGroupBox("Barometer", self)
        barometer_layout = QVBoxLayout(self.barometer_group)

        # Barometer section labels
        self.barometer_pressure_label = QLabel("Pressure: Waiting...", self)
        self.barometer_altitude_label = QLabel("Altitude: Waiting...", self)

        # Add labels to Barometer layout
        barometer_layout.addWidget(self.barometer_pressure_label)
        barometer_layout.addWidget(self.barometer_altitude_label)

        self.barometer_group.setLayout(barometer_layout)

    def create_second_imu_section(self):
        self.second_imu_group = QGroupBox("2nd IMU", self)
        second_imu_layout = QVBoxLayout(self.second_imu_group)

        # 2nd IMU section labels
        self.second_imu_roll_label = QLabel("Roll: Waiting...", self)
        self.second_imu_pitch_label = QLabel("Pitch: Waiting...", self)
        self.second_imu_yaw_label = QLabel("Yaw: Waiting...", self)
        self.second_imu_accel_label = QLabel("Acceleration (XYZ): Waiting...", self)

        # Add labels to 2nd IMU layout
        second_imu_layout.addWidget(self.second_imu_roll_label)
        second_imu_layout.addWidget(self.second_imu_pitch_label)
        second_imu_layout.addWidget(self.second_imu_yaw_label)
        second_imu_layout.addWidget(self.second_imu_accel_label)

        self.second_imu_group.setLayout(second_imu_layout)

    def create_terminal_section(self):
        self.terminal_group = QGroupBox("LoRa Terminal", self)
        lora_layout = QVBoxLayout(self.terminal_group)

        self.lora_terminal = QPlainTextEdit(self)
        self.lora_terminal.setReadOnly(True)
        self.lora_terminal.setLineWrapMode(QPlainTextEdit.NoWrap)
        lora_layout.addWidget(self.lora_terminal)

        self.terminal_group.setLayout(lora_layout)

    def create_radio_section(self):
        self.radio_group = QGroupBox("Radio", self)
        radio_layout = QVBoxLayout(self.radio_group)

        # Radio section labels
        self.radio_rssi_label = QLabel("Radio RSSI: Waiting...", self)
        self.radio_time_label = QLabel("Time since last message: Waiting...", self)

        # Add labels to Radio layout
        radio_layout.addWidget(self.radio_rssi_label)
        radio_layout.addWidget(self.radio_time_label)

        self.radio_group.setLayout(radio_layout)
        
    def update_data(self, data):
        try:
            pkt = self._receiver.read()
        except IOError:
            return  # no packet this cycle

        # update IMU labels
        att = pkt.roll, pkt.pitch, pkt.yaw
        self.imu_roll_label.setText(f"Roll: {att[0]:.2f}°")
        self.imu_pitch_label.setText(f"Pitch: {att[1]:.2f}°")
        self.imu_yaw_label.setText(f"Yaw: {att[2]:.2f}°")

        # update acceleration
        ax, ay, az = pkt.accelX, pkt.accelY, pkt.accelZ
        self.imu_accel_label.setText(
            f"Acceleration (XYZ): ({ax:.2f}, {ay:.2f}, {az:.2f}) m/s²"
        )

        # update barometer altitude
        self.barometer_altitude_label.setText(
            f"Altitude: {pkt.altitude:.2f} m"
        )

        # append stage to terminal
        from PyQt5.QtCore import QDateTime
        ts = QDateTime.fromSecsSinceEpoch(int(pkt.timestamp)).toString("HH:mm:ss")
        self.lora_terminal.appendPlainText(f"[{ts}] Stage: {pkt.stage.name}")
        
        # the radio signal was not part of the original packet, nor was the secondary IMU. 
        # TODO: secondary IMU and radio signal

    def simulate_data(self):        
        # Simulating live data values
        
        if random.random() < 0.3:
            msg_id = random.randint(1000, 9999)
            payload = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ012345", k=8))
            timestamp = QDateTime.currentDateTime().toString("HH:mm:ss")
            self.lora_terminal.appendPlainText(f"[{timestamp}] Msg {msg_id}: {payload}")
            
        imu_roll = random.uniform(-180, 180)
        imu_pitch = random.uniform(-90, 90)
        imu_yaw = random.uniform(-180, 180)
        imu_accel_xyz = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))

        barometer_pressure = random.uniform(900, 1100)
        barometer_altitude = random.uniform(0, 5000)

        second_imu_roll = random.uniform(-180, 180)
        second_imu_pitch = random.uniform(-90, 90)
        second_imu_yaw = random.uniform(-180, 180)
        second_imu_accel_xyz = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))

        # gnss_latitude = random.uniform(-90, 90)
        # gnss_longitude = random.uniform(-180, 180)
        # gnss_altitude = random.uniform(0, 5000)

        radio_rssi = random.randint(-100, -50)
        radio_time_since_last_msg = random.randint(0, 300)

        # Update the labels with the new data
        self.imu_roll_label.setText(f"Roll: {imu_roll:.2f}°")
        self.imu_pitch_label.setText(f"Pitch: {imu_pitch:.2f}°")
        self.imu_yaw_label.setText(f"Yaw: {imu_yaw:.2f}°")
        self.imu_accel_label.setText(f"Acceleration (XYZ): ({imu_accel_xyz[0]:.2f}, {imu_accel_xyz[1]:.2f}, {imu_accel_xyz[2]:.2f}) m/s²")

        self.barometer_pressure_label.setText(f"Pressure: {barometer_pressure:.2f} hPa")
        self.barometer_altitude_label.setText(f"Altitude: {barometer_altitude:.2f} m")

        self.second_imu_roll_label.setText(f"Roll: {second_imu_roll:.2f}°")
        self.second_imu_pitch_label.setText(f"Pitch: {second_imu_pitch:.2f}°")
        self.second_imu_yaw_label.setText(f"Yaw: {second_imu_yaw:.2f}°")
        self.second_imu_accel_label.setText(f"Acceleration (XYZ): ({second_imu_accel_xyz[0]:.2f}, {second_imu_accel_xyz[1]:.2f}, {second_imu_accel_xyz[2]:.2f}) m/s²")

        # self.gnss_latitude_label.setText(f"Latitude: {gnss_latitude:.6f}")
        # self.gnss_longitude_label.setText(f"Longitude: {gnss_longitude:.6f}")
        # self.gnss_altitude_label.setText(f"Altitude: {gnss_altitude:.2f} m")

        self.radio_rssi_label.setText(f"Radio RSSI: {radio_rssi} dBm")
        self.radio_time_label.setText(f"Time since last message: {radio_time_since_last_msg} s")
