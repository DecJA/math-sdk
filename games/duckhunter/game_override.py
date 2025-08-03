from game_executables import *
from src.events.events import update_freespin_event, update_global_mult_event
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    This class is is used to override or extend universal state.py functions.
    e.g: A specific game may have custom book properties to reset
    """

    def reset_book(self):
        # Reset global values used across multiple projects
        super().reset_book()
        # Reset parameters relevant to local game only
        self.birds_on_screen = []
        self.winning_birds_on_screen = []
        self.scatter_on_screen = False

    def reset_fs_spin(self):
        super().reset_fs_spin()
        self.birds_on_screen = []
        self.winning_birds_on_screen = []

    def assign_special_sym_function(self):
        pass
        # self.special_symbol_functions = {"B1": [self.assign_mult_property]}

    def check_game_repeat(self):
        """Verify final win matches required betmode conditions."""
        if self.repeat == False:
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
