from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time

BOARD_SIZE = 5

def main():
    game = goboard.GameState.new_game(BOARD_SIZE)
    bots = {
        gotypes.Player.black: agent.MCTSAgent(500, temperature=1.4),
        gotypes.Player.white: agent.MCTSAgent(500, temperature=1.4),
    }
    previous_move = None

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if previous_move:
            print(f"Last Player:{previous_move['player']}, Move:{previous_move['move']}")

        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)

        previous_move = {'player': 'Black' if game.next_player == gotypes.Player.black else 'White', 
                'move': print_move(game.next_player, bot_move)}

        game = game.apply_move(bot_move)

if __name__ == '__main__':
    main()