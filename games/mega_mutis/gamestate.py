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

            if self.win_data["totalWin"] > 0:
                self.winning_spin = True
            elif self.win_data["totalWin"] == 0 and self.criteria != "0":
                raise RuntimeError
            reveal_animal_event(self)

            count = {}
            for idx, _ in enumerate(self.board):
                for idy, _ in enumerate(self.board[idx]):
                    s = self.board[idx][idy]
                    try:
                        count[s.prize] += 1
                    except:
                        count[s.prize] = 1
            if sum(count.values()) != 9 or (max(count.values()) >= 3 and self.win_data["totalWin"] <= 0):
                print("error")
            if self.win_data["totalWin"] > 0:
                win_info_event(self, False)
                self.evaluate_wincap()
            self.win_manager.update_gametype_wins(self.gametype)
            set_win_event(self)
            self.evaluate_finalwin()
            if max(count.values()) >= 3 and (self.final_win <= 0 or self.win_manager.running_bet_win <= 0):
                print("error")

        c = self.get_board_counts()
        match self.criteria:
            case "0":
                if max(list(c.values())) > 2:
                    raise RuntimeError("wins in 0")
                if self.win_manager.running_bet_win > 0:
                    raise RuntimeError
            case "basegame":
                if self.win_manager.running_bet_win == 0:
                    raise RuntimeError
                if max(list(c.values())) < 3:
                    raise RuntimeError
            case "wincap":
                if round(self.win_manager.running_bet_win, 0) != round(self.config.wincap, 0):
                    raise RuntimeError
                if not (self.wincap_triggered):
                    raise RuntimeError

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            self.update_freespin()
            pass

        self.end_freespin()

    def get_board_counts(self):
        counter = {}
        for idx, _ in enumerate(self.board):
            for idy, _ in enumerate(self.board[idx]):
                p = self.board[idx][idy].prize
                try:
                    counter[p] += 1
                except:
                    counter[p] = 1

        return counter
