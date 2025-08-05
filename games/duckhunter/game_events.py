BOARD_MULT_INFO = "boardMultiplierInfo"
from copy import deepcopy
from src.events.events import EventConstants, json_ready_sym


def reveal_bird_event(gamestate):
    """Display the initial board drawn from reelstrips."""
    board_client = []
    special_attributes = list(gamestate.config.special_symbols.keys())
    for row in range(len(gamestate.board)):
        s = json_ready_sym(gamestate.board[row], special_attributes)
        if "prize" in s:
            s["prize"] = int(s["prize"] * 100)
        if gamestate.board[row].is_winning:
            s["winning"] = True
        else:
            s["winning"] = False
        board_client.append(s)

    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.REVEAL.value,
        "board": board_client,
        "gameType": gamestate.gametype,
    }
    gamestate.book.add_event(event)


def bird_win_info_event(gamestate):
    """
    include_padding_index: starts winning-symbol positions at row=1, to account for top/bottom symbol inclusion in board
    """
    win_data_copy = {}
    win_data_copy["wins"] = deepcopy(gamestate.win_data["wins"])
    for idx, w in enumerate(win_data_copy["wins"]):
        new_positions = w["positions"]
        win_data_copy["wins"][idx]["win"] = int(
            round(min(win_data_copy["wins"][idx]["win"], gamestate.config.wincap) * 100, 0)
        )
        win_data_copy["wins"][idx]["positions"] = new_positions

    if gamestate.win_data["totalWin"] > 0:
        event = {
            "index": len(gamestate.book.events),
            "type": EventConstants.WIN_DATA.value,
            "totalWin": int(round(min(gamestate.win_data["totalWin"], gamestate.config.wincap) * 100, 0)),
            "wins": win_data_copy["wins"],
        }
        gamestate.book.add_event(event)


def send_mult_info_event(gamestate, board_mult: int, mult_info: dict, base_win: float, updatedWin: float):
    multiplier_info, winInfo = {}, {}
    multiplier_info["positions"] = []
    if gamestate.config.include_padding:
        for m in range(len(mult_info)):
            multiplier_info["positions"].append(
                {"reel": mult_info[m]["reel"], "row": mult_info[m]["row"] + 1, "multiplier": mult_info[m]["value"]}
            )
    else:
        for m in range(mult_info):
            multiplier_info["positions"].append(
                {"reel": mult_info[m]["reel"], "row": mult_info[m]["row"], "multiplier": mult_info[m]["value"]}
            )

    winInfo["tumbleWin"] = int(round(min(base_win, gamestate.config.wincap) * 100))
    winInfo["boardMult"] = board_mult
    winInfo["totalWin"] = int(round(min(updatedWin, gamestate.config.wincap) * 100))

    assert round(updatedWin, 1) == round(base_win * board_mult, 1)
    event = {
        "index": len(gamestate.book.events),
        "type": BOARD_MULT_INFO,
        "multInfo": multiplier_info,
        "winInfo": winInfo,
    }
    gamestate.book.add_event(event)
