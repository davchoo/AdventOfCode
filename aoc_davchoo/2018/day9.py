from collections import deque
import re
from itertools import cycle


def process_data(data):
    num_players, last_marble = map(int, re.findall(r"(\d+)", data))
    return num_players, last_marble


def calc_winning_score(num_players, last_marble):
    marbles = deque([0])
    players = [0] * num_players

    for turn, current_player in enumerate(cycle(range(len(players))), start=1):
        if (turn % 23) == 0:
            players[current_player] += turn
            marbles.rotate(7)
            players[current_player] += marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(turn)
        if turn == last_marble:
            break
    return max(players)


def solve_a(data):
    num_players, last_marble = process_data(data)
    return calc_winning_score(num_players, last_marble)


def solve_b(data):
    num_players, last_marble = process_data(data)
    return calc_winning_score(num_players, last_marble * 100)
