import sys
from PyQt5.QtWidgets import *


class Somador(QWidget):
    def __init__(self):
        super(Somador, self).__init__()
        self.setWindowTitle('PyQT')
        self.setGeometry(200, 200, 200, 200)

        self.label1 = QLabel('A: ', self)
        self.label2 = QLabel('B: ', self)
        self.result = QLabel('C: ', self)

        self.edit1 = QLineEdit(self)
        self.edit2 = QLineEdit(self)
        self.button = QPushButton('Soma', self)

        self.result.resize(150, 20)
        self.button.setStyleSheet('background-color: green; color: white;')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.edit1)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self.edit2)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.result)
        self.setLayout(self.vbox)

        self.button.clicked.connect(self.sum)

    def sum(self):
        number1 = int(self.edit1.text())
        number2 = int(self.edit2.text())
        result = number1 + number2
        self.result.setText('C: ' + str(result))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = Somador()
    my_widget.show()
    sys.exit(app.exec_())