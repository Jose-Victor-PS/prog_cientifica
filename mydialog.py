from PyQt5.QtWidgets import *


class TempDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Temperatura")
        self.setGeometry(800, 275, 300, 200)
        self.temperatureNew = 0
        self.parentWidget = parent

        self.label = QLabel("Digite a Temperatura das Particulas")

        self.spinBox = QDoubleSpinBox()
        self.spinBox.setMinimum(-1000)
        self.spinBox.setMaximum(1000)
        self.spinBox.setValue(self.temperatureNew)
        self.spinBox.setSingleStep(1)
        self.spinBox.valueChanged.connect(self.valueChanged)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.spinBox)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def valueChanged(self):
        self.temperatureNew = self.spinBox.value()
        # print("Changed: ", self.temperatureNew)

    def apply(self):
        self.parentWidget.setParticlesTemperature(self.temperatureNew)
        print("Temperatura escolhida: ", self.temperatureNew)
        self.close()


class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Salvar Arquivo")
        self.setGeometry(800, 275, 300, 200)
        self.parentWidget = parent

        self.label = QLabel("Digite o nome do arquivo .json")

        self.text = QLineEdit()
        self.text.setMaxLength(20)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def apply(self):
        file_name = self.text.text()
        self.parentWidget.saveJsonFile(file_name)
        print("Nome do arquivo salvo: ", file_name)
        self.close()


class RestrDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aplicar Restr")
        self.setGeometry(800, 275, 300, 200)
        self.parentWidget = parent

        self.label = QLabel("Escolha os eixos para fixar")

        self.combobox = QComboBox()
        self.combobox.addItems(['X', 'Y', 'X e Y'])

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def apply(self):
        ctext = self.combobox.currentText()
        x = "X" in ctext
        y = "Y" in ctext
        self.parentWidget.applyRestr(x, y)
        print("Fixou nos eixos: ", ctext)
        self.close()


class ForcesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forces")
        self.setGeometry(800, 275, 300, 200)
        self.forcesXNew = 0
        self.forcesYNew = 0
        self.parentWidget = parent

        self.label_X = QLabel("Digite as Forces sobre as Particulas no eixo X")

        self.spinBox_X = QDoubleSpinBox()
        self.spinBox_X.setMinimum(-50_000)
        self.spinBox_X.setMaximum(50_000)
        self.spinBox_X.setValue(self.forcesXNew)
        self.spinBox_X.setSingleStep(100)
        self.spinBox_X.valueChanged.connect(self.valueChangedX)

        self.label_Y = QLabel("Digite as Forces sobre as Particulas no eixo Y")

        self.spinBox_Y = QDoubleSpinBox()
        self.spinBox_Y.setMinimum(-50_000)
        self.spinBox_Y.setMaximum(50_000)
        self.spinBox_Y.setValue(self.forcesYNew)
        self.spinBox_Y.setSingleStep(100)
        self.spinBox_Y.valueChanged.connect(self.valueChangedY)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label_X)
        layout.addWidget(self.spinBox_X)
        layout.addWidget(self.label_Y)
        layout.addWidget(self.spinBox_Y)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def valueChangedX(self):
        self.forcesXNew = self.spinBox_X.value()

    def valueChangedY(self):
        self.forcesYNew = self.spinBox_Y.value()

    def apply(self):
        self.parentWidget.setForcesOnParticles(self.forcesXNew, self.forcesYNew)
        print("Forces no eixo X: ", self.forcesXNew)
        print("Forces no eixo Y: ", self.forcesYNew)
        self.close()


class ElasticDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Elasticity")
        self.setGeometry(800, 275, 300, 200)
        self.kNew = 0
        self.parentWidget = parent

        self.label = QLabel("Digite a Constante Elastica")

        self.text = QLineEdit()
        self.text.setMaxLength(25)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def apply(self):
        self.parentWidget.setElasticity(int(self.text.text()))
        print("Constante Elastica escolhida: ", self.text.text())
        self.close()


class WeightDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Weight")
        self.setGeometry(800, 275, 300, 200)
        self.mNew = 0
        self.parentWidget = parent

        self.label = QLabel("Digite a Massa das Particulas")

        self.text = QLineEdit()
        self.text.setMaxLength(25)

        buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)
        layout.addWidget(buttonBox)
        self.resize(300, 200)
        self.setLayout(layout)

        okBtn = buttonBox.button(QDialogButtonBox.Ok)
        okBtn.clicked.connect(self.apply)
        cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
        cancelBtn.clicked.connect(self.reject)

    def apply(self):
        self.parentWidget.setWeight(int(self.text.text()))
        print("Massa da particula escolhida: ", self.text.text())
        self.close()
