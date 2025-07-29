from src.executables.executables import Executables
from src.calculations.statistics import get_random_outcome
from collections import defaultdict
import random
from copy import deepcopy


class GameCalculations(Executables):

    def draw_animals(self):
        match self.criteria:
            case "wincap":
                self.draw_max_board()
            case "0":
                self.draw_zero_board()
            case "basegame":
                self.draw_base_board()
            case _:
                raise RuntimeError("state not reconized")

        # reveal_animal_event(self)

    def draw_max_board(self):
        sym_count = {}
        for v, _ in self.get_current_distribution_conditions()["prize_dist"].items():
            sym_count[v] = 0
        place_count = 0
        av_pos = self.get_board_pos(3, 3)
        while place_count < 9:
            spot = random.choice(av_pos)
            av_pos.remove(spot)
            if place_count < 3:
                self.board[spot[0]][spot[1]] = self.create_symbol("P")
                self.board[spot[0]][spot[1]].prize = self.config.wincap
                sym_count[self.config.wincap] += 1
            else:
                s = self.create_symbol("P")
                while s.prize >= self.config.wincap or sym_count[s.prize] >= 2:
                    s = self.create_symbol("P")
                self.board[spot[0]][spot[1]] = s
                sym_count[s.prize] += 1
                # print(self.board[spot[0]][spot[1]].prize)

            place_count += 1

    def get_sym_count(self):
        sym_count = {}
        for v, _ in self.get_current_distribution_conditions()["prize_dist"].items():
            sym_count[v] = 0
        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                p = self.board[reel][row].prize
                sym_count[p] += 1

        return sym_count

    def draw_zero_board(self):
        sym_count = {}
        for v, _ in self.get_current_distribution_conditions()["prize_dist"].items():
            sym_count[v] = 0

        for reel, _ in enumerate(self.board):
            for row, _ in enumerate(self.board[reel]):
                s = self.create_symbol("P")
                while sym_count[s.prize] >= 2:
                    s = self.create_symbol("P")
                self.board[reel][row] = s
                sym_count[s.prize] += 1

        dummy_vals = []
        for s, c in sym_count.items():
            if c < 2 and s in (list(self.config.padding_dist.keys())):
                dummy_vals.append(s)

        dummy_vars = get_random_outcome(self.config.num_dummy_placement)
        for _ in range(dummy_vars):
            high_sym = random.choice(dummy_vals)
            aval_cols, aval_rows = [0, 1, 2], [0, 1, 2]
            rand_col, rand_row = random.choice(aval_cols), random.choice(aval_rows)
            aval_cols.remove(rand_col)
            aval_rows.remove(rand_row)
            self.board[rand_col][rand_row] = deepcopy(self.create_symbol("P"))
            self.board[rand_col][rand_row].prize = deepcopy(high_sym)
            sym_count = self.get_sym_count()
            if sym_count[high_sym] >= 2:
                dummy_vals.remove(high_sym)

    def get_board_pos(self, num_reels, num_rows):
        pos = []
        for i in range(num_reels):
            for j in range(num_rows):
                pos.append((i, j))
        return pos

    def draw_base_board(self):
        sym_count = {}
        for v, _ in self.get_current_distribution_conditions()["prize_dist"].items():
            sym_count[v] = 0

        av_pos = self.get_board_pos(3, 3)
        place_count = 0
        det_val = get_random_outcome(self.get_current_distribution_conditions()["prize_dist"])
        while det_val == 0:
            det_val = get_random_outcome(self.get_current_distribution_conditions()["prize_dist"])
        while place_count < 9:
            if place_count < 3:
                spot = random.choice(av_pos)
                av_pos.remove(spot)
                self.board[spot[0]][spot[1]] = deepcopy(self.create_symbol("P"))
                self.board[spot[0]][spot[1]].prize = deepcopy(det_val)
                sym_count[self.board[spot[0]][spot[1]].prize] += 1
            else:
                spot = random.choice(av_pos)
                s = self.create_symbol("P")
                while sym_count[s.prize] >= 2:
                    s = self.create_symbol("P")
                self.board[spot[0]][spot[1]] = deepcopy(s)
                sym_count[self.board[spot[0]][spot[1]].prize] += deepcopy(1)
                av_pos.remove(spot)

            place_count += 1

        dummy_vals = []
        for s, c in sym_count.items():
            if c < 2 and s in (list(self.config.padding_dist.keys())) and s != det_val:
                dummy_vals.append(s)
        av_pos = self.get_board_pos(3, 3)
        rem_vals = []
        for p in av_pos:
            if self.board[p[0]][p[1]].prize == det_val:
                rem_vals.append(p)
        for r in rem_vals:
            av_pos.remove(r)
        dummy_vars = get_random_outcome(self.config.num_dummy_placement)
        for _ in range(dummy_vars):
            high_sym = random.choice(dummy_vals)
            rng_pos = random.choice(av_pos)
            self.board[rng_pos[0]][rng_pos[1]] = self.create_symbol("P")
            self.board[rng_pos[0]][rng_pos[1]].prize = high_sym
            av_pos.remove(rng_pos)
            sym_count = self.get_sym_count()
            if sym_count[high_sym] >= 2:
                dummy_vals.remove(high_sym)

    def get_animal_wins(self):
        return_data = {
            "totalWin": 0,
            "wins": [],
        }
        total_win = 0
        symbols_on_board = defaultdict(list)
        for reel_idx, reel in enumerate(self.board):
            for row_idx, symbol in enumerate(reel):
                symbols_on_board[symbol.prize].append({"reel": reel_idx, "row": row_idx})
        for sym_vals in symbols_on_board:
            win_size = len(symbols_on_board[sym_vals])
            if win_size > 3:
                raise RuntimeError("too many symbols")
            if win_size == 3:
                symbol_win_data = {"symbol": "P", "win": float(sym_vals), "positions": symbols_on_board[sym_vals]}
                total_win += float(sym_vals)
                return_data["wins"].append(symbol_win_data)
        return_data["totalWin"] = total_win
        return return_data
