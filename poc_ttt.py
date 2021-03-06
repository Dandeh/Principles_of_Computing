"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10  # Number of trials to run
#MCMATCH = 1.0  # Score for squares played by the machine player
SCORE_CURRENT = 1.0  # Score for squares played by the machine player  # new constant name in 2015 version
#MCOTHER = 1.0  # Score for squares played by the other player
SCORE_OTHER = 1.0  # Score for squares played by the other player  # new constant name in 2015 version


def sort_dict_by_value(dictionary):
    """
    a helper function, takes in a dictionary, compare all its values and sort from max to min
    :param dictionary:
    :return: tuple (key, value)
    """
    temp = []
    for key, value in dictionary.items():
        temp.append((value, key))

    return sorted(temp, reverse=True)


def mc_trial(board, player):
    """
    Takes a current board and the next player to move. The function should play a game starting with the given player
    by making random moves, alternating between players. The function should return when the game is over. The modified
    board will contain the state of the game, so the function does not return anything.
    """
    next_player = player
    while board.check_win() is None:
        # while game is in progress
        # get next player and next move
        next_move = pick_next_move_random(board)
        board.move(next_move[0], next_move[1], next_player)
        next_player = provided.switch_player(next_player)  # switch player and repeat


def update_scores_win(board, scores, player):
    """
    update scores when player wins
    :param board:
    :param scores:
    :param player:
    :return: void
    """
    for row_index in range(board.get_dim()):
        for col_index in range(board.get_dim()):
            if board.square(row_index, col_index) == player:  # this square gets MCMATCH
                scores[row_index][col_index] += SCORE_CURRENT
            elif board.square(row_index, col_index) == provided.EMPTY:  # gets 0
                scores[row_index][col_index] += 0
            else:
                scores[row_index][col_index] -= SCORE_OTHER


def update_scores_lose(board, scores, player):
    """
    update scores when player lose
    :param board:
    :param scores:
    :param player:
    :return: void
    """
    for row_index in range(board.get_dim()):
        for col_index in range(board.get_dim()):
            if board.square(row_index, col_index) == player:  # this square gets -MCMATCH
                scores[row_index][col_index] -= SCORE_CURRENT
            elif board.square(row_index, col_index) == provided.EMPTY:  # gets 0
                scores[row_index][col_index] += 0
            else:
                scores[row_index][col_index] += SCORE_OTHER


def mc_update_scores(scores, board, player):
    """
    Takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board, a board from a completed
    game, and which player the machine player is. The function should score the completed board and update the scores
    grid. As the function updates the scores grid directly, it does not return anything,
    :param: scores: a list of scores
    :param: board
    :param: player: current player
    """
    result = board.check_win()
    # machine player is "player"
    if result is None:  # still in progress, do nothing
        return
    elif result == provided.DRAW:  # tie, do nothing
        return

    if result == player:  # machine player wins
        # update scores
        update_scores_win(board, scores, player)
    else:  # machine player loses
        # update scores
        update_scores_lose(board, scores, player)


def get_best_move(board, scores):
    """
    Takes a current board and a grid of scores. The function should find all of the empty squares with the maximum
    score and randomly return one of them as a (row, column) tuple. It is an error to call this function with a board
    that has no empty squares (there is no possible next move), so your function may do whatever it wants in that
    case. The case where the board is full will not be tested.
    :param: board: a board instance
    :param: scores: a list
    """
    available_moves = board.get_empty_squares()
    if len(available_moves) == 0:  # no available moves
        return

    temp_dict = {}
    for each_move in available_moves:
        # form a temp dictionary of available squares
        temp_dict[each_move] = temp_dict.get(each_move, scores[each_move[0]][each_move[1]])

    # get a list of moves
    move_list = sort_dict_by_value(temp_dict)

    # need to deal w/ equals
    best_move_score = move_list[0][0]

    while True:
        ran_index = random.randrange(0, len(move_list))
        if move_list[ran_index][0] == best_move_score:
            best_move = move_list[ran_index][1]
            return best_move


def mc_move(board, player, trials):
    """
    Takes a current board, which player the machine player is, and the number of trials to run. The function should
    use the Monte Carlo simulation described above to return a move for the machine player in the form of a (row,
    column) tuple. Be sure to use the other functions you have written!
    """
    number_of_trials = trials
    scores = [[[] for row_index in range(board.get_dim())] for col_index in range(board.get_dim())]

    # initialize scores dictionary
    for row_index in range(board.get_dim()):
        for col_index in range(board.get_dim()):
            scores[row_index][col_index] = 0

    while number_of_trials > 0:
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
        number_of_trials -= 1

    next_move = get_best_move(board, scores)

    return next_move


def pick_next_move_random(board):
    """
    randomly pick next move for "player" on current board "board"
    :return: a (row, col) tuple
    """
    # get current available squares
    available_moves = board.get_empty_squares()  # this is a list of (row, col) tuples

    # randomly pick one move from all the available ones
    rand_index = random.randrange(0, len(available_moves))
    next_move = available_moves[rand_index]

    return next_move

    # Test game with the console or the GUI.
    # Uncomment whichever you prefer.
    # Both should be commented out when you submit for
    # testing to save time.

    # provided.play_game(mc_move, NTRIALS, False)
    # poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

    # print get_best_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY,
    # provided.EMPTY]]),
    # [[0, 0], [3, 0]])
    # expected one tuple from [(1, 0)]

    # print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
    # [provided.PLAYERO, provided.PLAYERX, provided.PLAYERX],
    # [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]),
    # provided.PLAYERX, NTRIALS)
    #
    # print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
    # [provided.EMPTY, provided.PLAYERX, provided.PLAYERX],
    # [provided.PLAYERO, provided.EMPTY, provided.PLAYERO]]),
    #               provided.PLAYERO, NTRIALS)
    #
    # sc = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # mc_update_scores(sc, provided.TTTBoard(3, False, [[provided.PLAYERX,
    #                                                    provided.PLAYERX,
    #                                                    provided.PLAYERO],
    #                                                   [provided.PLAYERO,
    #                                                    provided.PLAYERX,
    #                                                    provided.EMPTY],
    #                                                   [provided.EMPTY,
    #                                                    provided.PLAYERX,
    #                                                    provided.PLAYERO]]), 2)
    # print sc
    # expected [[1.0, 1.0, -1.0], [-1.0, 1.0, 0], [0, 1.0, -1.0]] but
    # received [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


# print mc_move(provided.TTTBoard(3, False, [[provided.PLAYERX, provided.EMPTY, provided.EMPTY],
# [provided.PLAYERO, provided.PLAYERO, provided.EMPTY],
# [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]),
#               provided.PLAYERX, NTRIALS)

# print mc_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.PLAYERX, provided.PLAYERX],
#                                            [provided.PLAYERO, provided.EMPTY, provided.PLAYERX],
#                                            [provided.PLAYERO, provided.PLAYERX, provided.EMPTY]]),
#               provided.PLAYERO,
#               NTRIALS)
