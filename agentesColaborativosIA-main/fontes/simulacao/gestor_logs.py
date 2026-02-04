"""
Sistema de Logs para Simulação.

Registra todas as ações de agentes, objetivos alcançados, e eventos importantes.
"""
from datetime import datetime
from enum import Enum
from typing import List, Dict


class TipoEvento(Enum):
    """Tipos de eventos que podem ocorrer na simulação"""
    AGENTE_CRIADO = "AGENTE_CRIADO"
    AGENTE_MOVEU = "AGENTE_MOVEU"
    AGENTE_EXPLOROU_LIVRE = "AGENTE_EXPLOROU_LIVRE"
    AGENTE_ENCONTROU_TESOURO = "AGENTE_ENCONTROU_TESOURO"
    AGENTE_GANHOU_FORCA = "AGENTE_GANHOU_FORCA"
    AGENTE_DESATIVOU_BOMBA = "AGENTE_DESATIVOU_BOMBA"
    AGENTE_MORREU_BOMBA = "AGENTE_MORREU_BOMBA"
    AGENTE_COMPLETOU = "AGENTE_COMPLETOU"
    OBJETIVO_ALCANCADO = "OBJETIVO_ALCANCADO"
    SIMULACAO_INICIADA = "SIMULACAO_INICIADA"
    SIMULACAO_TERMINADA = "SIMULACAO_TERMINADA"
    COMPARTILHAMENTO_INFO = "COMPARTILHAMENTO_INFO"


class Evento:
    """Representa um evento na simulação"""
    
    def __init__(self, turno: int, tipo: TipoEvento, agente_id: str, 
                 grupo_id: int, mensagem: str, dados: Dict = None):
        self.timestamp = datetime.now()
        self.turno = turno
        self.tipo = tipo
        self.agente_id = agente_id
        self.grupo_id = grupo_id
        self.mensagem = mensagem
        self.dados = dados or {}
    
    def __str__(self):
        return (f"[T{self.turno:03d}] [{self.tipo.value}] {self.agente_id} "
                f"(Grupo {self.grupo_id}): {self.mensagem}")


class GestorLogs:
    """Gerencia logs de simulação"""
    
    def __init__(self):
        self.eventos = []  # Lista de todos os eventos
        self.por_agente = {}  # {agente_id: [eventos]}
        self.por_grupo = {}  # {grupo_id: [eventos]}
        self.por_tipo = {}  # {tipo: [eventos]}
        
        # Contadores
        self.contadores = {
            'agentes_criados': 0,
            'movimentos': 0,
            'tesouros_encontrados': 0,
            'bombas_acionadas': 0,
            'agentes_mortos': 0,
            'objetivos_alcancados': 0,
        }
    
    def registrar(self, evento: Evento):
        """Registra um evento"""
        self.eventos.append(evento)
        
        # Indexa por agente
        if evento.agente_id not in self.por_agente:
            self.por_agente[evento.agente_id] = []
        self.por_agente[evento.agente_id].append(evento)
        
        # Indexa por grupo
        if evento.grupo_id not in self.por_grupo:
            self.por_grupo[evento.grupo_id] = []
        self.por_grupo[evento.grupo_id].append(evento)
        
        # Indexa por tipo
        if evento.tipo not in self.por_tipo:
            self.por_tipo[evento.tipo] = []
        self.por_tipo[evento.tipo].append(evento)
        
        # Atualiza contadores
        if evento.tipo == TipoEvento.AGENTE_CRIADO:
            self.contadores['agentes_criados'] += 1
        elif evento.tipo == TipoEvento.AGENTE_MOVEU:
            self.contadores['movimentos'] += 1
        elif evento.tipo == TipoEvento.AGENTE_ENCONTROU_TESOURO:
            self.contadores['tesouros_encontrados'] += 1
        elif evento.tipo == TipoEvento.AGENTE_MORREU_BOMBA:
            self.contadores['agentes_mortos'] += 1
        elif evento.tipo == TipoEvento.OBJETIVO_ALCANCADO:
            self.contadores['objetivos_alcancados'] += 1
    
    def gerar_relatorio(self, grupo_id: int = None) -> str:
        """Gera relatório de logs"""
        relatorio = ""
        relatorio += "\n" + "="*70 + "\n"
        relatorio += "RELATÓRIO DE SIMULAÇÃO\n"
        relatorio += "="*70 + "\n"
        
        if grupo_id is not None:
            relatorio += f"\nGRUPO {grupo_id}:\n"
            relatorio += "-"*70 + "\n"
            eventos_grupo = self.por_grupo.get(grupo_id, [])
            for evento in eventos_grupo:
                relatorio += str(evento) + "\n"
        else:
            relatorio += "\nTODOS OS EVENTOS:\n"
            relatorio += "-"*70 + "\n"
            for evento in self.eventos:
                relatorio += str(evento) + "\n"
        
        relatorio += "\n" + "="*70 + "\n"
        relatorio += "ESTATÍSTICAS\n"
        relatorio += "="*70 + "\n"
        for chave, valor in self.contadores.items():
            relatorio += f"{chave:30s}: {valor}\n"
        
        return relatorio
    
    def gerar_log_sucinto(self, grupo_id: int) -> str:
        """Gera log sucinto de um grupo"""
        eventos_grupo = self.por_grupo.get(grupo_id, [])
        
        linhas = []
        linhas.append(f"\n{'='*70}")
        linhas.append(f"LOG DO GRUPO {grupo_id}")
        linhas.append(f"{'='*70}")
        
        for evento in eventos_grupo[-20:]:  # Últimos 20 eventos
            linhas.append(str(evento))
        
        return "\n".join(linhas)
    
    def obter_eventos_tipo(self, tipo: TipoEvento) -> List[Evento]:
        """Obtém todos os eventos de um tipo"""
        return self.por_tipo.get(tipo, [])
    
    def obter_eventos_agente(self, agente_id: str) -> List[Evento]:
        """Obtém todos os eventos de um agente"""
        return self.por_agente.get(agente_id, [])
    
    def obter_eventos_grupo(self, grupo_id: int) -> List[Evento]:
        """Obtém todos os eventos de um grupo"""
        return self.por_grupo.get(grupo_id, [])
    
    def limpar(self):
        """Limpa todos os logs"""
        self.eventos = []
        self.por_agente = {}
        self.por_grupo = {}
        self.por_tipo = {}
        self.contadores = {
            'agentes_criados': 0,
            'movimentos': 0,
            'tesouros_encontrados': 0,
            'bombas_acionadas': 0,
            'agentes_mortos': 0,
            'objetivos_alcancados': 0,
        }
    
    def exportar_csv(self, caminho_ficheiro: str):
        """Exporta logs para CSV"""
        import csv
        
        with open(caminho_ficheiro, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Turno', 'Timestamp', 'Tipo', 'Agente', 'Grupo', 'Mensagem'])
            
            for evento in self.eventos:
                writer.writerow([
                    evento.turno,
                    evento.timestamp.isoformat(),
                    evento.tipo.value,
                    evento.agente_id,
                    evento.grupo_id,
                    evento.mensagem
                ])
        
        print(f"Logs exportados para: {caminho_ficheiro}")

