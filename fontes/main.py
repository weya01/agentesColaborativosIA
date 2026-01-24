from PySide6.QtWidgets import QApplication
from ui.janela_principal import JanelaPrincipal
from simulacao.motor import MotorSimulacao
from agentes.agente_busca import AgenteBFS
from agentes.memoria_partilhada import MemoriaPartilhada
from ambientes.gerador_de_mapa import Mapa
import sys

mapa = Mapa()
mapa.gerar()

memoria = MemoriaPartilhada()

agentes = [
    AgenteBFS("A1", mapa, memoria),
    AgenteBFS("A2", mapa, memoria)
]

motor = MotorSimulacao(mapa, agentes, modo="A")

app = QApplication(sys.argv)
janela = JanelaPrincipal(motor)
janela.show()
sys.exit(app.exec())
