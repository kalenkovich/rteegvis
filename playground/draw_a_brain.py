import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtCore, QtGui
from mne.source_estimate import read_source_estimate
import numpy as np
from scipy import sparse
from scipy.sparse import coo_matrix
from mne.viz.utils import mne_analyze_colormap
from pyqtgraph import opengl as gl
from matplotlib import colors as mpl_colors
from matplotlib import cm
from pyqtgraph.opengl.GLGraphicsItem import GLOptions
from OpenGL.GL import (GL_ONE, GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA, GL_FUNC_ADD, GL_MAX, GL_BLEND,
                       GL_ALPHA_TEST, GL_DEPTH_TEST,
                       GL_CULL_FACE, GL_FRONT, GL_FRONT_FACE, GL_BACK)


from nfb.pynfb.brain import SourceSpaceWidget, SourceSpaceWidgetPainter, SourceSpaceRecontructor

app = QtGui.QApplication([])

widget = SourceSpaceWidget()
reconstructor = SourceSpaceRecontructor(signals=None)
painter = SourceSpaceWidgetPainter(reconstructor)
painter.prepare_widget(widget)
widget.show()


def read_smoothing_matrix():
    lh_npz = np.load('playground/vs_pysurfer/smooth_mat_lh.npz')
    rh_npz = np.load('playground/vs_pysurfer/smooth_mat_rh.npz')

    smooth_mat_lh = sparse.coo_matrix((
        lh_npz['data'], (lh_npz['row'], lh_npz['col'])),
        shape=lh_npz['shape'] + rh_npz['shape'])

    lh_row_cnt, lh_col_cnt = lh_npz['shape']
    smooth_mat_rh = sparse.coo_matrix((
        rh_npz['data'], (rh_npz['row'] + lh_row_cnt, rh_npz['col'] + lh_col_cnt)),
        shape=rh_npz['shape'] + lh_npz['shape'])

    return smooth_mat_lh.tocsc() + smooth_mat_rh.tocsc()
smoothing_matrix = read_smoothing_matrix()


def threshold_a_colormap(colormap, lower_threshold, upper_threshold):
    sample_points = np.linspace(0.0, 1.0, 256)
    color_list = colormap(sample_points)
    invisible_idx = np.logical_and(
        lower_threshold <= sample_points,
        sample_points <= upper_threshold)
    color_list[invisible_idx, -1] = 0 # The last number is opacity
    name = '{}_thresholded'.format(colormap.name)
    return mpl_colors.LinearSegmentedColormap.from_list(name=name, colors=color_list)

data = read_source_estimate('playground/vs_pysurfer/psi_stc-lh.stc').data[:, 0]

threshold = 90
pcts = [(100 - threshold)/2, (100 + threshold)/2]
pctls = np.percentile(data, pcts)



self = painter

painter.colormap_mode = 'local'
data_smoothed = smoothing_matrix.dot(data)

painter.vmin, painter.vmax = np.min(data), np.max(data)
sources_normalized = painter.normalize_to_01(data_smoothed)
invisible_idx = np.where((data_smoothed >= pctls[0]) & (data_smoothed <= pctls[1]))
colors = cm.seismic(sources_normalized)
colors[invisible_idx] = self.background_colors[invisible_idx]

self.cortex_mesh_data.setVertexColors(colors)
self.cortex_mesh_item.meshDataChanged()


self.cortex_mesh_data.set


self.data_mesh_data = self.read_mesh()
self.data_mesh_data.setVertexColors(colors)
self.data_mesh_item = gl.GLMeshItem(meshdata=self.data_mesh_data, shader='shaded')


if self.data_mesh_item in widget.items:
    widget.removeItem(self.data_mesh_item)

gloptions = {
    GL_BLEND: True,
    GL_CULL_FACE: True,
    'glBlendFuncSeparate': (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE),
    'glBlendEquationSeparate': (GL_FUNC_ADD, GL_MAX)
    }

# gloptions['glBlendFuncSeparate'] = (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE)
# gloptions['glBlendEquationSeparate'] = (GL_FUNC_ADD, GL_MAX)

self.data_mesh_item.setGLOptions(gloptions)
# self.data_mesh_item.setGLOptions('additive')
widget.addItem(self.data_mesh_item)


