from game_calculations import GameCalculations
from game_events import win_info_event
from src.calculations.statistics import get_random_outcome
from src.events.events import reveal_event


class GameExecutables(GameCalculations):

    def draw_base_values(self):
        "Blank on first position"
        self.board = [[]] * self.config.num_reels
        self.board[0] = [self.create_symbol("B")]
        for i in range(1, len(self.board)):
            sym = get_random_outcome(self.config.symbol_values[self.gametype])
            self.board[i] = [self.create_symbol(str(sym))]
        self.reel_positions = []
        reveal_event(self)

    def draw_freegame_values(self):
        "Blank on end position"
        self.board = [] * len(self.config.num_reels)
        for i in range(1, len(self.board) - 1):
            sym = get_random_outcome(self.config.symbol_values)
            self.board[i] = self.create_symbol(sym)
        self.board[len(self.board) - 1] = self.create_symbol("B")

        reveal_event(self)

    def check_fs_condition(self, scatter_key: str = "scatter") -> bool:
        """Check if there are enough active scatters to trigger fs."""
        if self.board[1][0].name == scatter_key:
            return True
        return False


class Prize:
    """Collection of functions to handle line-win games."""

    def evaluate_board_win(self, gamestate):
        "return win value"
        num = ""
        for i, _ in enumerate(gamestate.board):
            if gamestate.gametype == "basegame" and i == len(gamestate.board) - 1:
                num += "."
            if gamestate.board[i][0].name != "B":
                num += str(gamestate.board[i][0].name)

        return float(num)

    def emit_win_events(self, gamestate):
        win_info_event(gamestate)

    def update_wallet_manager(self, gamestate, win_data):
        gamestate.win_manager.update_spinwin(win_data["totalWin"])
        gamestate.win_manager.update_gametype_wins(gamestate.gametype)

    def win_actions(self, gamestate):
        gamestate.win_data = {"totalWin": 0.0}
        gamestate.win_data["totalWin"] = self.evaluate_board_win(gamestate)
        self.emit_win_events(gamestate)
        self.update_wallet_manager(gamestate, gamestate.win_data)
