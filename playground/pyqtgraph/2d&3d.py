import PyQt4
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui, QtCore

# app = QtGui.QApplication([])
# w = QtGui.QWidget()
# layout = QtGui.QGridLayout()
# w.setLayout(layout)
# plot = pg.PlotWidget()
# view = gl.GLViewWidget()
# #view.setMinimumSize(384,360)
# xgrid = gl.GLGridItem()
# view.addItem(xgrid)
# layout.addWidget(plot, 0, 0)
# layout.addWidget(view, 2, 0)
# w.show()

app = QtGui.QApplication([])
view = gl.GLViewWidget()

view.set