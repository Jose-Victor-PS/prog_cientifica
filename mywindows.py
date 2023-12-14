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
        fencing_pvc = QAction(QIcon("icons/fencing_pvc.png"), "fencing_pvc", self)
        tb.addAction(fencing_pvc)
        temperature = QAction(QIcon("icons/temperature.png"), "temperature", self)
        tb.addAction(temperature)
        save_file = QAction(QIcon("icons/json_file.png"), "save_file", self)
        tb.addAction(save_file)
        run_mdf = QAction(QIcon("icons/run_mdf.png"), "run_mdf", self)
        tb.addAction(run_mdf)
        restr = QAction(QIcon("icons/restr.png"), "restr", self)
        tb.addAction(restr)
        forces = QAction(QIcon("icons/forces.png"), "forces", self)
        tb.addAction(forces)
        elasticity = QAction(QIcon("icons/elastic.png"), "elasticity", self)
        tb.addAction(elasticity)
        weight = QAction(QIcon("icons/weight.png"), "weight", self)
        tb.addAction(weight)

        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "add_particle":
            self.canvas.addParticlesState()
        elif a.text() == "model_line":
            self.canvas.modelLineState()
        elif a.text() == "fencing_pvc":
            self.canvas.fencingPvcState()
        elif a.text() == "temperature":
            self.canvas.openTemperatureUI()
        elif a.text() == "save_file":
            self.canvas.openSaveDialog()
        elif a.text() == "run_mdf":
            self.canvas.runMdfSolver()
        elif a.text() == "restr":
            self.canvas.openRestrDialog()
        elif a.text() == "forces":
            self.canvas.openForcesDialog()
        elif a.text() == "elasticity":
            self.canvas.openElasticityDialog()
        elif a.text() == "weight":
            self.canvas.openWeightDialog()
