from PyQt5.QtWidgets import QSizePolicy, QPushButton, QHBoxLayout, QWidget

class ArmingSwitches(QWidget):
    def __init__(self):
        super().__init__()

        # Create the first button for the arming switch
        self.arming_button = QPushButton("Arm Rocket", self)
        
        # Set the button's size policy to expand horizontally
        self.arming_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Create the second button (you can set the text or action accordingly)
        self.another_button = QPushButton("Deploy Parachute", self)
        
        # Set the size policy for the second button (optional, depending on the desired effect)
        self.another_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create a horizontal layout to place the buttons side by side
        layout = QHBoxLayout(self)
        
        # Add both buttons to the horizontal layout
        layout.addWidget(self.arming_button)
        layout.addWidget(self.another_button)
        
        # Set the layout to fill the width of the section
        self.setLayout(layout)
