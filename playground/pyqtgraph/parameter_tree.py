import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph import opengl as gl
app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph.parametertree.parameterTypes import ListParameter

params = [
    {'name': 'Visualization', 'type': 'group', 'children': [
        {'name': 'Integer', 'type': 'int', 'value': 10},
        {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
        {'name': 'String', 'type': 'str', 'value': "hi"},
        {'name': 'List', 'type': 'list', 'values': [1, 2, 3], 'value': 2},
        {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3, 3, 3]}, 'value': 2},
        {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
        {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
        {'name': 'Gradient', 'type': 'colormap'},
        {'name': 'Subgroup', 'type': 'group', 'children': [
            {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
            {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
        ]},
        {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
        {'name': 'Action Parameter', 'type': 'action'},
    ]},
    {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
        {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True, 'suffix': 'V'},
        {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
        {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True,
         'suffix': 'Hz'},

    ]},
    {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
        {'name': 'Save State', 'type': 'action'},
        {'name': 'Restore State', 'type': 'action', 'children': [
            {'name': 'Add missing items', 'type': 'bool', 'value': True},
            {'name': 'Remove extra items', 'type': 'bool', 'value': True},
        ]},
    ]},
    {'name': 'Extra Parameter Options', 'type': 'group', 'children': [
        {'name': 'Read-only', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
        {'name': 'Renamable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
        {'name': 'Removable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'removable': True},
    ]},
]

params = [
    {'name': 'Visulization', 'type': 'group', 'children': [
        {'name': 'Colormap limits', 'type': 'group', 'children': [
            ListParameter(name='Type', limits=['local', 'global', 'manual']),
            {'name': 'Lock current limits', 'type': 'bool', 'value': False},
            {'name': 'Lower limit', 'type': 'float'},
            {'name': 'Upper limit', 'type': 'float'},
            {'name': 'Threshold', 'type': 'float'},
        ]},
        {'name': 'Cortex', 'type': 'group', 'children':[
            {'name': 'Flattening', 'type': 'int', 'suffix': '%', 'bounds': [0, 100], 'step': 10, 'value': 0},
            ListParameter(name='Hemispheres', limits=['left', 'right', 'both']),
            ListParameter(name='Shader', limits=gl.shaders.ShaderProgram.names.keys(), value='shaded')
        ]},

    ]},
    {'name': 'Signal', 'type': 'group', 'children': [
        {'name': 'Filter bounds', 'type': 'group', 'children': [
            ListParameter(name='Type', limits=['Insantaneous', 'Envelope']),
            {'name': 'Filter', 'type': 'bool', 'value': False},
            {'name': 'Lower bound', 'type': 'float', 'suffix': 'Hz', 'value': None},
            {'name': 'Upper bound', 'type': 'float', 'suffix': 'Hz'},
        ]},
    ]}
]

## Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)


## If anything changes in the tree, print a message
def change(param, changes):
    print("tree changes:")
    for param, change, data in changes:
        path = p.childPath(param)
        if path is not None:
            childName = '.'.join(path)
        else:
            childName = param.name()
        print('  parameter: %s' % childName)
        print('  change:    %s' % change)
        print('  data:      %s' % str(data))
        print('  ----------')


p.sigTreeStateChanged.connect(change)


def valueChanging(param, value):
    print("Value changing (not finalized):", param, value)


# Too lazy for recursion:
for child in p.children():
    child.sigValueChanging.connect(valueChanging)
    for ch2 in child.children():
        ch2.sigValueChanging.connect(valueChanging)



## Create two ParameterTree widgets, both accessing the same data
t = ParameterTree(showHeader=False)
t.setParameters(p, showTop=False)
t.setWindowTitle('pyqtgraph example: Parameter Tree')

win = QtGui.QWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout.addWidget(QtGui.QLabel("This is just one parameter widget."), 0,
                 0, 1, 2)
layout.addWidget(t, 1, 0, 1, 1)
win.show()
win.resize(300, 500)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
