import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtGui, QtCore
import mne
from multiprocessing import Process

from nfb.pynfb.windows import SourceSpaceWindow
from nfb.pynfb.brain import (SourceSpaceRecontructor, SourceSpaceWidgetPainterSettings)
from nfb.pynfb.io.xml_ import xml_file_to_params
from nfb.pynfb.generators import run_eeg_sim
from nfb.pynfb.inlets.lsl_inlet import LSLInlet

protocol = SourceSpaceRecontructor(signals=None)
window = SourceSpaceWindow(parent=None, current_protocol=protocol)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

settings = window.settings
settings_widget = window.settings_widget
sourcespace_widget = window.figure

window.show()

# Start stream from file
params = xml_file_to_params('nfb/pynfb/sourcespace.xml')
file_path = params['sRawDataFilePath']
stream_name = params['sStreamName']
reference = params['sReference']
raw = mne.io.read_raw_fif(file_path, verbose='ERROR')
labels = raw.info['ch_names']
fs = raw.info['sfreq']
start, stop = raw.time_as_index([0, 60])  # read the first 15s of data
source_buffer = raw.get_data(start=start, stop=stop)
thread = Process(target=run_eeg_sim, args=(), kwargs={'chunk_size': 0, 'source_buffer': source_buffer,
                                                      'name': stream_name, 'labels': labels, 'freq': fs})
thread.start()

# Start updating the brain
stream = LSLInlet(name=stream_name)
def update():
    chunk = stream.get_next_chunk()
    if chunk is not None:
        protocol.widget_painter.redraw_state(chunk)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000. / fs)