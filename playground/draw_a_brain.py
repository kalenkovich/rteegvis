import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtCore, QtGui

from nfb.pynfb.brain import SourceSpaceWidget, SourceSpaceWidgetPainter, SourceSpaceRecontructor

app = QtGui.QApplication([])

widget = SourceSpaceWidget()
reconstructor = SourceSpaceRecontructor(signals=None)
painter = SourceSpaceWidgetPainter(reconstructor)
painter.prepare_widget(widget)


widget.show()



from mne.datasets import sample
data_path = sample.data_path()