"""Scatter pays game calculations"""

import random
from src.calculations.statistics import get_random_outcome
from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Scatter sample game."""

    def __init__(self):
        self.birds_on_screen = []
        self.winning_birds_on_screen = []

    def get_display_birds(self):
        bird_array = self.config.brid_selection[self.gametype]
        for i in range(self.config.num_display_birds):
            bird_type = get_random_outcome(bird_array)
            sym = self.create_symbol(bird_type)
            self.board[i] = sym
            self.birds_on_screen.append(sym)

    def assign_default_bird_properties(self):
        num_wins = self.get_num_winning_birds()
        self.winning_birds_on_screen = self.draw_winning_birds(num_wins)

    def get_num_winning_birds(self):
        return get_random_outcome(self.config.num_winning_birds[self.gametype])

    def draw_winning_birds(self, num_wins):
        return random.sample(self.birds_on_screen, num_wins)

    def assign_winning_prizes(self):
        for i in range(len(self.winning_birds_on_screen)):
            self.birds_on_screen[i].prize = self.draw_prize_value(self.birds_on_screen[i].name)
            self.birds_on_screen[i].win_bool = True

        for j in range(i, len(self.birds_on_screen)):
            self.birds_on_screen[j].prize = 0
            self.birds_on_screen[j].win_bool = False

    def draw_prize_value(self, sym_name, std_val=1):
        mean_val = (self.config.paytable[sym_name][0] + self.config.paytable[sym_name][1]) / 2
        val = round(
            max(
                min(random.gauss(mean_val, std_val), self.config.paytable[sym_name][0]),
                self.config.paytable[sym_name][1],
            ),
            1,
        )

        return val

    # bird wins
    def get_winning_birds(self):
        win_data = {"totalWin": 0, "wins": []}
        for idx, _ in enumerate(self.board):
            if self.board[idx].prize > 0:
                win_data["totalWin"] += self.board[idx].prize
                win_data["wins"].append(idx)
        return win_data
