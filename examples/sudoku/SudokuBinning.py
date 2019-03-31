import random as r

import examples.sudoku.BoardGen as BoardGen


def hash_based_binning(inds, board_size, num_of_bins):
    inds_unconstrained = [[ind.phenome[i][j]
                           for i in range(board_size)
                           for j in range(board_size) if ind.constraints is None or ind.constraints[i][j] == 0]
                          for ind in inds]
    random_noise = [[r.randint(0, 999), r.randint(0, 999)] for _ in inds_unconstrained[0]]
    inds_hashed = [[hash(str(ind[i] * random_noise[i][0] + random_noise[i][1])) % 1000
                    for i in range(len(ind))]
                   for ind in inds_unconstrained]

    inds_summed_and_modded = [sum([abs(ind[i])
                                   for i in range(len(ind))]) % num_of_bins
                              for ind in inds_hashed]

    binned_inds = [[] for _ in range(num_of_bins)]

    for idx, ind in enumerate(inds):
        binned_inds[inds_summed_and_modded[idx]].append(ind)

    return binned_inds
