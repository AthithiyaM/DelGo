import math
import random

from dlgo import agent
from dlgo.gotypes import Player
from dlgo.utils import coords_from_point
from dlgo.goboard import GameState, Move

__all__ = [
    'MCTSAgent',
]

class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.legal_moves()

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node
    
    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def is_terminal(self):
        return self.game_state.is_over()

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)


class MCTSAgent(agent.Agent):
    def __init__(self, num_rounds, temperature):
        agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature
    
    def select_move(self, game_state):
        '''
        1. Start at the current Game State
        2. So long as the node has viable gameplay & isn't a game end, 
            select a random child and simulate the game till the end
        3. Record the game score and add the score to all preceeding 
            nodes in that game
        4. After performing x amount of rounds, select the best move
            by selecting the child with the highest winning percentage
        '''
        root = MCTSNode(game_state)

        for count in range(self.num_rounds):
            node = root
            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)
            
            if node.can_add_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)

            while node is not None:
                node.record_win(winner)
                node = node.parent
        
        best_move = None
        best_percentage = -1.0
        for child in root.children:
            child_pct = child.winning_frac(game_state.next_player)
            if child_pct > best_percentage:
                best_percentage = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node):
        '''
        1. Loop through the children of a node
        2. Calculate the UCT score of the child (see mcts_info for details)
        3. Return the child with the best score 
        '''

        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None

        for child in node.children:
            win_percentage = child.winning_frac(node.game_state.next_player)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.black: agent.RandomBot(),
            Player.white: agent.RandomBot(),
        }
        while not game.is_over():
            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
        return game.winner()