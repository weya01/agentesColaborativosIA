import time

CORES_GRUPOS = {
    "Busca": "blue",
    "KNN": "green",
    "NaiveBayes": "orange",
    "Hibrido": "purple"
}


class Comparador:
    def __init__(self):
        self.grupos = {}

    # -----------------------------
    # REGISTO INICIAL
    # -----------------------------
    def registrar_agente(self, agente):
        grupo = agente.grupo

        if grupo not in self.grupos:
            self.grupos[grupo] = {
                "agentes": {},
                "resultados": [],
                "cor": CORES_GRUPOS.get(grupo, "gray")
            }

        self.grupos[grupo]["agentes"][agente.nome] = {
            "inicio": time.time(),
            "fim": None,
            "morreu": False
        }

    # -----------------------------
    # ATUALIZAÇÕES
    # -----------------------------
    def registrar_passo(self, agente):
        pass  # apenas para contagem futura se quiseres

    def registrar_morte(self, agente):
        dados = self._get_agente(agente)
        dados["morreu"] = True
        dados["fim"] = time.time()

    def registrar_objetivo(self, agente):
        dados = self._get_agente(agente)
        dados["fim"] = time.time()

    # -----------------------------
    # RESULTADOS FINAIS
    # -----------------------------
    def registrar_resultado(self, grupo, resultado):
        self.grupos[grupo]["resultados"].append(resultado)

    def finalizar(self):
        relatorio = {}

        for grupo, dados in self.grupos.items():
            resultados = dados["resultados"]

            if not resultados:
                continue

            total = len(resultados)
            mortos = sum(1 for r in resultados if r["morreu"])
            media_score = sum(r["score"] for r in resultados) / total

            relatorio[grupo] = {
                "total": total,
                "mortos": mortos,
                "media_score": round(media_score, 2),
                "cor": dados["cor"],
                "resultados": resultados
            }

        return relatorio

    # -----------------------------
    # AUXILIAR
    # -----------------------------
    def _get_agente(self, agente):
        return self.grupos[agente.grupo]["agentes"][agente.nome]
