import curses

import requests
from time import sleep

import config

api_url = config.api_key

cur_state = {
    "away-team": "Dodgers",
    "home-team": "Padres",
    "away-score": 0,
    "home-score": 0,
    "inning": 1,
    "inning-half": "bottom",
    "outs": 0,
    "batter": "Bogaerts",
    "pitcher": "Kershaw",
    "pitch_count": 0,
    "count": [0, 0],
    "on_base": [None, None, None, None],
    "last-play": "",
}


def call_get_request():
    try:
        # make a GET request to the API
        response = requests.get(api_url)

        # check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def load_score():
    data = call_get_request()
    cur_state["away-team"] = data["away-team"]
    cur_state["home-team"] = data["home-team"]
    cur_state["away-score"] = data["away-score"]
    cur_state["home-score"] = data["home-score"]
    cur_state["inning"] = data["inning"]
    cur_state["inning-half"] = data["inning-half"]
    cur_state["outs"] = data["outs"]
    cur_state["batter"] = data["batter"]
    cur_state["pitcher"] = data["pitcher"]
    cur_state["pitch_count"] = data["pitch_count"]
    cur_state["count"] = data["count"]
    cur_state["on_base"] = data["on_base"]
    cur_state["last-play"] = data["last-play"]


def show_bases():
    on_base = "◆"
    empty = "◇"
    bases = ["◇", "◇", "◇", "◇"]
    for i in range(len(cur_state["on_base"])):
        if cur_state["on_base"][i]:
            bases[i] = on_base
        else:
            bases[i] = empty

    return bases


def show_inning():
    inning = cur_state["inning"]
    inning_half = cur_state["inning-half"]
    if inning_half == "top":
        inning_half = "▲"
    else:
        inning_half = "▼"
    return f"{inning_half} {inning}"


def display_state(stdscr):
    stdscr.clear()
    stdscr.addstr(
        1, 20,
        f"{cur_state['away-team']} {cur_state['away-score']} - {cur_state['home-team']} {cur_state['home-score']}"
    )
    stdscr.addstr(
        4, 25,
        show_inning()
    )
    stdscr.addstr(
        5, 25,
        f"{cur_state['outs']} outs"
    )
    stdscr.addstr(
        4, 2,
        f"Pitcher: {cur_state['pitcher']}"
    )
    stdscr.addstr(
        5, 2,
        f"{cur_state['pitch_count']} pitches"
    )
    stdscr.addstr(
        6, 2,
        f"Batter: {cur_state['batter']}"
    )

    stdscr.addstr(
        6, 25,
        f"Count: {cur_state['count'][0]} - {cur_state['count'][1]}"
    )

    stdscr.addstr(
        7, 15,
        f"Last play: {cur_state['last-play']}"
    )
    stdscr.addstr(
        4, 50,
        show_bases()[1]
    )
    stdscr.addstr(
        5, 48,
        show_bases()[2]
    )
    stdscr.addstr(
        5, 52,
        show_bases()[0]
    )
    stdscr.addstr(
        6, 50,
        show_bases()[3]
    )

    stdscr.addstr(
        2, 0,
        "--------------------------------------------------------"
    )

    stdscr.refresh()
    sleep(1)  # Sleep for 1 second (you can adjust this as needed)


def main(stdscr):
    curses.curs_set(0)

    while True:
        load_score()
        display_state(stdscr)
        stdscr.clear()


if __name__ == "__main__":
    curses.wrapper(main)
