from __future__ import division
import deepTic
import pickle
import random

def experiment(sarsa, defVal, outputFileName, selfPlay, symmetry ):
    print outputFileName
    canonicalPlayer = deepTic.AIPlayer( 0, "brainy.brain" )
    canonicalPlayer.competitionMode = True
    canonicalPlayer.useSymmetry = True
    
    nOfEpisodes = 5000
    nOfAgentIterations = 200
    totalResults = [0.0] * nOfEpisodes
    for agentIndex in xrange( nOfAgentIterations ):        
        if agentIndex % 10 == 0: 
            print( "{:.0%} done".format( agentIndex / nOfAgentIterations ) )  
        trainee = deepTic.AIPlayer( 0.1 )
        trainee.sarsa = sarsa
        trainee.initialStateActionValue = defVal
        trainee.useSymmetry = symmetry
        if selfPlay:
            canonicalPlayer = trainee
        gameResults = [ 0.0 ] * nOfEpisodes 
        for episodeNumber in xrange( nOfEpisodes):
            trainee.setEps( 0.2 * ( 1 - episodeNumber / float(nOfEpisodes ) ) )
            gresult = deepTic.GameEnvironment( trainee, canonicalPlayer, deepTic.Game() ).play()
            gameResults[ episodeNumber ] = gresult
        totalResults = list( a + b for ( a, b ) in zip( totalResults, gameResults ) )
    totalResults = list( x / float( nOfAgentIterations ) for x in totalResults )
    with open( outputFileName, 'wt' ) as f:
        pickle.dump( totalResults, f )

random.seed( 42 );


experiment( sarsa = True, defVal = 0.01, outputFileName = 'expResults/noSymmetry.pickle', selfPlay=False, symmetry = False)
experiment( sarsa = False, defVal = 0.01, outputFileName = 'expResults/QnoSymmetry.pickle', selfPlay=False, symmetry = False)
experiment( sarsa = True, defVal = 0.01, outputFileName = 'expResults/sarsa01.pickle', selfPlay=False, symmetry = True)
experiment( sarsa = True, defVal = 1.0,  outputFileName = 'expResults/sarsa1.pickle', selfPlay=False, symmetry = True )
experiment( sarsa = False, defVal = 0.01, outputFileName = 'expResults/Q01.pickle', selfPlay=False, symmetry = True )
experiment( sarsa = False, defVal = 1.0, outputFileName = 'expResults/Q1.pickle', selfPlay=False, symmetry = True )
