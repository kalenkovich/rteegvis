import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtCore, QtGui

from nfb.pynfb.windows import SourceSpaceWindow
from nfb.pynfb.brain import SourceSpaceReconstructor
from nfb.pynfb.io.xml_ import xml_file_to_params
from nfb.pynfb.generators import stream_file_in_a_thread
from nfb.pynfb.inlets.lsl_inlet import LSLInlet

app = QtGui.QApplication([])

# Read params from the settings file
params = xml_file_to_params('nfb/pynfb/sourcespace.xml')
file_path = params['sRawDataFilePath']
stream_name = params['sStreamName']
reference = params['sReference']

# Connect to the stream
stream = LSLInlet(name=stream_name)
fs = stream.get_frequency()

protocol = SourceSpaceReconstructor(stream)
window = SourceSpaceWindow(parent=None, current_protocol=protocol)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.show()


settings = window.settings
settings_widget = window.settings_widget
sourcespace_widget = window.figure
sourcespace_painter = protocol.widget_painter





def update():
    chunk = stream.get_next_chunk()
    if chunk is not None:
        protocol.update_state(chunk)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    print('creating timer')
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000. / fs)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(QtGui.QApplication.instance().exec_())