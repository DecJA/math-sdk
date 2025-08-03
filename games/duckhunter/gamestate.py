from game_override import GameStateOverride
from src.calculations.scatter import Scatter
from game_events import reveal_bird_event, bird_win_info_event


class GameState(GameStateOverride):
    """Gamestate for a single spin"""

    def run_spin(self, sim: int):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()

            self.get_display_birds()
            self.assign_default_bird_properties()
            self.assign_winning_prizes()

            self.win_data = self.get_winning_birds()
            reveal_bird_event(self)
            self.evaluate_wincap()
            bird_win_info_event(self)
            self.win_manager.update_spinwin(win_amount=self.win_data["totalWin"])
            self.win_manager.update_gametype_wins(self.gametype)

            if self.check_fs_condition() and self.check_freespin_entry():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.triggered_freegame = True
        self.reset_fs_spin()
        while self.fs < self.tot_fs:
            # Resets global multiplier at each spin
            self.update_freespin()

            self.get_display_birds()
            self.assign_default_bird_properties()
            self.assign_winning_prizes()

            self.win_data = self.get_winning_birds()
            reveal_bird_event(self)
            self.evaluate_wincap()
            bird_win_info_event(self)
            self.win_manager.update_spinwin(win_amount=self.win_data["totalWin"])
            self.win_manager.update_gametype_wins(self.gametype)

            # No retriggers implented

        self.end_freespin()
