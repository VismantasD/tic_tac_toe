import unittest
import deepTic
from distutils.archive_util import make_archive

class TestSymmetryMethods( unittest.TestCase ):

    def testBasicPermutations( self ):
        testState = tuple( range( 9 ) )
        s = deepTic.Symmetries()
        self.assertEqual( s.initPermute( testState, 'e'), testState )
        self.assertEqual( s.initPermute( testState, 'r'),  ( 2, 5, 8, 1, 4, 7, 0, 3, 6 ) )
        self.assertEqual( s.initPermute( testState, 'm'), ( 6, 7, 8, 3, 4, 5, 0, 1, 2 ) )
        
    def testInvariant( self ):
        '''
        test if all permutations of the same state 
        result in the same invariante state
        '''
        testState = tuple( range(8, -1, -1) )
        s = deepTic.Symmetries()
        for permIndex in range(len(s.allSymmetries)):
            permutedState = s.permuteState( testState, permIndex )
            r = s.invariant( permutedState )            
            self.assertEqual( r[0], testState )            
            
class TestGameMethods( unittest.TestCase ):

    def testTerminalState( self ):
        g = deepTic.Game()
        for x in xrange( 1, 3 ):
            #test for terminal state in the rows
            self.assertTrue( g.terminalState( ( x, x, x, 0, 0, 0, 0, 0, 0 ) ) )
            self.assertTrue( g.terminalState( ( 0, 0, 0, x, x, x, 0, 0, 0 ) ) )
            self.assertTrue( g.terminalState( ( 0, 0, 0, 0, 0, 0, x, x, x ) ) )
            
            #test for terminal state in the columns
            self.assertTrue( g.terminalState( ( x, 0, 0, x, 0, 0, x, 0, 0 ) ) )
            self.assertTrue( g.terminalState( ( 0, x, 0, 0, x, 0, 0, x, 0 ) ) )
            self.assertTrue( g.terminalState( ( 0, 0, x, 0, 0, x, 0, 0, x ) ) )
            
            #test for for terminal state in the diagonals
            self.assertTrue( g.terminalState( ( x, 0, 0, 0, x, 0, 0, 0, x ) ) )
            self.assertTrue( g.terminalState( ( 0, 0, x, 0, x, 0, x, 0, 0 ) ) )
            
        self.assertFalse( g.terminalState( ( 1, 2, 1, 0, 0, 0, 0, 0, 0 ) ) )
        self.assertFalse( g.terminalState( ( 1, 1, 2, 0, 0, 0, 0, 0, 0 ) ) )
        self.assertFalse( g.terminalState( ( 2, 1, 1, 0, 0, 0, 0, 0, 0 ) ) )
        
        self.assertFalse( g.terminalState( ( 2, 1, 2, 1, 2, 1, 1, 2, 1 ) ) )
        
    def testGetAvailableActions( self ):
        #emtpy board should give nine actions
        self.assertEqual( deepTic.Game( ( 0, 0, 0, 0, 0, 0, 0, 0, 0 ) ).getAvailableActions( False ), tuple( range( 9 ) ) )
        #full boad should give 0 actions
        self.assertEqual( deepTic.Game( ( 2, 1, 2, 1, 2, 1, 1, 2, 1 ) ).getAvailableActions( False ), tuple() )
        
        fullBoard = ( 2, 1, 2, 1, 2, 1, 1, 2, 1 )
        #test some other configurations of the boad being filled
        for x in xrange(10):
            if x > 0:
                state = fullBoard[:-x]+ (0,) * x
            else:
                state = fullBoard
            self.assertEqual( deepTic.Game( state ).getAvailableActions( False ), tuple( range(9-x, 9, 1 ) ) )   

    def testSetState( self ):  
        for x in xrange(9):
            g = deepTic.Game()
            g.setState( x, 1 , False )
            expectedState = [ 0, ] * 9
            expectedState[ x ] = 1            
            self.assertEqual( g.returnState( False ), tuple( expectedState ) )
            
    def testTie( self ):
        g = deepTic.Game( ( 2, 1, 2, 1, 2, 1, 1, 2, 1 ) ) 
        self.assertTrue( g.tie() )
        g = deepTic.Game( ( 1, 1, 2, 1, 2, 1, 1, 2, 1 ) ) 
        self.assertFalse( g.tie() )
        
        
        
class TestGameEnvironment( unittest.TestCase ):

    class MockPlayer():
        def __init__( self, moveSequence ):
            self.moveSequence = moveSequence
            self.useSymmetry = False
            self.updateCount = 0
            self.updatesReceived = []
            
        def makeMove( self, state, actions ):
            return self.moveSequence.pop( 0 )
        
        def update( self, update ):
            self.updateCount += 1
            self.updatesReceived.append( update )           
                        
    def testPlay( self ):
        #check if the game ends in a win for player one
        p1 = TestGameEnvironment.MockPlayer( [ 4, 0, 8 ] )
        p2 = TestGameEnvironment.MockPlayer( [ 1, 7 ] )
        gameInstance = deepTic.GameEnvironment( p1, p2, deepTic.Game() )
        self.assertEqual(gameInstance.play(), 1 )
        self.assertEqual( p1.updateCount, 3 )
        self.assertEqual( p2.updateCount, 2 )

        #check if the game ends up in a tie
        p1 = TestGameEnvironment.MockPlayer( [ 0, 2, 4, 5, 7 ] ) 
        p2 = TestGameEnvironment.MockPlayer( [ 1, 6, 8, 3 ] )         
        gameInstance = deepTic.GameEnvironment( p1, p2, deepTic.Game() )
        self.assertEqual( gameInstance.play(), 0 )
        self.assertEqual( p1.updateCount, 5 )
        self.assertEqual( p2.updateCount, 4 )

        #check that the players receive expected updates, as the 
        #game progresses
        player1ExpectedUpdates = [
            { 's1': ( 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 'a1': 0, 
              's2': ( 1, 0, 0, 0, 2, 0, 0, 0, 0 ), 'a2': 2,
              'r': 0, 't': False },                        
            { 's1': ( 1, 0, 0, 0, 2, 0, 0, 0, 0 ), 'a1': 2, 
              's2': ( 1, 2, 1, 0, 2, 0, 0, 0, 0 ), 'a2': 8,  
              'r': 0, 't': False },
            { 's1': ( 1, 2, 1, 0, 2, 0, 0, 0, 0 ), 'a1': 8,
              's2': ( 1, 2, 1, 0, 2, 0, 0, 2, 1 ), 'a2': -1, 
              'r': -1, 't': True } ]
        
        player2ExpectedUpdates = [
            { 's1': (1, 0, 0, 0, 0, 0, 0, 0, 0), 'a1': 4,
              's2': (1, 0, 1, 0, 2, 0, 0, 0, 0), 'a2': 1, 
              'r': 0, 't': False },
            { 's1': (1, 0, 1, 0, 2, 0, 0, 0, 0), 'a1': 1, 
              's2': (1, 2, 1, 0, 2, 0, 0, 0, 1), 'a2': 7, 
              'r': 0, 't': False },
            { 's1': (1, 2, 1, 0, 2, 0, 0, 0, 1), 'a1': 7,  
              's2': (1, 2, 1, 0, 2, 0, 0, 2, 1), 'a2': -1, 
              'r': 1, 't': True } ]

        p1 = TestGameEnvironment.MockPlayer( [ 0, 2, 8 ] ) 
        p2 = TestGameEnvironment.MockPlayer( [ 4, 1, 7 ] ) 
        gameInstance = deepTic.GameEnvironment( p1, p2, deepTic.Game() )
        self.assertEqual( gameInstance.play(), -1 )
        self.assertEqual( p1.updatesReceived, player1ExpectedUpdates )
        self.assertEqual( p2.updatesReceived, player2ExpectedUpdates )

class TestAIPlayer( unittest.TestCase ):
    
    def testUpating( self ):
        aiPlayer = deepTic.AIPlayer( 0 )
        s1 = ( 1, )
        s2 = ( 2, )
        #make a few moves and initialize states s1 and s2
        a1 = aiPlayer.makeMove( s1, (1, 2) )
        a2 = aiPlayer.makeMove( s2, (3, 4) )
        #send an update corresponding to the moves made
        aiPlayer.update( { 's1': s1, 's2': s2, 'a1':a1, 'a2':a2 , 'r':-1, 't': False } )
        #after observing negative reward for a1 we expect the agent to prefer the other action
        self.assertNotEqual( aiPlayer.makeMove( s1, ( 1, 2 ) ), a1 )
        aiPlayer.update( { 's1': s1, 's2': s2, 'a1':2, 'a2':a2, 'r':-3, 't': False } )
        self.assertEqual( aiPlayer.makeMove( s1, ( 1, 2 ) ), a1 )
        
if __name__ == '__main__':
    unittest.main()
