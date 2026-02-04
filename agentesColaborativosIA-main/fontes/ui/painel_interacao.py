"""
Painel de interação auxiliar para UI.
"""
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout


class PainelInteracao(QWidget):
    """Painel adicional para controles de interação"""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        titulo = QLabel("Controles Rápidos")
        titulo.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.layout.addWidget(titulo)

        # Botões de conveniência
        self.btn_acelerar = QPushButton("⏩ Acelerar")
        self.btn_desacelerar = QPushButton("⏪ Desacelerar")
        
        botoes = QHBoxLayout()
        botoes.addWidget(self.btn_acelerar)
        botoes.addWidget(self.btn_desacelerar)
        self.layout.addLayout(botoes)

        self.layout.addStretch()
        self.setLayout(self.layout)

