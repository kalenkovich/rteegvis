import sympy # sympy has to be imported before pyqtgraph on my setup
from pyqtgraph import QtCore, QtGui

from nfb.pynfb.windows import SourceSpaceWindow
from nfb.pynfb.brain import SourceSpaceReconstructor
from nfb.pynfb.io.xml_ import xml_file_to_params
from nfb.pynfb.generators import stream_file_in_a_thread
from nfb.pynfb.inlets.lsl_inlet import LSLInlet

protocol = SourceSpaceReconstructor(signals=None)
mesh_data = protocol.mesh_data

vertexes = mesh_data.vertexes()
faces = mesh_data.faces()
