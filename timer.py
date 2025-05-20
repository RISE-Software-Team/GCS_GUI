from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt  # Import Qt here

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QLabel to display the timer
        self.timer_label = QLabel('T+00:00:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)  # Center align the label text
        self.timer_label.setStyleSheet("font-size: 30px;")  # Increase font size

        # Initialize the QTimer to update the timer every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # Initialize the start time
        self.start_time = QTime(0, 0)

        # Create the layout and add the label
        layout = QVBoxLayout(self)
        layout.addWidget(self.timer_label)

    def update_timer(self):
        # Increment the time
        self.start_time = self.start_time.addSecs(1)

        # Update the label text with the formatted time
        self.timer_label.setText("T+" + self.start_time.toString("hh:mm:ss"))
