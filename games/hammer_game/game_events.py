from src.events.events import *


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
