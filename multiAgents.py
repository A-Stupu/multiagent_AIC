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

# change on peng

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.betterEvaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman_AIC.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman_AIC.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostsPos = [ghostState.getPosition() for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        
        capsules = successorGameState.getCapsules()
        score = successorGameState.getScore()

        for i in range(len(newGhostsPos)):
            ghostPos = newGhostsPos[i]
            scaredTime = newScaredTimes[i]
            
            ghostDist = manhattanDistance(newPos, ghostPos)

            if scaredTime > 0:
                if ghostDist > 0:
                    score += 15.0 / ghostDist 
            else:
                if ghostDist < 2:
                    score -= 500 
                else:
                    score -= 2.0 / ghostDist
        
        foodList = newFood.asList()
        
        if len(foodList) > 0:
            closestFoodDist = min([manhattanDistance(newPos, food) for food in foodList])
            
            score += 5.0 / (closestFoodDist + 1) # (+1 to avoid devided by 0)
        else:
            # win state
            score += 500

        capsules = successorGameState.getCapsules()
        if len(capsules) > 0:
            closestCapsuleDist = min([manhattanDistance(newPos, cap) for cap in capsules])
            score += 1.0 / (closestCapsuleDist + 1)
            
        if action == Directions.STOP:
            score -= 100

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
    Your minimax agent (question 5)
    """
   
   
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        
 

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 6)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 7)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        bestScore = -float('inf')
        bestActions = []  # actions list
        
        legalActions = gameState.getLegalActions(0)

        if Directions.STOP in legalActions: # remove STOP action
            legalActions.remove(Directions.STOP)

        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            
            score = self.getValue(successorState, 1, self.depth)
            
            if score > bestScore:
                bestScore = score
                bestActions = [action] 
            elif score == bestScore:
                bestActions.append(action) 
                
        return random.choice(bestActions)
                

    def getValue(self, gameState, agentIndex, depth):

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            return self.getMaxValue(gameState, depth) # Pacman is max
        else:
            return self.getExpectValue(gameState, agentIndex, depth) # Ghost is expectimax

    def getMaxValue(self, gameState, depth): # Pacman

        if depth == 0: # terminal test
            return self.evaluationFunction(gameState)
            
        v = -float('inf') # minus infinity
        
        legalActions = gameState.getLegalActions(0)
    
        if not legalActions: # no legal actions
            return self.evaluationFunction(gameState)
        
        for action in legalActions: 
            successorState = gameState.generateSuccessor(0, action)
            v = max(v, self.getValue(successorState, 1, depth))
            
        return v

    def getExpectValue(self, gameState, agentIndex, depth): # Ghosts
        
        v = 0.0 # expected value
        
        legalActions = gameState.getLegalActions(agentIndex)
        
        if not legalActions:
            return self.evaluationFunction(gameState)
            
        numAgents = gameState.getNumAgents() # bnumber of ghosts + pacman
        
        probability = 1.0 / len(legalActions) # randomly choose among legal actions

        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            
            if agentIndex == numAgents - 1:
                v += probability * self.getValue(successorState, 0, depth - 1)
            else:
                v += probability * self.getValue(successorState, agentIndex + 1, depth)
                
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 8).

    DESCRIPTION: 
    这个评估函数基于几个关键的启发式（heuristics）来给当前状态打分。
    1. 终止状态：如果当前是赢/输的状态，直接返回无穷大/无穷小，给算法最强烈的信号。
    2. 食物：计算到“最近食物”的距离（主要驱动力）和“剩余食物总数”（次要驱动力）。
    3. 鬼：
       - 危险的鬼：如果离得太近（距离<2），视为“立即死亡”，返回无穷小。
       - 害怕的鬼：如果存在，计算到“最近的害怕的鬼”的距离，作为“奖励目标”。
    4. 胶囊：计算“剩余胶囊总数”，作为次要惩罚。
    
    最终分数 = 基础分 - 食物距离成本 - 害怕的鬼距离成本 - 剩余工作量成本
    （注意：我们通过“最小化成本”来“最大化分数”）
    """
    "*** YOUR CODE HERE ***"
    # 提取关键状态信息
    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    
    # 1. 终止状态检查 (最优先)
    # ---------------------------------
    
    # 1a. 胜利状态：没有食物了
    if not foodList:
        return float('inf') # 胜利！这是最好的状态。

    # 1b. 立即失败状态：撞上危险的鬼
    for ghost in ghostStates:
        dist = manhattanDistance(pos, ghost.getPosition())
        if ghost.scaredTimer == 0 and dist < 2:
            # 如果鬼不害怕，且距离小于2（即下一步就可能被吃）
            # 这是一个“死局”，立即给予最低分
            return -float('inf') 

    # 2. 启发式成本计算 (Heuristics)
    # ---------------------------------
    # 我们把问题变成“最小化成本”，而不是“最大化奖励”。
    # 基础分是游戏自带的，我们在此之上增加或减少。
    
    score = currentGameState.getScore()

    # --- 启发式 1: 驱动力 (食物) ---
    # Pac-Man 的主要工作是吃豆
    
    # W_FOOD_DIST (权重): 1.5
    # Pac-Man 应该始终被“拉”向最近的食物。
    # 这是一个线性的“成本”，距离越远，分数越低。
    closestFoodDist = min([manhattanDistance(pos, food) for food in foodList])
    score -= closestFoodDist * 1.5

    # --- 启发式 2: 机会 (害怕的鬼) ---
    # 害怕的鬼是“高分食物”。
    
    # W_SCARED_GHOST (权重): 2.0
    scaredGhosts = [g for g in ghostStates if g.scaredTimer > 1]
    if scaredGhosts:
        closestScaredGhostDist = min([manhattanDistance(pos, g.getPosition()) for g in scaredGhosts])
        # 我们也想靠近它，所以也把它当作“成本”来减
        # 它的权重 (2.0) 应该高于食物 (1.5)，意味着鬼更“诱人”
        score -= closestScaredGhostDist * 2.0

   # --- 启发式 3: 驱动力 (胶囊) ---
    if capsules: # 只有在还有胶囊时才计算
        closestCapsuleDist = min([manhattanDistance(pos, cap) for cap in capsules])
        # 我们给胶囊一个“拉力”，但权重 (1.0) 设的比食物 (1.5) 低
        # 这样 Pac-Man 不会为了一个远处的胶囊而放弃近处的食物
        score -= closestCapsuleDist * 1.0 
    
    # --- 启发式 4: 剩余工作量 (食物和胶囊) ---
    # 每一个剩余的豆子都是一个“工作量”，给予一个固定的成本。
    score -= len(foodList) * 20

    # W_CAPSULE_COUNT = 20
    # 胶囊同理，吃掉一个胶囊 = 获得 +20 的收益
    # 20 -> 150 摆动问题
    score -= len(capsules) * 150

    # 返回最终的评估分数
    return score

# Abbreviation
better = betterEvaluationFunction
