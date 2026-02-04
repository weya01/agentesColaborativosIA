"""
Sistema de métricas para análise de desempenho de agentes e grupos.
Rastreia 7 métricas obrigatórias e adicionais para análise profunda.
"""
from enum import Enum
from datetime import datetime
from collections import defaultdict
import json


class TipoMetrica(Enum):
    """Tipos de métricas rastreadas"""
    # Métricas obrigatórias (7)
    TESOUROS_COLETADOS = "tesouros_coletados"
    CELULAS_EXPLORADAS = "celulas_exploradas"
    TEMPO_DECORRIDO = "tempo_decorrido"
    AGENTES_VIVOS = "agentes_vivos"
    AGENTES_MORTOS = "agentes_mortos"
    BANDEIRA_ENCONTRADA = "bandeira_encontrada"
    ALGORITMOS_USADOS = "algoritmos_usados"
    
    # Métricas adicionais
    EFICIENCIA_EXPLORACAO = "eficiencia_exploracao"
    TAXA_MORTALIDADE = "taxa_mortalidade"
    COBERTURA_MAPA = "cobertura_mapa"
    PASSOS_TOTAIS = "passos_totais"
    BOMBAS_ACIONADAS = "bombas_acionadas"


class MetricasAgente:
    """Rastreia métricas de um agente individual"""

    def __init__(self, id_agente, tipo_agente):
        """
        Args:
            id_agente: ID único do agente
            tipo_agente: Tipo de agente (BusCA, Aleatorio, etc.)
        """
        self.id_agente = id_agente
        self.tipo_agente = tipo_agente
        self.passos = 0
        self.bombas_acionadas = 0
        self.tesouros_coletados = 0
        self.celulas_exploradas = set()
        self.celulas_seguras = set()
        self.morto = False
        self.turno_morte = None
        self.algoritmos_usados = defaultdict(int)  # contador de uso por algoritmo
        self.historico_movimentos = []
        self.historico_decisoes = []

    def registrar_passo(self):
        """Registra um passo do agente"""
        self.passos += 1

    def registrar_bomba(self):
        """Registra acionamento de bomba"""
        self.bombas_acionadas += 1

    def registrar_tesouro(self):
        """Registra coleta de tesouro"""
        self.tesouros_coletados += 1

    def registrar_celula_explorada(self, pos):
        """Registra célula explorada"""
        self.celulas_exploradas.add(pos)

    def registrar_celula_segura(self, pos):
        """Registra célula identificada como segura"""
        self.celulas_seguras.add(pos)

    def registrar_morte(self, turno):
        """Registra morte do agente"""
        self.morto = True
        self.turno_morte = turno

    def registrar_algoritmo(self, nome_algoritmo):
        """Registra uso de algoritmo"""
        self.algoritmos_usados[nome_algoritmo] += 1

    def registrar_movimento(self, de, para, decisao):
        """Registra histórico de movimento"""
        self.historico_movimentos.append({
            "de": de,
            "para": para,
            "decisao": decisao,
            "turno": self.passos
        })

    def registrar_decisao(self, contexto, algoritmo, acao):
        """Registra histórico de decisão"""
        self.historico_decisoes.append({
            "contexto": contexto,
            "algoritmo": algoritmo,
            "acao": acao,
            "turno": self.passos
        })

    def obter_metricas(self):
        """Retorna dicionário de métricas do agente"""
        return {
            "id_agente": self.id_agente,
            "tipo_agente": self.tipo_agente,
            "passos": self.passos,
            "bombas_acionadas": self.bombas_acionadas,
            "tesouros_coletados": self.tesouros_coletados,
            "celulas_exploradas": len(self.celulas_exploradas),
            "celulas_seguras": len(self.celulas_seguras),
            "morto": self.morto,
            "turno_morte": self.turno_morte,
            "algoritmos_principais": dict(self.algoritmos_usados),
            "eficiencia": self._calcular_eficiencia()
        }

    def _calcular_eficiencia(self):
        """Calcula índice de eficiência do agente"""
        if self.passos == 0:
            return 0.0
        
        # Eficiência = (tesouros + células exploradas) / passos
        beneficio = self.tesouros_coletados + (len(self.celulas_exploradas) * 0.1)
        return beneficio / self.passos


class MetricasGrupo:
    """Rastreia métricas de um grupo de agentes"""

    def __init__(self, id_grupo, modo_jogo, tamanho_mapa=10):
        """
        Args:
            id_grupo: ID único do grupo
            modo_jogo: Modo de jogo (A_TESOUROS, B_SOBREVIVENCIA, C_BANDEIRA)
            tamanho_mapa: Tamanho do mapa (padrão 10x10)
        """
        self.id_grupo = id_grupo
        self.modo_jogo = modo_jogo
        self.tamanho_mapa = tamanho_mapa
        self.agentes = {}  # id_agente -> MetricasAgente
        self.inicio_simulacao = datetime.now()
        self.fim_simulacao = None
        self.turno_atual = 0
        self.objetivo_alcancado = False
        self.historico_turno = []

    def adicionar_agente(self, id_agente, tipo_agente):
        """Adiciona um agente ao grupo"""
        self.agentes[id_agente] = MetricasAgente(id_agente, tipo_agente)

    def remover_agente(self, id_agente):
        """Remove um agente (morto ou saído)"""
        if id_agente in self.agentes:
            del self.agentes[id_agente]

    def registrar_passo_agente(self, id_agente):
        """Registra passo de um agente"""
        if id_agente in self.agentes:
            self.agentes[id_agente].registrar_passo()

    def registrar_bomba(self, id_agente):
        """Registra acionamento de bomba"""
        if id_agente in self.agentes:
            self.agentes[id_agente].registrar_bomba()

    def registrar_tesouro(self, id_agente):
        """Registra coleta de tesouro"""
        if id_agente in self.agentes:
            self.agentes[id_agente].registrar_tesouro()

    def registrar_morte_agente(self, id_agente, turno):
        """Registra morte de agente"""
        if id_agente in self.agentes:
            self.agentes[id_agente].registrar_morte(turno)

    def registrar_objetivo_alcancado(self):
        """Registra que objetivo foi alcançado"""
        self.objetivo_alcancado = True
        self.fim_simulacao = datetime.now()

    def avanca_turno(self):
        """Avança para próximo turno"""
        self.turno_atual += 1
        # Registra snapshot do turno
        self.historico_turno.append(self._snapshot_turno())

    def _snapshot_turno(self):
        """Captura estado atual do grupo"""
        return {
            "turno": self.turno_atual,
            "agentes_vivos": sum(1 for a in self.agentes.values() if not a.morto),
            "agentes_mortos": sum(1 for a in self.agentes.values() if a.morto),
            "tesouros_coletados": sum(a.tesouros_coletados for a in self.agentes.values()),
            "celulas_exploradas": len(self._get_celulas_exploradas_grupo())
        }

    def _get_celulas_exploradas_grupo(self):
        """Retorna conjunto de todas as células exploradas pelo grupo"""
        exploradas = set()
        for agente in self.agentes.values():
            exploradas.update(agente.celulas_exploradas)
        return exploradas

    # =====================================================================
    # MÉTRICAS OBRIGATÓRIAS (7)
    # =====================================================================

    def obter_tesouros_coletados(self):
        """Métrica 1: Total de tesouros coletados"""
        return sum(a.tesouros_coletados for a in self.agentes.values())

    def obter_celulas_exploradas(self):
        """Métrica 2: Total de células exploradas"""
        return len(self._get_celulas_exploradas_grupo())

    def obter_tempo_decorrido(self):
        """Métrica 3: Tempo decorrido em turnos"""
        return self.turno_atual

    def obter_agentes_vivos(self):
        """Métrica 4: Número de agentes vivos"""
        return sum(1 for a in self.agentes.values() if not a.morto)

    def obter_agentes_mortos(self):
        """Métrica 5: Número de agentes mortos"""
        return sum(1 for a in self.agentes.values() if a.morto)

    def obter_bandeira_encontrada(self):
        """Métrica 6: Se bandeira foi encontrada"""
        return self.objetivo_alcancado

    def obter_algoritmos_usados(self):
        """Métrica 7: Algoritmos usados e frequência"""
        algoritmos = defaultdict(int)
        for agente in self.agentes.values():
            for algo, freq in agente.algoritmos_usados.items():
                algoritmos[algo] += freq
        return dict(algoritmos)

    # =====================================================================
    # MÉTRICAS ADICIONAIS
    # =====================================================================

    def obter_eficiencia_exploracao(self):
        """Eficiência de exploração em relação ao tempo"""
        total_explorado = self.obter_celulas_exploradas()
        tempo = self.obter_tempo_decorrido()
        if tempo == 0:
            return 0.0
        return total_explorado / tempo

    def obter_taxa_mortalidade(self):
        """Percentual de agentes mortos"""
        total = len(self.agentes)
        if total == 0:
            return 0.0
        mortos = self.obter_agentes_mortos()
        return (mortos / total) * 100

    def obter_cobertura_mapa(self):
        """Percentual do mapa explorado"""
        explorado = self.obter_celulas_exploradas()
        total = self.tamanho_mapa * self.tamanho_mapa
        if total == 0:
            return 0
        return (explorado / total) * 100

    def obter_passos_totais(self):
        """Total de passos dados por todos os agentes"""
        return sum(a.passos for a in self.agentes.values())

    def obter_bombas_acionadas(self):
        """Total de bombas acionadas"""
        return sum(a.bombas_acionadas for a in self.agentes.values())

    def obter_taxa_sucesso(self):
        """Taxa de sucesso: objetivo alcançado?"""
        return 1.0 if self.objetivo_alcancado else 0.0

    # =====================================================================
    # RELATÓRIOS
    # =====================================================================

    def obter_relatorio_completo(self):
        """Retorna relatório completo de métricas"""
        tempo_total = (self.fim_simulacao or datetime.now()) - self.inicio_simulacao
        
        return {
            "grupo": self.id_grupo,
            "modo_jogo": self.modo_jogo,
            "tempo_simulacao": str(tempo_total),
            "objetivo_alcancado": self.objetivo_alcancado,
            # Métricas obrigatórias
            "metricas_obrigatorias": {
                "tesouros_coletados": self.obter_tesouros_coletados(),
                "celulas_exploradas": self.obter_celulas_exploradas(),
                "tempo_decorrido_turnos": self.obter_tempo_decorrido(),
                "agentes_vivos": self.obter_agentes_vivos(),
                "agentes_mortos": self.obter_agentes_mortos(),
                "bandeira_encontrada": self.obter_bandeira_encontrada(),
                "algoritmos_usados": self.obter_algoritmos_usados()
            },
            # Métricas adicionais
            "metricas_adicionais": {
                "eficiencia_exploracao": self.obter_eficiencia_exploracao(),
                "taxa_mortalidade_pct": self.obter_taxa_mortalidade(),
                "cobertura_mapa_pct": self.obter_cobertura_mapa(),
                "passos_totais": self.obter_passos_totais(),
                "bombas_acionadas": self.obter_bombas_acionadas(),
                "taxa_sucesso": self.obter_taxa_sucesso()
            },
            # Métricas por agente
            "agentes": {
                id_ag: self.agentes[id_ag].obter_metricas()
                for id_ag in self.agentes
            }
        }

    def obter_resumo_visual(self):
        """Retorna resumo formatado para exibição"""
        return f"""
        ╔════════════════════════════════════════════════╗
        ║         RESUMO DA SIMULAÇÃO - GRUPO {self.id_grupo}      ║
        ╠════════════════════════════════════════════════╣
        ║ OBJETIVOS                                      ║
        ║  • Tesouros coletados: {self.obter_tesouros_coletados():>25} ║
        ║  • Células exploradas: {self.obter_celulas_exploradas():>25} ║
        ║  • Cobertura do mapa: {self.obter_cobertura_mapa():>26.1f}% ║
        ║  • Bandeira encontrada: {'SIM' if self.obter_bandeira_encontrada() else 'NÃO':>21} ║
        ╠════════════════════════════════════════════════╣
        ║ TEMPO & AGENTES                                ║
        ║  • Turnos decorridos: {self.obter_tempo_decorrido():>25} ║
        ║  • Agentes vivos: {self.obter_agentes_vivos():>31} ║
        ║  • Agentes mortos: {self.obter_agentes_mortos():>30} ║
        ║  • Taxa mortalidade: {self.obter_taxa_mortalidade():>26.1f}% ║
        ╠════════════════════════════════════════════════╣
        ║ EFICIÊNCIA                                     ║
        ║  • Passos totais: {self.obter_passos_totais():>32} ║
        ║  • Bombas acionadas: {self.obter_bombas_acionadas():>28} ║
        ║  • Efic. exploração: {self.obter_eficiencia_exploracao():>26.2f} ║
        ║  • Taxa sucesso: {self.obter_taxa_sucesso():>32.1%} ║
        ╚════════════════════════════════════════════════╝
        """
