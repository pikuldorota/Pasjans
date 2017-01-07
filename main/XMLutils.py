"""
Created by pikuldorota

History of modification:
pikuldorota      7 Jan, 2017    Init version
"""
from Field import Deck


def to_xml(board, document):
    """Used to change document so it shows actual state of board"""
    root = document.documentElement
    for child in root.getElementsByTagName("LatestCardPositions")[0].childNodes[1:]:
        root.getElementsByTagName("LatestCardPositions")[0].removeChild(child)
    for field in board:
        xml = document.createElement("field")
        xml.appendChild(document.createTextNode(''))
        for card in field.show_cards():
            xmlcard = document.createElement("card")
            xmlcard.setAttribute("rank", card.rank().name)
            xmlcard.setAttribute("suit", card.suit().name)
            xmlcard.setAttribute("is_shown", str(card.is_shown()))
            xml.appendChild(xmlcard)
        if isinstance(field, Deck):
            xmlidx = document.createElement("index")
            xmlidx.setAttribute("idx", str(field.get_index()))
            xml.appendChild(xmlidx)
        root.getElementsByTagName("LatestCardPositions")[0].appendChild(xml)


def from_xml(board, deck, document):
    """Used to put cards on board according to saved in document state"""
    latest = document.documentElement.getElementsByTagName("LatestCardPositions")[0]
    for field_xml, field_board in zip(latest.getElementsByTagName("field"), board):
        field_board.clear()
        for card_xml in field_xml.getElementsByTagName("card"):
            card_board = next((card for card in deck if card.is_xml_card(card_xml)), None)
            field_board.add(card_board)
            if card_xml.getAttribute("is_shown") == "True":
                card_board.show()
            else:
                card_board.hide()
        for idx in field_xml.getElementsByTagName("index"):
            field_board.set_index(idx.getAttribute("idx"))
