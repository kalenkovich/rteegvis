


import timeit
import numpy as np


setup = """
import numpy as np
import pyqtgraph.opengl as gl
from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator
data_path = sample.data_path()
filename_inv = data_path + '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'
inverse_operator = read_inverse_operator(filename_inv)

left_hemi, right_hemi = inverse_operator['src']

vertexes = np.r_[left_hemi['rr'], right_hemi['rr']]
lh_vertex_cnt = left_hemi['rr'].shape[0]
faces = np.r_[left_hemi['use_tris'], lh_vertex_cnt + right_hemi['use_tris']]
vertex_idx = np.r_[left_hemi['vertno'], lh_vertex_cnt + right_hemi['vertno']]

cortex_mesh_data = gl.MeshData(vertexes=vertexes, faces=faces)
cortex_mesh_data.setVertexColors(np.random.random(vertexes.shape[0]))


"""

stmt1 = """
colors = np.ones(cortex_mesh_data.vertexes().shape[0])
colors[vertex_idx] = np.random.random(vertex_idx.shape)
cortex_mesh_data.setVertexColors(colors)
"""
stmt2 = """
colors = np.random.random(vertex_idx.shape)
cortex_mesh_data._vertexColors[vertex_idx] = colors
"""

time1 = timeit.Timer(setup=setup, stmt=stmt1)
time2 = timeit.Timer(setup=setup, stmt=stmt2)

if __name__ == '__main__':
    print("with temp array :", time1.timeit(number=1000))
    print("without temp array:", time2.timeit(number=1000))