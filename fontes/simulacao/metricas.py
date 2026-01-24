import time
import matplotlib.pyplot as plt

class Metricas:

    def plotar_histograma(grupo_nome, resultados):
        nomes = [r["agente"] for r in resultados]
        valores = [r["score"] for r in resultados]

        plt.figure(figsize=(8,5))
        plt.bar(nomes, valores)
        plt.title(f"Grupo: {grupo_nome}")
        plt.xlabel("Agentes")
        plt.ylabel("Score")
        plt.grid(True)
        plt.show()

    def __init__(self, nome_agente):
        self.nome = nome_agente
        self.inicio = time.time()

        self.tesouros = 0
        self.bombas = 0
        self.desarmadas = 0
        self.celulas = 0
        self.morreu = False

    def finalizar(self):
        return {
            "agente": self.nome,
            "tesouros": self.tesouros,
            "bombas": self.bombas,
            "desarmadas": self.desarmadas,
            "celulas": self.celulas,
            "morreu": self.morreu,
            "tempo": round(time.time() - self.inicio, 3),
            "score": self.calcular_score()
        }

    def calcular_score(self):
        return (
            self.tesouros * 10 +
            self.desarmadas * 5 -
            self.bombas * 10 +
            self.celulas
        )
