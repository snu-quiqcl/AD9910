# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 16:50:11 2018

@author: 1109282

Adapted from https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
and https://stackoverflow.com/questions/48264553/matplotlib-navigation-toolbar-embeded-in-pyqt5-window-reset-original-view-cras?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

"""



from __future__ import unicode_literals
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from numpy import arange, sin, pi

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        """
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        """
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



class PlotWindow(QtWidgets.QWidget):
    def __init__(self, title="Plot window"):
        QtWidgets.QWidget.__init__(self)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(title)

        l = QtWidgets.QVBoxLayout(self)
        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        l.addWidget(self.toolbar)
        l.addWidget(self.canvas)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    pw = PlotWindow()
    pw.show()
    #sys.exit(qApp.exec_())
    app.exec_()
