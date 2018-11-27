import scipy.sparse
import numpy as np
sparse_matrix = scipy.sparse.csc_matrix([[0, 0, 3],[4, 0, 0]])
print (sparse_matrix)


sparse_matrix.todense()
scipy.sparse.save_npz('sparse_matrix.npz', sparse_matrix)
sparse_matrix = scipy.sparse.load_npz('sparse_matrix.npz')

sparse_matrix = sparse_matrix.todense()
print (sparse_matrix[0])
