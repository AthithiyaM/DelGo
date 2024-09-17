# This script can be used to feed a board into the trained model and print out its predictions

import numpy as np
from CNN import loading_and_preprocessing # This can be changed to any of the NNs

test_board = np.array([[
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
    [0, 1, -1,  1, -1, 0, 0, 0, 0,],
    [0, 1, -1,  1, -1, 0, 0, 0, 0,],
    [0, 0,  1, -1,  0, 0, 0, 0, 0,],
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
    [0, 0,  0,  0,  0, 0, 0, 0, 0,],
]])

move_prob = loading_and_preprocessing.model.predict(test_board)[0]
i = 0
for row in range(9):
    row_formatted = []
    for col in range(9):
        row_formatted.append('{:.3f}'.format(move_prob[i]))
        i += 1
    print(' '.join(row_formatted))