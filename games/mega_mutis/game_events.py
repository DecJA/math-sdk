from copy import deepcopy
from src.events.events import json_ready_sym, EventConstants


def reveal_animal_event(gamestate):
    """Display the initial board drawn from reelstrips."""
    board_client = []
    special_attributes = list(gamestate.config.special_symbols.keys())
    for reel, _ in enumerate(gamestate.board):
        board_client.append([])
        for row in range(len(gamestate.board[reel])):
            s = json_ready_sym(gamestate.board[reel][row], special_attributes)
            if "prize" in s:
                s["prize"] = int(s["prize"] * 100)
            board_client[reel].append(s)

    if gamestate.config.include_padding:
        for reel, _ in enumerate(board_client):
            board_client[reel] = [json_ready_sym(gamestate.top_symbols[reel], special_attributes)] + board_client[
                reel
            ]
            board_client[reel].append(json_ready_sym(gamestate.bottom_symbols[reel], special_attributes))

    flat_board = []
    for idx, _ in enumerate(board_client):
        flat_board.extend([i for i in board_client[idx]])
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.REVEAL.value,
        "board": flat_board,
        "gameType": gamestate.gametype,
        "winningBoard": gamestate.winning_spin,
    }
    gamestate.book.add_event(event)


def win_info_event(gamestate, include_padding_index=True):
    """
    include_padding_index: starts winning-symbol positions at row=1, to account for top/bottom symbol inclusion in board
    """
    win_data_copy = {}
    win_data_copy["wins"] = deepcopy(gamestate.win_data["wins"])
    for idx, w in enumerate(win_data_copy["wins"]):
        if include_padding_index:
            new_positions = []
            for p in w["positions"]:
                new_positions.append({"reel": p["reel"], "row": p["row"] + 1})
        else:
            new_positions = w["positions"]

        win_data_copy["wins"][idx]["win"] = int(
            round(min(win_data_copy["wins"][idx]["win"], gamestate.config.wincap) * 100, 0)
        )
        win_data_copy["wins"][idx]["positions"] = new_positions
        if "meta" in win_data_copy["wins"][idx]:
            win_data_copy["wins"][idx]["meta"]["winWithoutMult"] = int(
                int(
                    min(
                        win_data_copy["wins"][idx]["meta"]["winWithoutMult"] * 100,
                        gamestate.config.wincap * 100,
                    ),
                )
            )
            if "overlay" in win_data_copy["wins"][idx]["meta"] and include_padding_index:
                win_data_copy["wins"][idx]["meta"]["overlay"]["row"] += 1

    mapping = {
        str({"reel": 0, "row": 0}): 0,
        str({"reel": 0, "row": 1}): 1,
        str({"reel": 0, "row": 2}): 2,
        str({"reel": 1, "row": 0}): 3,
        str({"reel": 1, "row": 1}): 4,
        str({"reel": 1, "row": 2}): 5,
        str({"reel": 2, "row": 0}): 6,
        str({"reel": 2, "row": 1}): 7,
        str({"reel": 2, "row": 2}): 8,
    }
    new_wins = {}
    assert len(win_data_copy["wins"]) <= 1
    for idx in range(len(win_data_copy["wins"])):
        pos_flat = []
        for _, p in enumerate(win_data_copy["wins"][idx]["positions"]):
            pos_flat.append(mapping[str(p)])
        win_data_copy["wins"][idx]["positions"] = pos_flat
        new_wins["symbol"] = "P"
        new_wins["win"] = win_data_copy["wins"][0]["win"]
        new_wins["positions"] = pos_flat
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.WIN_DATA.value,
        "totalWin": int(round(min(gamestate.win_data["totalWin"], gamestate.config.wincap) * 100, 0)),
        "wins": new_wins,
    }
    gamestate.book.add_event(event)
