from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

class GridMapa(QWidget):
    def __init__(self, mapa):
        super().__init__()
        self.mapa = mapa
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.labels = []

        self._criar_grade()

    def _criar_grade(self):
        for i in range(len(self.mapa)):
            linha = []
            for j in range(len(self.mapa[0])):
                lbl = QLabel()
                lbl.setFixedSize(40, 40)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet("border: 1px solid black;")
                self.layout.addWidget(lbl, i, j)
                linha.append(lbl)
            self.labels.append(linha)

    def atualizar(self, agentes):
        # Limpa tudo
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                self.labels[i][j].setText("")
                self.labels[i][j].setStyleSheet("border:1px solid black;")

        # Desenha agentes
        for agente in agentes:
            if agente.vivo:
                x, y = agente.x, agente.y
                self.labels[x][y].setText(agente.nome[0])
                self.labels[x][y].setStyleSheet(
                    "background-color: lightblue; border: 1px solid black;"
                )
