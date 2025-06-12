from src.events.event_constants import EventConstants


def win_info_event(gamestate):
    """
    include_padding_index: starts winning-symbol positions at row=1, to account for top/bottom symbol inclusion in board
    """
    event = {
        "index": len(gamestate.book.events),
        "type": EventConstants.WIN_DATA.value,
        "totalWin": int(round(min(gamestate.win_data["totalWin"], gamestate.config.wincap) * 100, 0)),
    }
    gamestate.book.add_event(event)
