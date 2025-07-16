from src.executables.executables import Executables
from src.calculations.statistics import get_random_outcome
from game_events import reveal_animal_event
from collections import defaultdict


class GameCalculations(Executables):

    def draw_animals(self):
        match self.criteria:
            case "wincap":
                self.draw_max_board()
            case "0":
                self.draw_zero_board()
            case "basegame":
                self.draw_base_board()
        reveal_animal_event(self)

    def draw_max_board(self):
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                self.board[reel][row] = self.create_symbol("T1")

    def draw_zero_board(self):
        sym_count = {}
        for tup in self.config.paytable:
            sym_count[tup[1]] = 0

        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                sym = get_random_outcome(self.config.sym_dist)
                while sym_count[sym] >= 2:
                    sym = get_random_outcome(self.config.sym_dist)
                self.board[reel][row] = self.create_symbol(sym)
                sym_count[sym] += 1

    def draw_base_board(self):
        sym_count = {}
        for tup in self.config.paytable:
            sym_count[tup[1]] = 0

        while all([c < 3 for _, c in sym_count.items()]):
            self.board = [[[] for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
            for reel, _ in enumerate(self.board):
                for row, _ in enumerate(self.board[reel]):
                    sym = get_random_outcome(self.config.sym_dist)
                    while sym_count[sym] >= 3:
                        sym = get_random_outcome(self.config.sym_dist)
                    self.board[reel][row] = self.create_symbol(sym)
                    sym_count[sym] += 1

    def get_animal_wins(self):
        return_data = {
            "totalWin": 0,
            "wins": [],
        }
        total_win = 0
        symbols_on_board = defaultdict(list)
        for reel_idx, reel in enumerate(self.board):
            for row_idx, symbol in enumerate(reel):
                symbols_on_board[symbol.name].append({"reel": reel_idx, "row": row_idx})
        for sym in symbols_on_board:
            win_size = len(symbols_on_board[sym])
            if (win_size, sym) in self.config.paytable:
                symbol_win_data = {
                    "symbol": sym,
                    "win": self.config.paytable[(win_size, sym)],
                    "positions": symbols_on_board[sym],
                }
                total_win += symbol_win_data["win"]
                return_data["wins"].append(symbol_win_data)
        return_data["totalWin"] = total_win
        return return_data
