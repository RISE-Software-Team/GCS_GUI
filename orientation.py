from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt, QTimer
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class OrientationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        main_layout = QVBoxLayout(self)
        group_box = QGroupBox("Rocket Orientation")
        group_box.setStyleSheet("QGroupBox { font-size: 18px; font-weight: bold; }")
        group_layout = QVBoxLayout(group_box)

        # VTK setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Load model using OBJReader (simpler than OBJImporter and easier to transform)
        reader = vtk.vtkOBJReader()
        reader.SetFileName("rocket_exterior.obj")
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        self.rocket_actor = vtk.vtkActor()
        self.rocket_actor.SetMapper(mapper)

        # Add actor and set up transform
        self.transform = vtk.vtkTransform()
        self.rocket_actor.SetUserTransform(self.transform)
        self.renderer.AddActor(self.rocket_actor)

        self.renderer.SetBackground(0.1, 0.1, 0.2)
        self.renderer.ResetCamera()

        group_layout.addWidget(self.vtk_widget)
        main_layout.addWidget(group_box)

        # Timer to animate
        self.time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_orientation)
        self.timer.start(100)

        self.vtk_widget.GetRenderWindow().Render()
        self.vtk_widget.GetRenderWindow().GetInteractor().Initialize()

    def update_orientation(self):
        t = self.time

        # Orientation logic
        if t < 5:
            pitch = 0
        elif 5 <= t < 10:
            pitch = (t-5) * 18  # Slowly tilts to horizontal (90 degrees)
        elif 10 <= t < 15:
            pitch = 90  # stays horizontal
        elif 15 <= t < 20:
            pitch = 90 - ((t-15) * 18) # Slowly tilts back to vertical (0 degrees)
        else:
            pitch = 0  # stays vertical after jerk

        # Apply pitch rotation around the Z-axis
        self.transform.Identity()
        self.transform.RotateZ(pitch)

        self.rocket_actor.Modified()
        self.vtk_widget.GetRenderWindow().Render()
        self.time += 0.1
