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
        self.spinBox.setMinimum(-300)
        self.spinBox.setMaximum(300)
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
        file_name = self.text.text() + "_pvc.json"
        self.parentWidget.saveJsonFile(file_name)
        print("Nome do arquivo salvo: ", file_name)
        self.close()
