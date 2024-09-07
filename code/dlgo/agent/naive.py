import random
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move, GameState
from dlgo.gotypes import Point

class RandomBot(Agent):
    def select_move(self, game_state: GameState):
        '''
        Chooses a random valid move that preserves its own eyes.
        1. Check all points on the board --> see if the move is valid, and is not an eye
        2. Randomly select a move from all candidates. If there is none, pass.
        '''
        candidates = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and not is_point_an_eye(game_state.board, candidate, game_state.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))