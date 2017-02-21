# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(iterations): 
          self.values = self.valueIteration(iterations)

    ####### HELPERS BY MAHA ALKHAIRY #########
    def calculateValue(self, state, action, prob, nextState):
      """
      calculate the value inside the sum
      """
      reward = self.mdp.getReward(state, action, nextState)
      value = self.getValue(nextState)
      val = (prob * (reward + (self.discount * value)))
      return val

    def valueIteration(self, iterations):
      """
      computes the updated values
      """
      states = self.mdp.getStates()
      stateValue = util.Counter()
      for state in states: 
        actions = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state): 
          stateValue[state] = 0 
        else:
          maxVal = float("-inf")
          for action in actions: 
            statesTrans =  self.mdp.getTransitionStatesAndProbs(state, action)
            val = 0
            for nextState, prob in statesTrans: 
              val = val + self.calculateValue(state, action, prob, nextState)
            maxVal = max(maxVal, val)
            stateValue[state] = maxVal
      return stateValue 

    ##########################################

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        ## in the form [(state, transition value), ... ]
        statesTrans =  self.mdp.getTransitionStatesAndProbs(state, action)

        ## the discount 
        dis = self.discount

        ## 
        qVal = 0
        ## compute the vals from the 
        for nextState, prob in statesTrans: 
          qVal = qVal + self.calculateValue(state, action, prob, nextState)
        return qVal
       

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state): 
          return None
        else: 
          ## choose action that maximizes the qValue 
          actions = self.mdp.getPossibleActions(state)
          val = float('-inf')
          actn = actions[0]
          for action in actions: 
            Qval = self.getQValue(state, action)
            if Qval > val: 
              val = Qval 
              actn = action
          return actn

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
