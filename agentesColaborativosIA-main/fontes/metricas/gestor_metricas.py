"""
Gestor central de métricas para múltiplos grupos.
Coordena coleta e análise de dados de todos os grupos.
"""
from .metricas import MetricasGrupo
from collections import defaultdict
import json
from pathlib import Path
from datetime import datetime


class GestorMetricas:
    """Gerencia métricas de múltiplos grupos de agentes"""

    def __init__(self, diretorio_saida="logs/metricas"):
        """
        Args:
            diretorio_saida: Diretório para salvar relatórios
        """
        self.grupos = {}  # id_grupo -> MetricasGrupo
        self.diretorio_saida = Path(diretorio_saida)
        self.diretorio_saida.mkdir(parents=True, exist_ok=True)

    def criar_grupo(self, id_grupo, modo_jogo, tamanho_mapa=10):
        """Cria novo grupo de métricas"""
        self.grupos[id_grupo] = MetricasGrupo(id_grupo, modo_jogo, tamanho_mapa)
        return self.grupos[id_grupo]

    def obter_grupo(self, id_grupo):
        """Obtém métricas de um grupo"""
        return self.grupos.get(id_grupo)

    def listar_grupos(self):
        """Lista todos os grupos"""
        return list(self.grupos.keys())

    # =====================================================================
    # ANÁLISE COMPARATIVA
    # =====================================================================

    def comparar_grupos(self):
        """Compara métricas entre todos os grupos"""
        comparacao = {
            "total_grupos": len(self.grupos),
            "grupos": {}
        }

        for id_grupo, metricas in self.grupos.items():
            comparacao["grupos"][id_grupo] = {
                "modo": metricas.modo_jogo,
                "tesouros": metricas.obter_tesouros_coletados(),
                "cobertura": metricas.obter_cobertura_mapa(),
                "mortalidade": metricas.obter_taxa_mortalidade(),
                "eficiencia": metricas.obter_eficiencia_exploracao(),
                "sucesso": metricas.obter_taxa_sucesso()
            }

        # Calcula agregados
        comparacao["agregados"] = {
            "tesouros_total": sum(g["tesouros"] for g in comparacao["grupos"].values()),
            "cobertura_media": sum(g["cobertura"] for g in comparacao["grupos"].values()) / len(self.grupos) if self.grupos else 0,
            "mortalidade_media": sum(g["mortalidade"] for g in comparacao["grupos"].values()) / len(self.grupos) if self.grupos else 0,
        }

        return comparacao

    def listar_melhores_agentes(self, n=5):
        """Lista os N melhores agentes de todos os grupos"""
        todos_agentes = []
        
        for metricas_grupo in self.grupos.values():
            for id_agente, agente in metricas_grupo.agentes.items():
                todos_agentes.append({
                    "id": id_agente,
                    "grupo": metricas_grupo.id_grupo,
                    "tipo": agente.tipo_agente,
                    "eficiencia": agente._calcular_eficiencia(),
                    "tesouros": agente.tesouros_coletados,
                    "passos": agente.passos
                })

        # Ordena por eficiência
        todos_agentes.sort(key=lambda x: x["eficiencia"], reverse=True)
        return todos_agentes[:n]

    def listar_agentes_mortos(self):
        """Lista todos os agentes mortos e quando morreram"""
        mortos = []
        for metricas_grupo in self.grupos.values():
            for id_agente, agente in metricas_grupo.agentes.items():
                if agente.morto:
                    mortos.append({
                        "id": id_agente,
                        "grupo": metricas_grupo.id_grupo,
                        "tipo": agente.tipo_agente,
                        "turno_morte": agente.turno_morte,
                        "passos_antes_morte": agente.passos,
                        "tesouros_coletados": agente.tesouros_coletados
                    })
        return mortos

    # =====================================================================
    # EXPORTAR E SALVAR
    # =====================================================================

    def salvar_relatorios(self, nome_base="simulacao"):
        """Salva relatórios de todos os grupos em JSON"""
        relatorios = {}
        for id_grupo, metricas in self.grupos.items():
            relatorios[id_grupo] = metricas.obter_relatorio_completo()

        # Salva arquivo principal
        arquivo = self.diretorio_saida / f"{nome_base}_relatorios.json"
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(relatorios, f, indent=2, ensure_ascii=False, default=str)

        # Salva comparação
        arquivo_comp = self.diretorio_saida / f"{nome_base}_comparacao.json"
        with open(arquivo_comp, "w", encoding="utf-8") as f:
            json.dump(self.comparar_grupos(), f, indent=2, ensure_ascii=False, default=str)

        return {
            "relatorios": str(arquivo),
            "comparacao": str(arquivo_comp)
        }

    def salvar_resumos_visuais(self, nome_base="simulacao"):
        """Salva resumos formatados de todos os grupos"""
        arquivo = self.diretorio_saida / f"{nome_base}_resumos.txt"
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("RESUMOS DE SIMULAÇÕES\n")
            f.write("=" * 50 + "\n\n")

            for id_grupo, metricas in self.grupos.items():
                f.write(metricas.obter_resumo_visual())
                f.write("\n\n")

        return str(arquivo)

    def obter_relatorio_consolidado(self):
        """Retorna relatório consolidado de todas as simulações"""
        return {
            "timestamp": str(datetime.now()),
            "total_grupos": len(self.grupos),
            "comparacao": self.comparar_grupos(),
            "melhores_agentes": self.listar_melhores_agentes(10),
            "agentes_mortos": self.listar_agentes_mortos()
        }
