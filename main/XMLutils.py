"""
Created by pikuldorota

History of modification:
pikuldorota      7 Jan, 2017    Init version
pikuldorota     12 Jan, 2017    Add adding and cleaning moves save and
                                rename previous methods
pikuldorota     14 Jan, 2017    Add undoing last move and removing it from xml
pikuldorota     27 Jan, 2017    Adapt to maximum line length from PEP 8
"""
from Field import Deck


def game_state_to_xml(board, document):
    """Used to change document so it shows actual state of board"""
    root = document.documentElement
    latest_card_positions = root.getElementsByTagName("LatestCardPositions")[0]
    for child in latest_card_positions.childNodes[1:]:
        latest_card_positions.removeChild(child)
    for field in board:
        xml_field = document.createElement("Field")
        xml_field.appendChild(document.createTextNode(''))
        for card in field.show_cards():
            xml_card = document.createElement("Card")
            xml_card.setAttribute("rank", card.rank().name)
            xml_card.setAttribute("suit", card.suit().name)
            xml_card.setAttribute("is_shown", str(card.is_shown()))
            xml_field.appendChild(xml_card)
        if isinstance(field, Deck):
            xml_idx = document.createElement("Index")
            xml_idx.setAttribute("idx", str(field.get_index()))
            xml_field.appendChild(xml_idx)
        latest_card_positions.appendChild(xml_field)


def game_state_from_xml(board, deck, document):
    """Used to put cards on board according to saved in document state"""
    root = document.documentElement
    latest = root.getElementsByTagName("LatestCardPositions")[0]
    fields = latest.getElementsByTagName("Field")
    for field_xml, field_board in zip(fields, board):
        field_board.clear()
        for card_xml in field_xml.getElementsByTagName("Card"):
            card_board = next((card for card in deck
                               if card.is_xml_card(card_xml)), None)
            field_board.add(card_board)
            if card_xml.getAttribute("is_shown") == "True":
                card_board.show()
            else:
                card_board.hide()
        for idx in field_xml.getElementsByTagName("Index"):
            field_board.set_index(idx.getAttribute("idx"))


def add_move_to_xml(idx_from, idx_to, cards, next_card_reveled, document):
    """Used to save in memory information about each move and click"""
    moves = document.documentElement.getElementsByTagName("Moves")[0]
    xml_move = document.createElement("Move")
    xml_move.appendChild(document.createTextNode(''))
    xml_move.setAttribute("field_index_from", str(idx_from))
    xml_move.setAttribute("field_index_to", str(idx_to))
    xml_move.setAttribute("next_card_reveled", str(next_card_reveled))
    for card in cards:
        xml_card = document.createElement("Card")
        xml_card.setAttribute("rank", card.rank().name)
        xml_card.setAttribute("suit", card.suit().name)
        xml_move.appendChild(xml_card)
    moves.appendChild(xml_move)


def undo_last_move(board, deck, document):
    """Used to undo last move and to remove it from xml"""
    moves = document.documentElement.getElementsByTagName("Moves")[0]
    if not moves.getElementsByTagName("Move"):
        return
    move = moves.getElementsByTagName("Move")[-1]
    field_from = board[int(move.getAttribute("field_index_from"))]
    field_to = board[int(move.getAttribute("field_index_to"))]
    hide_last = move.getAttribute("next_card_reveled")
    cards = []
    for xml_card in move.getElementsByTagName("Card"):
        card = next((card for card in deck
                     if card.is_xml_card(xml_card)), None)
        cards.append(card)
    if cards:
        if hide_last == "True":
            field_from.hide_last()
        field_to.take(cards)
        if len(cards) == 1:
            field_from.add(cards[0])
        else:
            field_from.add(cards)
    else:
        field_from.set_index(field_from.get_index()-1)
    moves.removeChild(move)


def clean_moves_xml(document):
    """Cleans all moves from xml file"""
    root = document.documentElement
    for child in root.getElementsByTagName("Moves")[0].childNodes[1:]:
        root.getElementsByTagName("Moves")[0].removeChild(child)

