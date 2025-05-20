from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt

class PyroChannelStatusWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Outer QGroupBox to wrap the entire widget
        outer_group = QGroupBox("Pyrochannel Status")
        outer_group.setObjectName("outerGroupBox")  # Set an object name for the outer group
        outer_group.setStyleSheet("""
            #outerGroupBox {
                font-size: 20px;
                font-weight: bold;
            }
            QGroupBox::title {
                font-size: 12px;
                font-weight: normal;
            }
        """)  # Larger title only for outer box, smaller for inner group titles
        outer_layout = QVBoxLayout()

        # --- Main Flight Computer Section ---
        main_fc_group = QGroupBox("Main Flight Computer")
        main_fc_layout = QGridLayout()
        self.main_flight_computer = [
            QCheckBox(f"Channel {i+1}: Disabled") for i in range(8)
        ]
        for i, checkbox in enumerate(self.main_flight_computer):
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(self.update_status)
            col = 0 if i < 4 else 1
            row = i if i < 4 else i - 4
            main_fc_layout.addWidget(checkbox, row, col)
        main_fc_group.setLayout(main_fc_layout)

        # --- Redundant Flight Computer Section ---
        redundant_fc_group = QGroupBox("Redundant Flight Computer")
        redundant_fc_layout = QVBoxLayout()
        self.redundant_flight_computer = [
            QCheckBox(f"Channel {i+1}: Disabled") for i in range(4)
        ]
        for checkbox in self.redundant_flight_computer:
            checkbox.setChecked(False)
            checkbox.stateChanged.connect(self.update_status)
            redundant_fc_layout.addWidget(checkbox)
        redundant_fc_group.setLayout(redundant_fc_layout)

        # --- Horizontal layout for side-by-side sections ---
        sections_layout = QHBoxLayout()
        sections_layout.addWidget(main_fc_group)
        sections_layout.addWidget(redundant_fc_group)

        # Add the sections layout to the outer layout
        outer_layout.addLayout(sections_layout)
        outer_group.setLayout(outer_layout)

        # Top-level layout of the widget (just contains the outer group)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(outer_group)
        self.setLayout(main_layout)

    def update_status(self):
        for i, checkbox in enumerate(self.main_flight_computer):
            checkbox.setText(f"Channel {i+1}: {'Enabled' if checkbox.isChecked() else 'Disabled'}")

        for i, checkbox in enumerate(self.redundant_flight_computer):
            checkbox.setText(f"Channel {i+1}: {'Enabled' if checkbox.isChecked() else 'Disabled'}")
