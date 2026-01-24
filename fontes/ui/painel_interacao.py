from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel
)

class Painel(QWidget):
    def __init__(self, executar_callback):
        super().__init__()
        self.setWindowTitle("Agentes Colaborativos")

        self.layout = QVBoxLayout()

        self.info = QLabel("Escolha o modo:")
        self.layout.addWidget(self.info)

        self.btnA = QPushButton("Modo A")
        self.btnB = QPushButton("Modo B")
        self.btnC = QPushButton("Modo C")

        self.btnA.clicked.connect(lambda: executar_callback("A"))
        self.btnB.clicked.connect(lambda: executar_callback("B"))
        self.btnC.clicked.connect(lambda: executar_callback("C"))

        self.layout.addWidget(self.btnA)
        self.layout.addWidget(self.btnB)
        self.layout.addWidget(self.btnC)

        self.setLayout(self.layout)
