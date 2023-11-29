import serial
import time


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

    def set_teams(self, team_1, team_2):
        self.teams = f"{team_1} - {team_2}"

    def new_key_event(self, event):
        self.event = event

    def send_data(self, data):
        self.arduino.write(data.encode())

    def close_connection(self):
        self.arduino.close()

    def send_score(self, score_1, score_2):
        self.send_data(f"0:{self.teams} "
                       f"1:{score_1} - {score_2}")

    def update_lcd(self, score_1, score_2, strikes, balls, inning):
        self.send_data(f"0:{self.teams} "
                       f"1:S:{score_1}-{score_2} C:{strikes}-{balls} {inning}")


def api_team_get(state):
    return state['away-team'], state['home-team']
