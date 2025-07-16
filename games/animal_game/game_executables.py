from game_calculations import GameCalculations
from src.calculations.scatter import Scatter


class GameExecutables(GameCalculations):

    def get_scatterpays_update_wins(self):
        """Return the board since we are assigning the 'explode' attribute."""
        self.win_data = Scatter.get_scatterpay_wins(
            self.config, self.board, global_multiplier=self.global_multiplier
        )  # Evaluate wins, self.board is modified in-place
        Scatter.record_scatter_wins(self)
        self.win_manager.update_spinwin(self.win_data["totalWin"])  # Update wallet
