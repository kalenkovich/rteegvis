import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtCore, QtGui

from nfb.pynfb.windows import SourceSpaceWindow
from nfb.pynfb.brain import SourceSpaceRecontructor
from nfb.pynfb.io.xml_ import xml_file_to_params
from nfb.pynfb.generators import stream_file_in_a_thread
from nfb.pynfb.inlets.lsl_inlet import LSLInlet

protocol = SourceSpaceRecontructor(signals=None)
window = SourceSpaceWindow(parent=None, current_protocol=protocol)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.showMinimized()


settings = window.settings
settings_widget = window.settings_widget
sourcespace_widget = window.figure


# Read params from the settings file
params = xml_file_to_params('nfb/pynfb/sourcespace.xml')
file_path = params['sRawDataFilePath']
stream_name = params['sStreamName']
reference = params['sReference']

# Start updating the brain
stream = LSLInlet(name=stream_name)
freq = stream.get_frequency()


def update():
    chunk = stream.get_next_chunk()
    if chunk is not None:
        protocol.widget_painter.redraw_state(chunk)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000. / freq)


