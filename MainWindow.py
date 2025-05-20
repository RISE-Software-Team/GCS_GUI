from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget
from accelerationplot import AccelerationPlot
from orientation import OrientationWidget
from armingswitches import ArmingSwitches
from altitudeplot import AltitudePlot
from pyrochannels import PyroChannelStatusWidget
from timer import TimerWidget
from datadisplay import LiveDataWidget

dark_mode_stylesheet = """
    * {
        background-color: #2e2e2e;
        color: #ffffff;
        font-family: Arial, sans-serif;
    }
    QPushButton {
        background-color: #444444;
        border: 1px solid #555555;
        color: #ffffff;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #666666;
    }
    QMainWindow {
        background-color: #2e2e2e;
    }
    QLabel {
        color: #ffffff;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(dark_mode_stylesheet)

        self.setWindowTitle("Mission Control")
        self.setGeometry(100, 100, 1000, 600)  # Adjusted window size for layout

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)  # Use QVBoxLayout to stack everything vertically

        # Add the timer widget at the top of the layout (centered)
        self.timer_widget = TimerWidget()  # Create an instance of the TimerWidget
        main_layout.addWidget(self.timer_widget)  # Add the timer at the top of the layout

        # Create and add the left-side widget (for plots)
        left_layout = QVBoxLayout()
        self.acceleration_plot = AccelerationPlot()
        self.altitudeplot = AltitudePlot()
        left_layout.addWidget(self.acceleration_plot)
        left_layout.addWidget(self.altitudeplot)

        # Create and add the right-side widget (for orientation and arm switches)
        right_layout = QVBoxLayout()
        self.orientation_widget = OrientationWidget()
        self.armingswitches = ArmingSwitches()
        self.datadisplay = LiveDataWidget()
        right_layout.addWidget(self.orientation_widget)
        right_layout.addWidget(PyroChannelStatusWidget())
        right_layout.addWidget(self.datadisplay)
        right_layout.addWidget(self.armingswitches)

        # Create a horizontal layout for side-by-side arrangement of plots and widgets
        side_by_side_layout = QHBoxLayout()
        side_by_side_layout.addLayout(left_layout)  # Plots on the left side
        side_by_side_layout.addLayout(right_layout)  # Orientation widget and switches on the right side

        # Add the side-by-side layout to the main layout (below the timer)
        main_layout.addLayout(side_by_side_layout)

        self.setCentralWidget(central_widget)
