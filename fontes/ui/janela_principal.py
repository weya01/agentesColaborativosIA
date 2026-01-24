from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QTimer

from ui.grid_mapa import GridMapa


class JanelaPrincipal(QWidget):
    def __init__(self, motor):
        super().__init__()
        self.motor = motor
        self.setWindowTitle("Agentes Colaborativos")

        self.layout = QVBoxLayout()
        self.grid = GridMapa(motor.mapa)

        self.btn_iniciar = QPushButton("Iniciar Simulação")
        self.btn_iniciar.clicked.connect(self.iniciar)

        self.layout.addWidget(self.grid)
        self.layout.addWidget(self.btn_iniciar)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar)

    def iniciar(self):
        self.timer.start(300)  # 300 ms por turno

    def atualizar(self):
        if not self.motor._fim():
            self.motor.executar()
            self.grid.atualizar(self.motor.agentes)
        else:
            self.timer.stop()
            print("Simulação terminou.")
            return
        self.motor.executar_um_turno()
        self.grid.atualizar(self.motor.agentes)