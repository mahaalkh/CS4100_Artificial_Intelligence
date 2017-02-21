# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

   
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newScore = successorGameState.getScore()

        # "*** YOUR CODE HERE ***"

        if successorGameState.isWin(): 
          return float('inf')

        if successorGameState.isLose(): 
          return float('-inf')

        if successorGameState.getNumFood() == 0: 
          return float('inf')

        if newPos == currentGameState.getPacmanPosition(): 
          return float('-inf')


        A1, foodCost = min(getFoodCost(currentGameState, -1.5), getFoodCost(successorGameState, -1.5)) 

        A2, pelletCost = getPelletCost(currentGameState, -8.0)

        A3, ghostCost =  getGhostCost(currentGameState, -12.0, 10.0, 3)

        score = newScore * 100.0 + foodCost  + A1  + pelletCost + A2  + ghostCost + A3 

        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    ##### HELPERS BY MAHA ALKHAIRY #######
    def value(self, gameState, i): 
     
      if (gameState.isLose() or gameState.isWin()) or (i == self.depth * gameState.getNumAgents()): 
        return (self.evaluationFunction(gameState), None)
      if i % gameState.getNumAgents() == 0: 
        # pacman
        return self.maxValue(gameState, i)
      else:
        return self.minValue(gameState, i) 


    def minValue(self, gameState, i):
      """
      helps in getting the min value and the action to take to have the minValue for the successor agents
      :returns: (value, action)
      """

      legalActions = gameState.getLegalActions(i % gameState.getNumAgents())
      if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)

      v = (float('inf'), None)
      successors = map(lambda x: (gameState.generateSuccessor(i % gameState.getNumAgents(),x), x), legalActions)
      successorEvalFunc = map(lambda y: (self.value(y[0], i + 1)[0], y[1]), successors) 

      for h in successorEvalFunc: 
        if h[0] < v[0]: 
          v = h

      return v

    def maxValue(self, gameState, i): 
       """
       helps in getting the max value and the action to take to have the minValue for the successor agents
       :returns: (value, action)
       """ 
      
       agentIndex = 0

       legalActions = gameState.getLegalActions(agentIndex)
       if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)
       v = (float('-inf'), None)
       successors = map(lambda x: (gameState.generateSuccessor(agentIndex,x), x), legalActions)
       successorEvalFunc = map(lambda y: (self.value(y[0], i + 1)[0] , y[1]), successors) 
        
       for h in successorEvalFunc: 
         if h[0] > v[0]: 
           v = h

       return v
      ########################################################### ##### 



    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.value(gameState, 0)
        return bestAction


    

class AlphaBetaAgent(MultiAgentSearchAgent):

  ##### HELPERS BY MAHA ALKHAIRY #######
    def value(self, gameState, i, alpha, beta): 
     
      if (gameState.isLose() or gameState.isWin()) or (i == self.depth * gameState.getNumAgents()): 
        return (self.evaluationFunction(gameState), None)
      if i % gameState.getNumAgents() == 0: 
        # pacman
        return self.maxValue(gameState, i, alpha, beta)
      else:
        return self.minValue(gameState, i, alpha, beta) 


    def minValue(self, gameState, i, alpha, beta):
      """
      helps in getting the min value and the action to take to have the minValue for the successor agents
      :returns: (value, action)
      """

      legalActions = gameState.getLegalActions(i % gameState.getNumAgents())
      
      if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)

      v = (float('inf'), None)
      
      for move in legalActions: 
        nextGameState = gameState.generateSuccessor(i % gameState.getNumAgents(), move) 
        nextVal = self.value(nextGameState, i + 1, alpha, beta)
        if nextVal[0] < v[0]:
          v = (nextVal[0], move)
        if v[0] < alpha: 
          return v
        beta = min(beta, v[0])

      return v

    def maxValue(self, gameState, i, alpha, beta): 
       """
       helps in getting the max value and the action to take to have the minValue for the successor agents
       :returns: (value, action)
       """ 
      
       agentIndex = 0

       legalActions = gameState.getLegalActions(agentIndex)
       if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)
       v = (float('-inf'), None)
       for move in legalActions:
        nextGameState = gameState.generateSuccessor(agentIndex, move) 
        nextVal = self.value(nextGameState, i + 1, alpha, beta)
        if nextVal[0] > v[0]:
          v = (nextVal[0], move)
        if v[0] > beta: 
          return v
        alpha = max(alpha, v[0])

       return v
      ########################################################### ##### 



    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.value(gameState, 0, float('-inf'), float('inf'))
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    ##### HELPERS BY MAHA ALKHAIRY #######
    def value(self, gameState, i): 
     
      if (gameState.isLose() or gameState.isWin()) or (i == self.depth * gameState.getNumAgents()): 
        return (self.evaluationFunction(gameState), None)
      if i % gameState.getNumAgents() == 0: 
        # pacman
        return self.maxValue(gameState, i)
      else:
        return self.expectiValue(gameState, i) 


    def expectiValue(self, gameState, i):
      """
      helps in getting the min value and the action to take to have the minValue for the successor agents
      :returns: (value, action)
      """

      legalActions = gameState.getLegalActions(i % gameState.getNumAgents())
      if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)

      ## since uniform
      prob = 1.0 / float(len(legalActions))
      v = 0

      for move in legalActions: 
        nextGameState = gameState.generateSuccessor(i % gameState.getNumAgents(), move) 
        nextVal, nextAction = self.value(nextGameState, i + 1) 
        v1 = nextVal * prob
        v = v + nextVal

    
      return (v, None)

    
    def maxValue(self, gameState, i): 
       """
       helps in getting the max value and the action to take to have the minValue for the successor agents
       :returns: (value, action)
       """ 
      
       agentIndex = 0

       legalActions = gameState.getLegalActions(agentIndex)
       if len(legalActions) == 0: 
        return (self.evaluationFunction(gameState), None)
       v = (float('-inf'), None)
       successors = map(lambda x: (gameState.generateSuccessor(agentIndex,x), x), legalActions)
       successorEvalFunc = map(lambda y: (self.value(y[0], i + 1)[0] , y[1]), successors) 
        
       for h in successorEvalFunc: 
         if h[0] > v[0]: 
           v = h

       return v
      ########################################################### ##### 
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.value(gameState, 0)
        return bestAction

#---------------------- HELPERS BY MAHA ALKHAIRY -----------------------------
## the distance to the food (DF) 
## the distance to the pellet (DP)
## the distance to the ghost  
## the food cost 
## the pellet cost 
## the ghost cost 
## did you already win or lose? 
## are the ghosts scared? 

## A = 1 / DF
## A2 = 1 / DP

def getFoodCost(currentGameState, cost): 
  """
  returns the cost of the food 
  """
  #-----------------------------------
  curPos = currentGameState.getPacmanPosition()
  curFood = currentGameState.getFood()
  foodCount = currentGameState.getNumFood()
  distancesFood = map(lambda x: util.manhattanDistance(curPos, x), curFood.asList())
  #----------------------------------
  minFoodDistance = min(distancesFood)
  if minFoodDistance == 0: 
    minFoodDistance = 1.0
  A = 1.0 / minFoodDistance
  #-------------------------------
  ## since we want to have less food on the board the food would cost negatively
  foodCost = foodCount * cost

  return (A, foodCost)


def getPelletCost(currentGameState, cost): 
  """ 
  returns the cost teh pellet
  """
  #---------------------------------------
  curPos = currentGameState.getPacmanPosition()
  curGhostStates = currentGameState.getGhostStates()
  curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
  curPellets = currentGameState.getCapsules()
  distancesPellet = map(lambda x: util.manhattanDistance(curPos, x), curPellets)
  pelletCount = len(curPellets)
  #-------------------------------------
  minPelletDistance = 10 
  minPelletDistance = min(minPelletDistance, distancesPellet)
  if minPelletDistance == 0:
    minPelletDistance = 1.0
  A = 1.0 / minPelletDistance
  #------------------------------------ 
  if all(t > 0 for t in curScaredTimes): 
    pelletCost = pelletCount * cost 
  else: 
    pelletCost = -1.0 / (pelletCount + 1.0) 
  #-----------------------------------
  return (A, pelletCost)

def getGhostCost(currentGameState, cost1, cost2, minDistance): 
  """
  returns the cost of the ghost 
  """
  #--------------------------------
  curPos = currentGameState.getPacmanPosition()
  curGhostStates = currentGameState.getGhostStates()
  curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
  ghostCoordinates = map(lambda x: x.getPosition(), curGhostStates) 
  distancesGhost = map(lambda x: util.manhattanDistance(curPos, x), ghostCoordinates)
  # -----------------------------------
  minGhostDistance = min(distancesGhost)
  indexMinGhostDistance = distancesGhost.index(minGhostDistance)

  if minGhostDistance == 0 and curScaredTimes[indexMinGhostDistance] < 1: 
    return (float('-inf'), float('-inf'))

  if curScaredTimes[indexMinGhostDistance] > 1: 
    A = 1.0 / (indexMinGhostDistance + 1.0)
  else: 
    if minGhostDistance < minDistance: 
      A = (minGhostDistance ** 2) * cost1
    else: 
      A = -1.0 / minGhostDistance

  ghostCost = 0 
  costFunction = lambda d: (d ** 2) * cost2

  for i, distance in enumerate(distancesGhost): 
    if curScaredTimes[i] > 1:
      ghostCost = ghostCost + costFunction(distance)
    else: 
      ghostCost = ghostCost + (-1.0 / (distance + 1))


  ghostCost = sum(map(lambda d: (d ** 2) * cost2, distancesGhost))

  if all(t > 0 for t in curScaredTimes): 
    ghostCost = -1.0 * ghostCost


  return (A, ghostCost)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:  please see README.txt
    """
    "*** YOUR CODE HERE ***"


    if currentGameState.getNumFood() == 0: 
      return float('inf')

    if currentGameState.isWin(): 
      return float('inf')

    if currentGameState.isLose(): 
      return float('-inf')

    curScore = currentGameState.getScore()

    A1, foodCost = getFoodCost(currentGameState, -1.5)

    A2, pelletCost = getPelletCost(currentGameState, -9)

    A3, ghostCost =  getGhostCost(currentGameState, -12.0, 10.0, 3)

    score = curScore * 100.0 + A1 + foodCost + pelletCost  + A2 + ghostCost + A3 
    return score


# Abbreviation
better = betterEvaluationFunction

