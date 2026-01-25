from PySide6.QtWidgets import QApplication
from agentes.agente_ml import AgenteML
from simulacao import comparador
from ui.janela_principal import JanelaPrincipal
from simulacao.motor import MotorSimulacao
from agentes.agente_busca import AgenteBFS
from agentes.agente_naive_bayes import AgenteNaiveBayes
from agentes.agente_knn import AgenteKNN
from agentes.memoria_partilhada import MemoriaPartilhada
from ambientes.gerador_de_mapa import Mapa, GeradorDeMapa
import sys


# Bombas existem em todos os modos
prob_bomba = float(input("Porcentagem de Bombas (0 a 100)(Recomendado: 30): ")) / 100
while prob_bomba < 0 or prob_bomba > 1:
    prob_bomba = float(input("Porcentagem de Bombas (0 a 100)(Recomendado: 30): ")) / 100

# Seleção do modo de jogo
modo_jogo = input("Modo de Jogo (A: Tesouros, B: Sobrevivência, C: Bandeira): ").upper()
while modo_jogo not in ["A", "B", "C"]:
    modo_jogo = input("Modo de Jogo (A: Tesouros, B: Sobrevivência, C: Bandeira): ").upper()

# Modo Bandeira não tem tesouros
if modo_jogo == "C":
    prob_tesouro = 0.0
else:
    prob_tesouro = float(input("Porcentagem de Tesouros (0 a 100)(Recomendado: 20): ")) / 100
    while prob_tesouro < 0 or prob_tesouro > 1:
        prob_tesouro = float(input("Porcentagem de Tesouros (0 a 100)(Recomendado: 20): ")) / 100


#mapa = Mapa()
#mapa.gerar()

mapa = GeradorDeMapa(tamanho=10, prob_bomba=prob_bomba, prob_tesouro=prob_tesouro, modo=modo_jogo).gerar()


memorias = {
    "BUSCA": MemoriaPartilhada(),
    "NAO_BUSCA": MemoriaPartilhada(),
    "HIBRIDO": MemoriaPartilhada()
}
memoria_B = memorias["NAO_BUSCA"]
memoria_NB = memorias["NAO_BUSCA"]
memoria_H = memorias["HIBRIDO"]

#agente = AgenteML("ML", mapa, memoria_NB)
    
agentes = [
    #AgenteBFS("BFS1", mapa, memoria),
    AgenteBFS("BFS2", mapa, memoria_B, modo_jogo),
    AgenteNaiveBayes("NB1", mapa, memoria_NB, modo_jogo),
    AgenteKNN("KNN1", mapa, memoria_NB, modo_jogo, k=3),
    AgenteML("ML", mapa, memoria_NB, modo_jogo)
]

motor = MotorSimulacao(mapa, agentes, modo=modo_jogo)

app = QApplication(sys.argv)
janela = JanelaPrincipal(motor)
janela.show()

sys.exit(app.exec())
