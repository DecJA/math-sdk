from game_override import GameStateOverride
from src.calculations.lines import Lines
from src.events.events import reveal_event


class GameState(GameStateOverride):
    """Handles game logic and events for a single simulation number/game-round."""

    def run_spin(self, sim):
        self.reset_seed(sim)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            if self.criteria == "wincap":
                self.draw_wincap_values()
            elif self.criteria == "0":
                self.draw_zero_board()
            else:
                self.draw_base_values()

            # Handle wincap - force freegame

            # Evaluate wins, update wallet, transmit events
            self.prize_object.win_actions(self)

            if self.check_fs_condition():
                self.run_freespin_from_base()

            self.evaluate_finalwin()
            self.check_repeat()

        self.imprint_wins()

    def run_freespin(self):
        self.reset_fs_spin()
        while self.fs < self.tot_fs:

            # Handle wincap
            if self.criteria != "wincap":
                self.draw_freegame_values()
            else:
                self.draw_wincap_values()

            self.prize_object.win_actions(self)
            self.update_freespin()

        self.end_freespin()
