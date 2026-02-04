"""
Ponto de entrada da aplicação.
Inicializa a simulação multi-agentes com 3 abordagens simultâneas.
"""
from PySide6.QtWidgets import QApplication
import sys

# Importa direto da interface nova (evita janela_principal.py legado)
from ui.janela_principal_clean import JanelaPrincipal


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


