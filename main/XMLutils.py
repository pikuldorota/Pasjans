"""
Created by pikuldorota

History of modification:
pikuldorota      7 Jan, 2017    Init version
pikuldorota     12 Jan, 2017    Add adding and cleaning moves save and
                                rename previous methods
pikuldorota     14 Jan, 2017    Add undoing last move and removing it from xml
pikuldorota     27 Jan, 2017    Adapt to maximum line length from PEP 8
pikuldorota     28 Jan, 2017    Add support for double decked games
                                and subfields
"""
from Field import Deck, LongDeck
from Application import double_deck_games


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
        elif isinstance(field, LongDeck):
            for subfield in field.show_subfields():
                xml_subfield = document.createElement("Subfield")
                xml_subfield.appendChild(document.createTextNode(''))
                for card in subfield.show_cards():
                    xml_card = document.createElement("Card2")
                    xml_card.setAttribute("rank", card.rank().name)
                    xml_card.setAttribute("suit", card.suit().name)
                    xml_card.setAttribute("is_shown", str(card.is_shown()))
                    xml_subfield.appendChild(xml_card)
                xml_field.appendChild(xml_subfield)
        latest_card_positions.appendChild(xml_field)


def game_state_from_xml(board, deck, document):
    """Used to put cards on board according to saved in document state"""
    deck = deck[:]
    root = document.documentElement
    latest = root.getElementsByTagName("LatestCardPositions")[0]
    fields = latest.getElementsByTagName("Field")
    for field_xml, field_board in zip(fields, board):
        field_board.clear()
        for card_xml in field_xml.getElementsByTagName("Card"):
            card_board = next((card for card in deck
                               if card.is_xml_card(card_xml)), None)
            field_board.add(card_board)
            deck.remove(card_board)
            if card_xml.getAttribute("is_shown") == "True":
                card_board.show()
            else:
                card_board.hide()
        for idx in field_xml.getElementsByTagName("Index"):
            field_board.set_index(int(idx.getAttribute("idx")))
        for i, subfield_xml in enumerate(field_xml.getElementsByTagName
                                         ("Subfield")):
            for card_xml in subfield_xml.getElementsByTagName("Card2"):
                card_board = next((card for card in deck
                                   if card.is_xml_card(card_xml)), None)
                field_board.show_subfields()[i].add(card_board)
                deck.remove(card_board)
                if card_xml.getAttribute("is_shown") == "True":
                    card_board.show()
                else:
                    card_board.hide()


def add_move_to_xml(idx_from, idx_to, cards, next_card_reveled, subfield, document):
    """Used to save in memory information about each move and click"""
    moves = document.documentElement.getElementsByTagName("Moves")[0]
    xml_move = document.createElement("Move")
    xml_move.appendChild(document.createTextNode(''))
    xml_move.setAttribute("field_index_from", str(idx_from))
    xml_move.setAttribute("field_index_to", str(idx_to))
    xml_move.setAttribute("next_card_reveled", str(next_card_reveled))
    xml_move.setAttribute("subfield", str(subfield))
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
    subfield = int(move.getAttribute("subfield"))
    if subfield >= 0:
        field_from = field_from.show_subfields()[subfield]
    how_many = len(move.getElementsByTagName("Card"))
    if how_many:
        if hide_last == "True":
            field_from.hide_last()
        cards = field_to.show_cards()[-how_many:]
        field_to.take(cards)
        field_from.add(cards)
    else:
        if isinstance(field_from, Deck):
            field_from.set_index(field_from.get_index()-1)
        else:
            field_from.undo()
    moves.removeChild(move)


def clean_moves_xml(document):
    """Cleans all moves from xml file"""
    root = document.documentElement
    for child in root.getElementsByTagName("Moves")[0].childNodes[1:]:
        root.getElementsByTagName("Moves")[0].removeChild(child)

