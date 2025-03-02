import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import load, lgpio

class LoadSensorStatusDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Load Sensor")
        self.setGeometry(100, 100, 350, 200)

        # Create a layout
        self.layout = QVBoxLayout()

        # Label to show sensor load status
        self.status_label = QLabel("Load Status: Unknown")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Label to show current weight
        self.weight_label = QLabel("Current Weight: 0 kg")
        self.weight_label.setAlignment(Qt.AlignCenter)

        # Button to simulate changing the load value
        self.change_weight_button = QPushButton("Simulate Load Change")
        self.change_weight_button.clicked.connect(self.simulate_load_change)

        # Add widgets to the layout
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.weight_label)
        self.layout.addWidget(self.change_weight_button)

        # Set layout for the main window
        self.setLayout(self.layout)

        # Initialize sensor status (mock data)
        self.current_weight = 0  # in kilograms
        self.recommended_weight = 50  # kg
        self.overload_limit = 100  # kg

        # Timer to simulate periodic load changes (optional)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.simulate_load_change)
        # self.timer.start(2000)  # Change load every 2 seconds
        
        # load pins
        self.device = lgpio.gpiochip_open(0)
        # device, in, out
        self.ld = load.init_load(self.device, 1, 1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status_label())
        self.timer.start(500)  # Change load every 2 seconds

    def update_status_label(self):
        """Update the load sensor status based on the current weight."""
        # Update the weight display
        self.current_weight = float(load.getLoadinGrams(self.ld)/1000) 
        self.weight_label.setText(f"Current Weight: {self.current_weight} kg")

        # Check if the weight is under, at, or over the recommended limit
        if self.current_weight < self.recommended_weight:
            self.status_label.setText("Load Status: Under Load")
            self.status_label.setStyleSheet("color: orange;")
        elif self.current_weight == self.recommended_weight:
            self.status_label.setText("Load Status: Recommended Weight Reached")
            self.status_label.setStyleSheet("color: green;")
        elif self.current_weight > self.overload_limit:
            self.status_label.setText("Load Status: Overloaded")
            self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setText("Load Status: Within Recommended Range")
            self.status_label.setStyleSheet("color: blue;")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 300, 150)

        # Create a layout for the main window
        layout = QVBoxLayout()

        # Button to open the load sensor status window
        self.weight_status_button = QPushButton("Weight Status")
        self.weight_status_button.clicked.connect(self.open_load_sensor_window)

        # Add the button to the layout
        layout.addWidget(self.weight_status_button)

        # Set the layout for the window
        self.setLayout(layout)

    def open_load_sensor_window(self):
        """Open the load sensor status display window."""
        self.load_sensor_window = LoadSensorStatusDisplay()
        self.load_sensor_window.show()
        self.close()  # Close the main window after opening the load sensor window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
