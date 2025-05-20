import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

class AltitudePlot(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout of the widget
        main_layout = QVBoxLayout(self)

        # Create a group box to hold the plot
        group_box = QGroupBox("Altitude Plot")
        group_box.setStyleSheet("QGroupBox { font-size: 18px; font-weight: bold; }")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget(self)
        group_layout.addWidget(self.plot_widget)

        # Set plot labels (title already set by group box)
        self.plot_widget.setLabel('left', 'Altitude', units='m')
        self.plot_widget.setLabel('bottom', 'Time', units='s')

        # Add group box to the main layout
        main_layout.addWidget(group_box)

        # Simulated data variables
        self.time_data = []  # Time in seconds
        self.altitude_data = []  # Altitude values

        # Create a QTimer to update the plot every 0.1 second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulated_data)
        self.timer.start(100)  # Update every 0.1 second (100 milliseconds)

    def update_simulated_data(self):
        # Time update
        new_time = len(self.time_data) * 0.1  # Each step is 0.1s

        # Altitude profile:
        # Rise: 0–900 over 30 seconds
        # Hold: 900 for 20 seconds
        # Fall: 900–0 over 30 seconds
        total_time = new_time

        if total_time <= 10:
            new_altitude = (total_time / 10) * 900  # Ascend linearly to 900
        elif 10 < total_time <= 15:
            new_altitude = 900  # Cruise at 900
        elif 15 < total_time <= 20:
            new_altitude = 900 - ((total_time - 20) / 15) * 900  # Descend linearly
        else:
            new_altitude = 0  # After descent, stay at 0

        # Append new data
        self.time_data.append(new_time)
        self.altitude_data.append(new_altitude)

        # Update plot
        self.update_plot()


    def update_plot(self):
        # Plot the simulated data
        self.plot_widget.plot(self.time_data, self.altitude_data, clear=True)