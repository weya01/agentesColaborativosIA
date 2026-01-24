class MemoriaPartilhada:
    def __init__(self):
        self.visitados = {}
        self.bombas = set()
        self.tesouros = set()

    def atualizar(self, pos, estado):
        self.visitados[pos] = estado
        if estado == "B":
            self.bombas.add(pos)
        elif estado == "T":
            self.tesouros.add(pos)

    def consultar(self, pos):
        return self.visitados.get(pos, None)
