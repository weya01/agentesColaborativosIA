from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from ui.cores import CORES


class GridMapa(QWidget):
    def __init__(self, mapa):
        super().__init__()
        self.mapa = mapa
        self.tamanho = mapa.tamanho
        self.layout = QGridLayout()
        self.celulas = {}

        # Cores para distinguir agentes
        self.cores_agentes = {
            "BFS1": "#00cc66",  # Verde
            "BFS2": "#0066cc",  # Azul
            "NB1": "#ff6600",   # Laranja
            "KNN1": "#cc00cc",  # Roxo
            "ML": "#ffcc00"     # Amarelo
        }

        self.setLayout(self.layout)
        self._criar_grid()

    def _criar_grid(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                label = QLabel()
                label.setFixedSize(30, 30)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("border: 1px solid #aaa;")
                self.layout.addWidget(label, i, j)
                self.celulas[(i, j)] = label

    def atualizar(self, agentes):
        # limpa
        for (x, y), label in self.celulas.items():
            valor = self.mapa.ver((x, y))
            label.setStyleSheet(
                f"background-color: {CORES.get(valor, '#fff')};"
            )

        # desenha agentes
        for ag in agentes:
            if ag.vivo:
                cor = self.cores_agentes.get(ag.nome, CORES['A'])
                self.celulas[(ag.x, ag.y)].setStyleSheet(
                    f"background-color: {cor};"
                )
