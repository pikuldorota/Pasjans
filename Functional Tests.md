# Functional tests
Below there is list of functional tests. To perform them you need to know basics about game. To find out about type of fields and rules of patience look into [README.md](./README.md) file
## First lunch test
This test is to check that on the very first run the game runs in right conditions.

##### Pre conditions:

> Make sure that all files in `save_files` folder are exactly the same as the ones in the repository

##### Flow
> Run the game. Check that loaded patience is klondike and that cards are dealt freshly.

##### Post conditions

> Close the game.

## Another launch test

Checks if save files are working correctly.

##### Flow

> Run the game. Then change patience and make some moves. Remember state of game. Shut down the game and launch it again. Check if it loaded the remembered state of game.

##### Post conditions

> Shut down the game.

## New game option

Checks if shuffling game is working correctly.

##### Pre conditions

> Run the game.

##### Flow

> Remember state of actual game. Click on `new game` button. Check if state of game has changed and if the cards are distributed correctly. Repeat this on all available patience.

##### Post conditions

> Close the game.

## Change game option

##### Pre conditions

> Run the game.

##### Flow

> Click on the `change game` button then click on `algerian` button. Check if loaded game looks like it should. Repeat for all available patiences.

##### Post conditions

> Shut down the game.

## Undo option

This test case may include some more steps to find card which can be moved. It can be achieved by either solving patience or clicking on `new game` option. It checks all possible moves in the game.
##### Pre conditions

> Run the game. Then set patience to be klondike.

##### Flow

> Click on Deck and then on `undo` button. Check if game is back to first state. Then put card on Stack and click on `undo`. Check if this move was undone too. At last do the same with putting one card on Pile and moving few cards between Piles. Then change patience to algerian. Click on deck and undo this move. Check if it is undone. Then do this move again to see if cards were distributed the same as before move. Now change patience to osmosis. Put card on top Cascade and undo this move. Again check if it was undone. Then put card on second Cascade. Check if after clicking `undo` button the card get back to previous place. Change game to fifteen puzzle. Move one card and check if `undo` works correctly. Then move two cards and check working of this button again. Click `new game` button. Check that `undo` button has no effect.

##### Post conditions

> Close the game.

## Stack
This test checks whether this field works correctly. It may include a lot more moves to find proper cards for test.

##### Pre conditions

> Run the game and choose algerian or natali patience.

##### Flow

> Take any card that is neither ace nor king. Try to put it on Stack with king symbol and then on Stack with ace symbol. None of this moves shall happen. Then find some ace and put it on ace Stack. It should have effect. Do the same with king card and king stack. Take two that is in different colour then ace. Try putting it on ace which shall not happen. Find some card in the same colour as ace have but not being two. Try putting it on ace which shall have no effect. Then find two with the same colour as ace has. Put it on ace and check that it happens. Then take dame with different colour then king and try to put it on king. Do the same with some card in colour of king but not being dame. Both shall have no effect. Then find dame with colour of king and put it on king. It shall happen. Then find second king with the same colour as previous one and put it on dame. It shall not happen. At last find second ace with the same colour as previous and try to put it on to. It too should not have effect.

##### Post conditions

> Close the game.

## Pile

This is to check all possible moves on Piles. It may include a lot of several additional moves to find proper cards

##### Pre conditions

> Run the game and choose klondike patience.

##### Flow

> Check that possible moves occurs and impossible doesn't.
> Moves that shall not happen:
>  - putting card in the same colour as previous one, rank should be one lower (e.g. dame over king)
>  - putting card in wrong rank when colour is opposite (e.g king over dame, two over ten)
>  - moving few cards where the first is wrong (same conditions for first card as in above two cases)

> Moves that should happen:
> - putting card in different colour with rank one lower (e.g. five over six)
> - moving several cards where the first one is correct (same conditions as in the previous one)

> After checking all that change patience to algerian. Moves that shall not occur:
> - putting card in the same colour as one above
> - putting card with rank which is not one different from previous one (e.g. four over six, ten over five)
> - moving few cards were the last one is wrong according to conditions above

> Moves that should happen:
> - putting card with opposite colour that the previous one and has rank one lower or higher than the previous (e.g. ten over nine, nine over ten)
> - several cards where the last one fulfills conditions from previous. The cards shall be putted in reverse order then they was before.

#####Post conditions

> Close the game.

## Deck

Aim of this test is to check if deck is functioning right.

##### Pre conditions

> Run the game and choose one of games using Deck which are canfield, klondike, natali and osmosis.

##### Flow

> Check that clicking on the left part will show new card on the left. Take this card and put on other field. Check that it disappeared from Deck and on the Deck is shown previously shown card. Click through Deck and check that it will get back to the beginning with showing cards.

##### Post conditions

> Close the game.

## Fours

It tests validating moves.

##### Pre conditions

> Run game and choose fifteen puzzle.

##### Flow

> Check that possible moves occurs and impossible doesn't.
> Moves that shouldn't happen:
> - putting card with the same rank as last on fours when it would be fifth card there.
> - putting card with different rank than the one on top of Fours

> Possible moves
> - any card moved on empty Fours
> - any cards where all have the same rank on empty Fours
> - card with the same rank as the top one on Fours not fully filled
> - cards where all have the same rank as the top one on Fours if after move there will be no more than four cards there

> Change patience to osmosis. Here Only possible moves shall be taking card from Fours. Nothing can be putted on it.

##### Post conditions

> Shut down the game

## Long Deck

This is checking that Long Deck works correctly

##### Pre conditions

> Run game and choose algerian patience.

##### Flow

> Check that it is possible to get card from any subfield and that you can't put any card on them. After licking on hidden card new cards shall be distributed to subfields. Click through it to see that clicking on empty field has no effect.

##### Post conditions

> Close the game.

## Unputtable Pile

It checks if Unputtable Pile is working fine.

##### Pre conditions

> Run game and choose canfield patience.

##### Flow

> Check if card can be taken from this field and that none card can be putted on it.

##### Post conditions

> Shut down game.

## Cascade

It checks if cascade works as it should.

##### Pre conditions

> Run game and choose osmosis patience.

##### Flow

> Check that listed below moves will not occur.
> - putting card with different suit than the ones on the Cascade.
> - putting card with good suit but with rank that is not to be found in the Cascade above

> Then check that on the top Cascade you can put any card with the same suit as the one already there. then check that in the next Cascade you can put only cards with ranks to be found in the row above. All cards in one Cascade shall have the same suit.

##### Post conditions

> Shut down the game.


## Finish game

This test case should be performed for all available patience.

##### Pre conditions

> Run game and choose patience. Click on `new game` button.

##### Flow

> Solve the patience. After final move check that congratulations are shown on the screen.

##### Post conditions

> Click on `new game` button and close the game.

