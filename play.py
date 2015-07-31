from __future__ import division
import argparse
import deepTic
import random

#Helper functions for simplistic UI        
def doYouWantToPlay():
    print( "Shall we play a game? (y/n)" )
    x = '_'
    while x not in [ 'y', 'n' ]:
        x = raw_input()
    return x == 'y'

def chooseSide():
    print( "Choose 'x' or 'o':" )
    x = '_'
    while x not in [ 'x', 'o' ]:
        x = raw_input()
    return x == 'x'

if __name__ == "__main__":  
    random.seed( None ) #initialize with system time
    parser = argparse.ArgumentParser()
    parser.add_argument("--brain", nargs='?', help='Path to pre-trained policy')
    args = parser.parse_args()
    if args.brain is not None:
        print( "AI is being loaded from file." )
        opponent = deepTic.AIPlayer( 0.2, args.brain )
    else:  
        opponent = deepTic.AIPlayer( 0.2 )
        print( "Training AI. Please wait." )
        gameResults = []
        nOfEpisodes = 50000
        for x in range( nOfEpisodes ):        
            if x % 10000 == 0:
                print( "{:.0%} done".format( x / nOfEpisodes ) ) 
            g = deepTic.GameEnvironment( opponent, opponent, deepTic.Game(None, False))
            gameResults.append( g.play() )
        print( "Training statistics:" )
        print( "Number of ties: {}".format( sum( list( 1 for x in gameResults if x == 0) ) ) )
        print( "Number of wins as Player 1: {}".format( sum( list( 1 for x in gameResults if x == 1) ) ) )
        print( "Number of wins as Player 2: {}".format( sum( list( 1 for x in gameResults if x == -1) ) ) )


    opponent.competitionMode = True
    
    print("These are all available actions in the game:\n\n0|1|2\n-----\n3|4|5\n-----\n6|7|8\n\n")
    
    while doYouWantToPlay():
        if (chooseSide()):
            g = deepTic.GameEnvironment( deepTic.HumanPlayer(), opponent, deepTic.Game() )
        else:
            g = deepTic.GameEnvironment( opponent, deepTic.HumanPlayer(), deepTic.Game() )
        g.debug = True
        g.play()
