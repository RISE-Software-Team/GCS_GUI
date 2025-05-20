from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import numpy as np

class AccelerationPlot(QWidget):
    def __init__(self):
        super().__init__()

        self.time = 0
        self.data = []
        self.timestamps = []

        # Main layout
        main_layout = QVBoxLayout(self)

        # Group box
        group_box = QGroupBox("Acceleration Plot")
        group_box.setStyleSheet("QGroupBox { font-size: 18px; font-weight: bold; }")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)

        # Plot widget
        self.plot_widget = pg.PlotWidget(self)
        group_layout.addWidget(self.plot_widget)
        self.plot_widget.setLabel('left', 'Acceleration', units='m/s²')
        self.plot_widget.setLabel('bottom', 'Time', units='s')

        # Add to layout
        main_layout.addWidget(group_box)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # 100ms = 0.1s

    def simulate_acceleration(self, t):
        """ Simulate acceleration profile based on time """
        if t < 10:
            return 2.0  # accelerating
        elif 10 <= t < 20:
            return 0.0  # constant speed
        elif 20 <= t < 30:
            return -2.0  # decelerating
        else:
            return 0.0  # stop

    def update_plot(self):
        acc = np.random.normal(loc=0.0, scale=1.0)  # Mean 0, standard deviation 1
        self.data.append(acc)
        self.timestamps.append(self.time)

        self.plot_widget.plot(self.timestamps, self.data, clear=True)
        self.time += 0.1

