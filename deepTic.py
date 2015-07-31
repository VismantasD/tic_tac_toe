import random
import pickle
from pprint import pprint

class Symmetries():
    """Class for finding invariant states of the tic tac toe board.
    
    Given a state will return an invariant state based on 8 symmetries
    
    Attributes:
        multiplier: multipliers for different positions on the board
        perm: encodings for basic allSymmetries of identity, rotation
            and mirroring
        allSymmetries: stores the recipies for generating all symmetry transformations
            using the primitive operations or rotation and mirroring
    """
    
    multiplier = tuple( range( 10 , 0, -1 ) )
    perm = {
        'r': ( 2, 5, 8, 1, 4, 7, 0, 3, 6 ), #rotation left
        'm': ( 6, 7, 8, 3, 4, 5, 0, 1, 2 ), #mirroring
        'e': tuple( range( 9 ) ) }          #identity
    allSymmetries = ( 'e', 'r', 'rr', 'rrr', 'm','mr','mrr','mrrr' )
    
    def __init__( self ):
        self.p = [[]] * len(Symmetries.allSymmetries) * 2
        state = tuple(range(9))
        #cache the allSymmetries
        for permutationIndex in range( len( Symmetries.allSymmetries ) ):
            r = self.initPermute( state, Symmetries.allSymmetries[ permutationIndex ] )  
            self.p[ permutationIndex ] = r           
            
    def invariant( self, state ):
        """For a given state returns its invariant under the symmetries.
        
        Args:
            state: A state of the tic tac toe board - tuple of length 9 with values 0, 1, or 2
        """
        
        bestState = tuple( state )
        bestPerm = 0
        bestScore = self.score( state )
        for p in range( len( Symmetries.allSymmetries ) ):
            newState = self.permuteState( state, p )
            tempScore = self.score( newState )
            if tempScore > bestScore:
                bestState, bestPerm, bestScore = newState, p, tempScore
        return ( bestState, bestPerm )
                
    def score( self, state ):
        """Returns a score for a state. This score is used to find invariante state.
        
        The state transformed with symmetry transformation with the highest score
        will be the invariant for a given state.
        
        Args:
            state: state of the tic tac toe board.        
        """
        return sum( a * 10**b for ( a, b ) in zip( state, Symmetries.multiplier ) )
     
    def initPermute( self, state, permutation ):
        """Permutes given state with a sequence of basic transformations"
        
        Args:
            state: state of the tic tac toe board.
            permutation: string of r and m letters encoding a sequence of 
                rotation and mirroring transformations.
        """
        
        cs = state        
        for op in permutation:        
            cs =  tuple( cs[ i ] for i in Symmetries.perm[ op ] )
        return cs
        
    def permuteState( self, state, permutationIndex ):
        """Permutes state using cached allSymmetries"""
        return tuple( state[ i ] for i in self.p[ permutationIndex ] )
        
    def permuteAction( self, action, permutation):
        """Gives action value under permutation"""
        return self.p[ permutation ].index( action )
    
    def inverseAction( self, action, permutation):
        """Given action under permutation, returns original action"""
        return self.p[ permutation ][ action ]


class Game( object ):
    """Represents the state of the game.
    
    Attributes:
        __state: stores the state of the game
        __invState: stores the invariante of the current
            state of the game ( it is cached for performance )
        debug: flag to indicate if debog output should be printed
        useSymmetry: stores instance of the Symmetries class for
            computing invariants of the states
        
    """
    def __init__( self, state = None, debug = False ):
        """
        Args:
            state: Initial state of the game
            debug: indicates if deboug output should be printed
        """
        
        if state is not None:
            self.__state = tuple( state )
        else:
            self.__state = [ 0 ] * 9
        self.debug = debug
        self.useSymmetry = Symmetries()
        self.__invState = self.useSymmetry.invariant( self.__state )

    @staticmethod
    def mapper( s ):
        """Maps numerical representations of the board
        to characters for printing
        """
        if s == 0:
            return ' '
        elif s == 1:
            return 'X'
        else:
            return 'O'
              
    def __repr__( self ):
        """Returns string representation of the board
        """ 
        lines = ( lineIndex for lineIndex in range( 3 ) )
        lineState = ( self.__state[ line * 3 : line * 3 + 3 ] for line in lines )        
        allLines = ( "|".join( ( Game.mapper( x ) for x in line ) ) for line in lineState )
        return "\n-----\n".join( allLines )  
        
    def setState( self, pos, symbol , usingSymmetry ):
        """Updates the state of the game.
        Args:
            pos: position on the board to be updates 0-8
            symbol: 0 - emptu, 1-X, 2-O
            usingSymmetry: flag, denoting if the 'pos' is given 
                w.r.t. the symmetric invariant of the current state (__invState)
                or not
        """
        if usingSymmetry:            
            pos = self.useSymmetry.inverseAction( pos, self.__invState[1] )
        self.__state[ pos ] = symbol
        self.__invState = self.useSymmetry.invariant( self.__state )
        if self.debug: print( self.__state )
    
    def returnState( self, usingSymmetry ):
        """Gives current state.
        
        Args:
            usingSymmetry: if True the symmetric invariant of the state is returned
        """
        if usingSymmetry:
            return self.__invState[ 0 ]            
        else:
            return tuple(self.__state)
    
    def terminalState( self, state ):
        """Checks if the state is in a wining position.
        
        Args:
            state: state of the board
        """
        if ( ( ( state[ 0 ] != 0) and ( state[ 0 ] == state[ 4 ] == state[ 8 ] ) ) or 
           ( ( state[ 2 ] != 0 ) and ( state[ 2 ] == state[ 4 ] == state[ 6 ] ) ) ):
            return True
        for line in range( 3 ):
            tmpLine = state[ line*3:line*3 + 3 ]
            tmpCol = state[ line:line + 2 * 3 + 1:3]
            if tmpLine[ 0 ] != 0 and all( ( x == tmpLine[ 0 ] for x in tmpLine ) ):
                return True
            if tmpCol[0] != 0 and all((x == tmpCol[0] for x in tmpCol)):
                return True
        return False
    
    def getAvailableActions( self, usingSymmetry ):
        """Returns all available actions in the current game state.
        
        Args:
            usingSymmetry: flag denoting if the actions should be returned 
                w.r.t the symmetric invariant of the current state or not.
        """
        if usingSymmetry:
            r = self.__invState[ 0 ]
            return tuple( i for (i, v) in enumerate( r ) if v == 0)           
        else:
            return tuple( i for (i, v) in enumerate( self.__state ) if v == 0)
    
    def end( self ):
        """Returns true if the game is in a terminal state with a player winning.
        """
        return self.terminalState( self.__state )
    
    def tie( self ):
        """Returns true if the game is in a terminal state which is a tie.
        """
        return (not self.end()) and (len( self.getAvailableActions( False ) ) == 0)
            
class Update( object ):
    '''
    Class to store SARSA updates to the agents
    '''
    def __init__( self, callback ):
        self.a1 = None  #action in first state
        self.s1 = None  #first state
        self.a2 = None  #action in subsequent state
        self.s2 = None  #subsequent state
        self.t = None   #denotes terminal state, it is used by agent to know to ignore s2 and a2 when doing update
        self.r = None   #reward experienced after taking a1 in s1
        self.firstPush = True   
        self.callback = callback    #agent who should receive this update
        
    def send( self ):
        '''
        Sends SARSA update to the registered agents
        '''
        r = {
            'a1': self.a1,
            'a2': self.a2,
            's1': self.s1,
            's2': self.s2,
             'r': self.r,
             't': self.t}
        self.callback.update( r )
        
    def push(self, state, action, reward, terminal):
        """Push data, to build an update packet for the agent.
        
        Args:
            state: state of the game
            action: action taken in the state
            reward: reward aboserved after taking that action
            terminal: flag denoting if the state is a terminal state
        """
        if self.firstPush:
            self.s2 = state
            self.a2 = action
            #we do not send update on first push, because
            #we do not have the full necessary information
            #for a full SARSA update (we have not seen the second state yet)
            self.firstPush = False
        else:
            self.a1 = self.a2
            self.s1 = self.s2
            self.a2 = action
            self.s2 = state
            self.t = terminal
            self.r = reward
            self.send()
            

class GameEnvironment( object ):
    """Class to manage the gameplay.
    
    Class manages the game-play: keeps the state of the game, notices when it
    the game has terminated, alternates player moves. Also keeps track of
    player actions and builds SARSA updates for the players and sends them
    at appropriate time.
    
    Attributes:
        __p1: Player one
        __p2: Player two
        __game: State of the game
        debug: Flag denoting if debug output should be printed
        sym: 
    """
    def __init__(self, p1, p2, game):
        """Constructor
        
        Args:
            p1: player one
            p2: player two
            game: game to play
        """
        self.__p1 = p1
        self.__p2 = p2
        self.__game = game
        self.debug = False
               
    def step( self, p1, p2, game, p1Update, p2Update, symbol ):
        """Conducts a single step of a game.

        Conducts a single step of a game. One player makes a move,
        the game state is updated. It is checked for termination
        cirterions and then appropriate updates of state, action and
        rewards are sent to the players.

        Args:
            p1: player one. The one who makes a move in this step
            p2: the other player
            game: object representing current state of the game
            p1Update: object managing updates to the player 1
            p2Update: object managing updates to the player 2
            symbol: symbol to be placed on the board by the current
                player

        Returns:
            1 if the game is in terminal winning position
            0 if the game ended in a tie
            -1 if the game continues 
        """
        currentGameState = game.returnState( p1.useSymmetry )
        move = p1.makeMove( currentGameState, game.getAvailableActions( p1.useSymmetry ) )        
        p1Update.push( currentGameState, move, 0, False )
        game.setState( move, symbol, p1.useSymmetry )           
        if game.end():
            currentGameState = game.returnState( p1.useSymmetry )
            p1Update.push( currentGameState, -1, 1,  True )
            currentGameState = game.returnState( p2.useSymmetry )
            p2Update.push( currentGameState, -1, -1, True )
            return 1
        elif game.tie():
            currentGameState = game.returnState( p1.useSymmetry )
            p1Update.push( currentGameState, -1, 0,  True )
            currentGameState = game.returnState( p2.useSymmetry )
            p2Update.push( currentGameState, -1, 0, True )
            return 0
        else:            
            return -1
        
    def play( self ):
        """Conducts the game play.

        Starts the game. Alternates players, keeps track of the state
        of the game and it termination.

        Returns:
            1 if Player 1 won
            0 if the game ended in a tie
            -1 if the Player 1 lost
        """
        currentPlayer = 1
        result = -1
        if self.debug: 
            print( self.__game )
            print( "======" )
        p1Update = Update( self.__p1 )
        p2Update = Update( self.__p2 )
        while result == -1:    
            if self.debug: print( "Player's {} move!".format( currentPlayer ) )        
            if currentPlayer == 1:
                result = self.step( self.__p1, self.__p2, self.__game, p1Update, p2Update, 1 )
                if result == -1: 
                    currentPlayer = 2
            else:                                
                result = self.step( self.__p2, self.__p1, self.__game, p2Update, p1Update, 2 )
                if result == -1: 
                    currentPlayer = 1
            if self.debug: 
                print( self.__game )
                print( "======" )
        if self.debug: 
            if result * currentPlayer == 0:
                print( "It is a tie!" )
            elif result * currentPlayer == 1:
                print( "Player one wins!" )
            elif result * currentPlayer == 2:
                print( "Player two wins!" )
        if result * currentPlayer == 2:
            return -1
        else:
            return result
            
            
class HumanPlayer( object ):
    """Class representing a human player.
    """
    def __init__( self ):
        self.debug = False
        self.useSymmetry = False
        
    def makeMove( self, _, possibleActions ):
        """Get the move from they keyboard
        
        Args:
            state: but for human player we do not need the state
            possibleActions: actions possible in the current state
        """

        moveDone = False
        print( "You have the following choices: {}".format( possibleActions ) )
        while not moveDone:
            try:
                action = int(raw_input())
            except ValueError:
                continue
            if action in possibleActions:
                return action
            
    def update( self, state ):
        """Method to update the startegy. Irrelevant for human player.
        """
        if self.debug: 
            print( "Update received: ")
            pprint( state )


class AIPlayer( object ):
    """Represents an AI player.
    
    Attributes:
        __q: State action pair values. Hash table storing the values
            for all encountered state action pairs.
        __eps: The epsilon parameter for the epsilon-greedy strategy.
        debug: Flag denoting if the debug output should be printed.
        competitionMode: flag denoting if the agent should do exploratory moves
            and update its strategy based on experience. When set to True
            agent does not do policy imporovements and uses completely
            greedy strategy.
        sarsa: Flag denoting if SARSA ( when set to True ) or Q-learning (when set 
            to False) algorithm should be used when updating state action pair
            values.
        initialStateActionValue: Initial value for state action pairs, when initialising 
            them.
        learningRate: learning rate as define in SARSA and Q-learning algorithms
        useSymmetry: Flag denoting if the agent is aware of symmetric states.
                       
    """
    
    def __init__( self, eps, pretaindFile = None ):
        """Constructor
        
        Args:
            eps: epsilon parameter for the epsilon greedy strattegy.
                controls how may exploratory moves the agent does.
            pretrainedFile: path to file containint pretrained state action
                values ( can be created using saveState method ).
        """
        if pretaindFile is None:
            self.__q = {}
        else:
            with open( pretaindFile, 'rt' ) as f:
                self.__q = pickle.load( f )
        self.__eps = eps
        self.debug = False
        self.competitionMode = False
        self.sarsa = True
        self.initialStateActionValue = 0.01
        self.learningRate = 0.2
        self.useSymmetry = True
        
    def saveState( self, fileName ):
        """Saves the current state of state action pair values.
        
        The saved data can be used to initialise new instances
        of the agent.
        """
        with open( fileName, 'wt') as f:
            pickle.dump( self.__q, f )
            
    def setEps(self, eps ):
        """Sets the epsilon parameter
        """
        self.__eps = eps
        
    def selectAction( self, actions, values ):
        """Selects action using epsilon greedy strategy
        
        Args:
            actions: All available actions
            values: Corresponding values of the actions.
        """
        
        if ( ( random.random() < self.__eps ) and ( not self.competitionMode ) ):
            return random.choice( actions )
        else:
            return actions[values.index( max( values ) ) ]
    
    def initializeStateActions( self, state, possibleActions ):
        """Initializes unseen states (state, action) pairs with default values.
        
        Args:
            state: Unseen state.
            possibleActions: all actions, possible in the given state.         
        """
        values = [ self.initialStateActionValue ] * len(possibleActions)
        self.__q[ state ] = dict(zip(possibleActions, values) )
    
    def makeMove( self, state, possibleActions ):
        """Chooses a move, best in the given state using epsilon greedy strategy
        
        Args:
            state: State for which action is needed.
            possibleActions: All actions possible in the given state.
        """
        #check if state is in q already
        state = tuple(state)
        if state not in self.__q:
            #initialize q(s, a) for given state arbitrarily
            self.initializeStateActions( state, possibleActions )
            #now that the q(s, a) is initialized, proceed
        return self.selectAction( self.__q[ state ].keys(), self.__q[ state ].values() )
        
    def strategy( self ):
        pprint( self.__q )
        
    def update( self, stateUpdate ):
        """Updates state action pairs.
        
        Args:
            stateUpdate: dictionary containing state action pairs for two consecutive
                states experienced by agent. Also contains reward gained after making
                first action. Also contains flat, that indicates if the second state
                is a terminal state for the game.
        """
        if self.competitionMode:
            return
        if self.debug: 
            print( "Update received: ")
            pprint( stateUpdate )
        if not stateUpdate[ 't' ]: #if the stateUpdate is not terminal, then we care about s2,a2 reward.
            s2 = stateUpdate[ 's2' ]
            s1 = stateUpdate[ 's1' ]
            a1 = stateUpdate[ 'a1' ]
            a2 = stateUpdate[ 'a2' ]
            currVal = self.__q[ s1 ][ a1 ]
            if self.sarsa: #SARSA update
                currVal = currVal + self.learningRate * ( stateUpdate[ 'r' ] + self.__q[ s2 ][ a2 ] - currVal )
            else: #Q-learning update
                tmpVal = max( self.__q[ s2 ].values() )
                currVal = currVal + self.learningRate * ( stateUpdate[ 'r' ] + tmpVal - currVal )            
            self.__q[ s1 ][ a1 ] = currVal
        else:
            #in a terminal state we know the value for s2,a2 is zero. 
            #Therefore We only care about the transition reward.
            s1 = stateUpdate[ 's1' ]
            a1 = stateUpdate[ 'a1' ]
            currVal = self.__q[ s1 ][ a1 ] 
            currVal = currVal + 0.1 * ( stateUpdate[ 'r' ] - currVal )
            self.__q[ s1 ][ a1 ] = currVal



    
    
