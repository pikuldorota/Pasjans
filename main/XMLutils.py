"""
Created by pikuldorota

History of modification:
pikuldorota      7 Jan, 2017    Init version
pikuldorota     12 Jan, 2017    Add adding and cleaning moves save and rename previous methods
"""
from Field import Deck


def game_state_to_xml(board, document):
    """Used to change document so it shows actual state of board"""
    root = document.documentElement
    for child in root.getElementsByTagName("LatestCardPositions")[0].childNodes[1:]:
        root.getElementsByTagName("LatestCardPositions")[0].removeChild(child)
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
        root.getElementsByTagName("LatestCardPositions")[0].appendChild(xml_field)


def game_state_from_xml(board, deck, document):
    """Used to put cards on board according to saved in document state"""
    latest = document.documentElement.getElementsByTagName("LatestCardPositions")[0]
    for field_xml, field_board in zip(latest.getElementsByTagName("Field"), board):
        field_board.clear()
        for card_xml in field_xml.getElementsByTagName("Card"):
            card_board = next((card for card in deck if card.is_xml_card(card_xml)), None)
            field_board.add(card_board)
            if card_xml.getAttribute("is_shown") == "True":
                card_board.show()
            else:
                card_board.hide()
        for idx in field_xml.getElementsByTagName("index"):
            field_board.set_index(idx.getAttribute("idx"))


def add_move_to_xml(idx_from, idx_to, cards, next_card_reveled, document, index_change=None):
    """Used to save in memory information about each move and click"""
    moves = document.documentElement.getElementsByTagName("Moves")[0]
    xml_move = document.createElement("Move")
    xml_move.appendChild(document.createTextNode(''))
    xml_move.setAttribute("field_index_from", str(idx_from))
    xml_move.setAttribute("field_index_to", str(idx_to))
    xml_move.setAttribute("next_card_reveled", str(next_card_reveled))
    if index_change:
        xml_index = document.createElement("index_changed")
        xml_index.setAttribute("idx", str(index_change))
        xml_move.appendChild(xml_index)
    for card in cards:
        xml_card = document.createElement("Card")
        xml_card.setAttribute("rank", card.rank().name)
        xml_card.setAttribute("suit", card.suit().name)
        xml_move.appendChild(xml_card)
    moves.appendChild(xml_move)


def clean_moves_xml(document):
    """Cleans all moves from xml file"""
    root = document.documentElement
    for child in root.getElementsByTagName("Moves")[0].childNodes[1:]:
        root.getElementsByTagName("Moves")[0].removeChild(child)

