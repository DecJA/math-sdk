"""Scatter pays game calculations"""

import random
from src.calculations.statistics import get_random_outcome
from src.executables.executables import Executables


class GameCalculations(Executables):
    """Game specific calculations for Scatter sample game."""

    def get_display_birds(self):
        bird_array = self.config.bird_selection[self.gametype]
        self.scatter_on_screen = False
        num_birds_dispaly = get_random_outcome(self.config.)
        freegame_maxwin_spin = random.choice([0, 1, 2])
        for i in range(self.config.num_display_birds):
            if self.get_current_distribution_conditions()["force_freegame"] and not (self.scatter_on_screen):
                bird_type = self.config.special_symbols["scatter"][0]
                self.scatter_on_screen = True
            elif (
                self.criteria == "wincap"
                and i == len(self.board) - 1
                and self.gametype == "freegame"
                and self.fs == freegame_maxwin_spin
            ):
                bird_type == "RD"
            else:
                bird_type = get_random_outcome(bird_array)
                if self.scatter_on_screen:
                    while bird_type == self.config.special_symbols["scatter"][0]:
                        bird_type = get_random_outcome(bird_array)  # one scatter appears on any given round
            sym = self.create_symbol(bird_type)
            self.board[i] = sym
            self.birds_on_screen.append(sym)

        self.get_special_symbols_on_board()

    def assign_default_bird_properties(self):
        match self.criteria:
            case "0":
                num_wins = 0
            case "basegame" | "freegame" | "wincap":
                num_wins = self.get_num_winning_birds()
            case _:
                raise RuntimeError("criteria not implemented")

        if self.get_current_distribution_conditions()["force_freegame"]:
            num_wins = max(1, num_wins)  # force at least one hit (for the scatter)

        self.winning_birds_on_screen = self.draw_winning_birds(num_wins)

    def get_num_winning_birds(self):
        return get_random_outcome(self.config.num_winning_birds[self.gametype])

    def draw_winning_birds(self, num_wins):
        winning_birds = []
        if self.get_current_distribution_conditions()["force_freegame"]:
            for i, _ in enumerate(self.birds_on_screen):
                if self.birds_on_screen[i].name == self.config.special_symbols["scatter"][0]:
                    winning_birds = [self.birds_on_screen[i]]
                    num_wins -= 1
                    break

        wins = random.sample(self.birds_on_screen, num_wins)
        winning_birds.extend(wins)
        return winning_birds

    def assign_winning_prizes(self):
        # hanlde the scatter first
        for i in range(len(self.winning_birds_on_screen)):
            if self.birds_on_screen[i].name != self.config.special_symbols["scatter"][0]:
                self.birds_on_screen[i].prize = self.draw_prize_value(self.birds_on_screen[i].name)
            else:
                self.birds_on_screen[i].prize = 0
            self.birds_on_screen[i].is_winning = True

        for j in range(len(self.winning_birds_on_screen), len(self.birds_on_screen)):
            self.birds_on_screen[j].prize = 0
            self.birds_on_screen[j].is_winning = False

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
                sym_data = {"symbol": self.board[idx].name, "positions": idx, "win": self.board[idx].prize}
                win_data["wins"].append(sym_data)
        return win_data

    def get_special_symbols_on_board(self) -> None:
        """Scans board for any active special symbols."""
        self.refresh_special_syms()
        for row, _ in enumerate(self.board):
            if self.board[row].special:
                for specialType in list(self.special_syms_on_board.keys()):
                    if self.board[row].check_attribute(specialType):
                        self.special_syms_on_board[specialType].append({"row": row})
