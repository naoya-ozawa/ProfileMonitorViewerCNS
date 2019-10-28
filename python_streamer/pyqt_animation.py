from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
import numpy as np
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
            
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]
            
        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)
    
def main():
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    area = DockArea()
    win.setCentralWidget(area)
    win.resize(1000,500)
    win.setWindowTitle('dockarea example')

    # Create Docks
    d1 = Dock("Dock1",size=(1,1))
    d2 = Dock("Dock2 - Image",size=(500,200))
    area.addDock(d1,'left')
    area.addDock(d2,'right',d1)

    w2 = pg.PlotWidget(title="Plot")
    w2.plot(np.random.normal(size=100))
    d2.addWidget(w2)
    win.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
