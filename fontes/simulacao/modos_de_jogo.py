class ModosDeJogo:

    @staticmethod
    def modo_A(resultados, total_tesouros):
        return sum(r["tesouros"] for r in resultados) >= total_tesouros * 0.5

    @staticmethod
    def modo_B(resultados):
        return any(not r["morreu"] for r in resultados)

    @staticmethod
    def modo_C(bandeira_encontrada):
        return bandeira_encontrada

