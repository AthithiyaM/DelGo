from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords

BOARD_SIZE = 5
HUMAN_PLAYS_BLACK = False

def main():
    game = goboard.GameState.new_game(BOARD_SIZE)
    bot = agent.MCTSAgent(500, temperature=1.4)
    human_player_type = gotypes.Player.black if HUMAN_PLAYS_BLACK else gotypes.Player.white
    previous_move = None

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board(game.board)

        if previous_move:
            print(f"Last Player:{previous_move['player']}, Move:{previous_move['move']}")

        if game.next_player == human_player_type:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        
        # Storing previous move to print on screen
        previous_move = {'player': 'Black' if game.next_player == gotypes.Player.black else 'White', 
                        'move': print_move(game.next_player, move)}
        
        game = game.apply_move(move)

if __name__ == '__main__':
    main()