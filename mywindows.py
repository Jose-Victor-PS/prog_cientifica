from PyQt5.QtGui import *
from mycanvas import *
from mymodel import *


class MyWindow(QMainWindow):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,1200,800)
        self.setWindowTitle("Modelador")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)
        # create a Toolbar
        tb = self.addToolBar("File")
        fit = QAction(QIcon("icons/fit.png"), "fit", self)
        tb.addAction(fit)
        add_particle = QAction(QIcon("icons/particle.png"), "add_particle", self)
        tb.addAction(add_particle)
        model_line = QAction(QIcon("icons/model_line.png"), "model_line", self)
        tb.addAction(model_line)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "add_particle":
            self.canvas.addParticlesState()
        elif a.text() == "model_line":
            self.canvas.modelLineState()
