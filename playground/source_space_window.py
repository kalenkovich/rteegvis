import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtGui, QtCore

from nfb.pynfb.windows import SourceSpaceWindow
from nfb.pynfb.brain import (SourceSpaceRecontructor, SourceSpaceWidgetPainterSettings)

protocol = SourceSpaceRecontructor(signals=None)
window = SourceSpaceWindow(parent=None, current_protocol=protocol)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

settings = window.settings
settings_widget = window.settings_widget

sourcespace_widget = window.figure

layout = window.centralWidget().layout()
layout.addWidget(settings_widget)

window.show()