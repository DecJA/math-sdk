from src.executables.executables import Executables


class GameCalculations(Executables):
    "Game specific calculations"

    def evaluate_board_win(self):
        "return win value"
        num = ""
        for i, _ in enumerate(self.board):
            if self.gametype == "basegame" and i == len(self.board) - 1:
                num += "."
            if self.board[i].name != "B":
                num += str(self.board[i].name)

        return float(num)
