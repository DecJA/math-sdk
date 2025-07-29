"""Handles the state and output for a single simulation round"""

from game_override import GameStateOverride
from src.calculations.scatter import Scatter
from src.events.events import *
from game_events import reveal_animal_event


class GameState(GameStateOverride):
    """Handle all game-logic and event updates for a given simulation number."""

    def run_spin(self, sim):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            self.draw_animals()
            self.win_data = self.get_animal_wins()
            self.win_manager.update_spinwin(self.win_data["totalWin"])
            totlVal = 0
            for idx, _ in enumerate(self.board):
                for idy, _ in enumerate(self.board[idx]):
                    totlVal += self.board[idx][idy].prize

            if totlVal < 50:
                print("error")
            if self.win_data["totalWin"] > 0:
                self.winning_spin = True
            elif self.win_data["totalWin"] == 0 and self.criteria != "0":
                raise RuntimeError
            reveal_animal_event(self)
            if self.win_data["totalWin"] > 0:
                win_info_event(self, False)
                self.evaluate_wincap()
            self.win_manager.update_gametype_wins(self.gametype)
            set_win_event(self)
            self.evaluate_finalwin()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            self.update_freespin()
            pass

        self.end_freespin()
