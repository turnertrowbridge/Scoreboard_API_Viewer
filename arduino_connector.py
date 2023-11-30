import serial


# Establish serial communication with the Arduino
class Uno:
    def __init__(self, port_name, baude_rate):
        self.port_name = port_name
        self.baude_rate = baude_rate
        self.arduino = self.setup()
        self.teams = ""
        self.event = ""

    def setup(self):
        arduino = serial.Serial(self.port_name, self.baude_rate)
        return arduino

    def send_data(self, data):
        self.arduino.write((data + '\n').encode())

    def close_connection(self):
        self.arduino.close()