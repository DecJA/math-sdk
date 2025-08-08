import random
from game_override import GameStateOverride
from src.calculations.scatter import Scatter
from game_events import reveal_bird_event, bird_win_info_event
from src.events.events import set_win_event, set_total_event


class GameState(GameStateOverride):
    """Gamestate for a single spin"""

    def run_spin(self, sim: int):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()

            self.get_display_birds(self.config.num_display_birds)
            self.assign_default_bird_properties()
            self.assign_winning_prizes()
            random.shuffle(self.board)

            self.win_data = self.get_winning_birds()
            reveal_bird_event(self)
            self.win_manager.update_spinwin(win_amount=self.win_data["totalWin"])
            self.win_manager.update_gametype_wins(self.gametype)

            if len(self.win_data["wins"]) > 0:
                bird_win_info_event(self)
            if self.win_data["totalWin"] > 0:
                set_win_event(self)
                set_total_event(self)
            self.evaluate_wincap()

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.triggered_freegame = True
        self.board = [[] for _ in range(self.config.num_display_bonus_birds)]
        self.reset_fs_spin()
        self.get_display_birds(self.config.num_display_bonus_birds)
        self.assign_default_bird_properties()
        self.assign_winning_prizes()

        self.win_data = self.get_winning_birds()
        reveal_bird_event(self)
        self.win_manager.update_spinwin(win_amount=self.win_data["totalWin"])
        self.win_manager.update_gametype_wins(self.gametype)

        if len(self.win_data["wins"]) > 0:
            bird_win_info_event(self)
            set_win_event(self)
            set_total_event(self)
        self.evaluate_wincap()

        # self.end_freespin()
