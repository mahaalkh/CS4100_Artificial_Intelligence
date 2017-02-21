# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

directions = {
    "South": Directions.SOUTH,
    "West" : Directions.WEST,
    "North": Directions.NORTH,
    "East" : Directions.EAST
}



class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

"""------------ HELPERS FOR THE SEARCH (By Maha Alkhairy) --------------""" 

def expandThisNode(nodeInfo, isUCS): 
    """
    explores this node and appends the direction to the 
    :param nodeInfo: Species
    :param isUCS: indicates whether the search is ucs
    :return: None 
    """
    problem, thisNode, frontier, exploredSet, result = nodeInfo
    nextStates = problem.getSuccessors(thisNode)
    
    # add states to the frontier
    for  nextNode, nextDirection, nextCost in nextStates: 
        ## don't wanna change the result itself 
        newResult = list(result) 
        newResult.append(nextDirection)
        ## the newResult is the actions to get to the nextNode
        item = (nextNode, newResult, nextCost)
        if isUCS: 
            frontier.push(item, problem.getCostOfActions(newResult))
        else: 
            frontier.push(item)

    # add this node to the explored list
    if thisNode not in exploredSet: 
        exploredSet.append(thisNode)

def helperSearch(frontier, exploredSet, problem, isUCS): 
    """ 
    This function is a helper for depth first search and breadth first search
    it performs the node expansion and places the states
    in the correct order on the frontier

    frontier: Stack or Queue or PriorityQueueWITHFunction 
    exploredSet: set of explored nodes 
    problem: The problem 
    isUCS: Boolean, if we are using a priority queue this value is true

    return: [Action, ...] ; 
     where Action is one of: 
     Directions.NORTH, Directions.SOUTH, Directions.EAST and Directions.WEST
    """  

    thisState = frontier.pop()
    thisNode, result, _ = thisState

    ## check if node has been explored 
    if thisNode in exploredSet: 
        return "continue"

    # did we reach the goal state? 
    if problem.isGoalState(thisNode): 
        return result
        
    # expand the node 
    nodeInfo = problem, thisNode, frontier, exploredSet, result
    expandThisNode(nodeInfo, isUCS)

def helperLoop(frontier, problem, isUCS):
    """ 
    implements helperSearch in a while loop 

    :frontier: type depends on search so it is either a 
                Stack, Queue, PriorityQueue, or a PriorityQueueWithFunction
    :problem: ---
    :isUCS: indicates when the search is ucs
    """  
    exploredSet = []
    path = []
    
    if isUCS: 
        frontier.push((problem.getStartState(), [], 0), 0)
    else: 
        frontier.push((problem.getStartState(), [], 0))

    while not frontier.isEmpty():  
        path = helperSearch(frontier, exploredSet, problem, isUCS)
        if path == "continue" or not (isinstance(path, list)): 
            continue
        else: 
            break

    return path

""" ----------------------END OF HELPERS---------------------- """


def depthFirstSearch(problem):
    """ Search the deepest nodes in the search tree first. """
    ## frontier is a stack
    "*** YOUR CODE HERE ***"
    frontier =  util.Stack()
    return helperLoop(frontier, problem, False)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    ## frontier is a QUEUE
    "*** YOUR CODE HERE ***"
    frontier =  util.Queue()
    return helperLoop(frontier, problem, False)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    ## frontier is a PRIORITY QUEUE
    "*** YOUR CODE HERE ***"
    frontier =  util.PriorityQueue()
    return helperLoop(frontier, problem, True)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    ## frontier is a PRIORITY QUEUE WITH FUNCTION
    "*** YOUR CODE HERE ***"
    ## function is g(n) + h(n) ; where g(n) is the cost of the actions 
    ## and h(n) is the heuristic
    function = lambda x: problem.getCostOfActions(x[1]) + heuristic(x[0], problem)
    frontier =  util.PriorityQueueWithFunction(function)
    return helperLoop(frontier, problem, False)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
