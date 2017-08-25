import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from mne.datasets import sample
from mne.minimum_norm import read_inverse_operator
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import ptime
import matplotlib as mpl
from matplotlib import cm
from matplotlib import colors as mcolors


data_path = sample.data_path()
filename_inv = data_path + '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'
inverse_operator = read_inverse_operator(filename_inv)


left_hemi, right_hemi = inverse_operator['src']
vertexes = np.r_[left_hemi['rr'], right_hemi['rr']]
lh_vertex_cnt = left_hemi['rr'].shape[0]
faces = np.r_[left_hemi['use_tris'], lh_vertex_cnt + right_hemi['use_tris']]
submesh_verrtex_idx = np.unique(faces)
vertex_idx = np.r_[left_hemi['vertno'], lh_vertex_cnt + right_hemi['vertno']]
vertex_cnt = vertex_idx.shape[0]

cortex_mesh_data = gl.MeshData(vertexes=vertexes, faces=faces)
cortex_mesh_data.setVertexColors(np.ones((vertexes.shape[0], 4)))


app = QtGui.QApplication([])
widget = gl.GLViewWidget()
widget.show()
widget.setWindowTitle('My first pyqtgraph brain mesh')
# The largest brain dimension
max_dim = max(np.ptp(vertexes, axis=0))
widget.setCameraPosition(distance=2 * max_dim)


grid = gl.GLGridItem()
grid.scale(2, 2, 1)
widget.addItem(grid)


# m1 = gl.GLMeshItem(vertexes=vertices, faces=faces,
#                    drawFaces=False, color=pg.mkColor('k'),
#                    drawEdges=True, edgeColor=pg.mkColor('g'),
#                    #faceColors=colors,
#                    smooth=False)
mesh = gl.GLMeshItem(meshdata=cortex_mesh_data)
# m1.translate(5, 5, 0)
# m1.setGLOptions('additive')
widget.addItem(mesh)

# stc is from the plot_compute_mne_inverse_raw_in_label.py example
sources = stc.data.squeeze()
cmapper = cm.ScalarMappable(cmap='viridis')
cmap = mcolors.Colormap(name='viridis')
cmap.to_
colors = cmapper.to_rgba(sources)

lastTime = ptime.time()
fps = None
def update():
    # Update colors
    colors = np.concatenate((np.random.random((vertex_cnt, 3)),
                             np.ones((vertex_cnt, 1))), axis=1)
    cortex_mesh_data._vertexColors[vertex_idx] = colors
    cortex_mesh_data._vertexColorsIndexedByFaces = None
    # colors = np.concatenate((np.random.random((vertexes.shape[0], 3)),
    #                          np.ones((vertexes.shape[0], 1))), axis=1)
    # cortex_mesh_data.setVertexColors(colors)
    #
    mesh.meshDataChanged()

    # Update fps
    global lastTime, fps
    now = ptime.time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0 / dt
    else:
        s = np.clip(dt * 3., 0, 1)
        fps = fps * (1 - s) + (1.0 / dt) * s
    widget.setWindowTitle('%0.2f fps' % fps)



t = QtCore.QTimer()
t.timeout.connect(update)
t.start(10)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        # app.exec()

