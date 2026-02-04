"""
Gerenciamento de grupos de agentes com diferentes estratégias.
Permite: grupos homogêneos (mesmo tipo) e grupos híbridos (mesclagem de tipos).
"""
from enum import Enum
from typing import List, Dict, Optional, Tuple
from agentes.base.agente_base import AgenteBase


class TipoGrupo(Enum):
    """Tipos de grupos de agentes"""
    HOMOGENEO = "homogêneo"      # Todos com mesmo tipo de algoritmo
    HIBRIDO = "híbrido"          # Mesclagem de dois tipos de algoritmos


class ConfiguracaoGrupo:
    """Configuração de um grupo de agentes"""
    
    def __init__(self, grupo_id: int, nome: str, tipo: TipoGrupo, 
                 tipos_agentes: List[str], tamanho: int = 3):
        """
        Args:
            grupo_id: Identificador único do grupo
            nome: Nome descritivo do grupo
            tipo: TipoGrupo.HOMOGENEO ou TipoGrupo.HIBRIDO
            tipos_agentes: Lista de tipos de agentes (1 para homogêneo, 2 para híbrido)
            tamanho: Número de agentes no grupo
        """
        self.grupo_id = grupo_id
        self.nome = nome
        self.tipo = tipo
        self.tipos_agentes = tipos_agentes
        self.tamanho = tamanho
        
        # Validação
        if tipo == TipoGrupo.HOMOGENEO and len(tipos_agentes) != 1:
            raise ValueError("Grupo homogêneo deve ter exatamente 1 tipo de agente")
        if tipo == TipoGrupo.HIBRIDO and len(tipos_agentes) != 2:
            raise ValueError("Grupo híbrido deve ter exatamente 2 tipos de agentes")


class GestorGrupos:
    """Gerencia grupos de agentes e suas métricas"""
    
    def __init__(self):
        self.grupos: Dict[int, ConfiguracaoGrupo] = {}
        self.agentes_por_grupo: Dict[int, List[AgenteBase]] = {}
        self.metricas_grupo: Dict[int, Dict] = {}
        self.proximo_grupo_id = 0
    
    def criar_grupo(self, nome: str, tipo: TipoGrupo, tipos_agentes: List[str], 
                   tamanho: int = 3) -> int:
        """
        Cria um novo grupo de agentes.
        
        Args:
            nome: Nome do grupo
            tipo: TipoGrupo.HOMOGENEO ou TipoGrupo.HIBRIDO
            tipos_agentes: Tipos de agentes a usar
            tamanho: Número de agentes
        
        Returns:
            grupo_id do grupo criado
        """
        config = ConfiguracaoGrupo(self.proximo_grupo_id, nome, tipo, 
                                   tipos_agentes, tamanho)
        self.grupos[self.proximo_grupo_id] = config
        self.agentes_por_grupo[self.proximo_grupo_id] = []
        self.metricas_grupo[self.proximo_grupo_id] = self._inicializar_metricas()
        
        grupo_id = self.proximo_grupo_id
        self.proximo_grupo_id += 1
        return grupo_id
    
    def adicionar_agente_grupo(self, grupo_id: int, agente: AgenteBase):
        """Adiciona agente a um grupo"""
        if grupo_id not in self.agentes_por_grupo:
            raise ValueError(f"Grupo {grupo_id} não existe")
        
        self.agentes_por_grupo[grupo_id].append(agente)
        agente.grupo_id = grupo_id
    
    def obter_agentes_grupo(self, grupo_id: int) -> List[AgenteBase]:
        """Obtém todos os agentes de um grupo"""
        return self.agentes_por_grupo.get(grupo_id, [])
    
    def obter_config_grupo(self, grupo_id: int) -> Optional[ConfiguracaoGrupo]:
        """Obtém configuração de um grupo"""
        return self.grupos.get(grupo_id)
    
    def atualizar_metricas_grupo(self, grupo_id: int):
        """Atualiza métricas agregadas de um grupo"""
        agentes = self.agentes_por_grupo.get(grupo_id, [])
        if not agentes:
            return
        
        metricas = {
            'total_agentes': len(agentes),
            'agentes_ativos': sum(1 for a in agentes if a.estado.value == 'ativo'),
            'agentes_mortos': sum(1 for a in agentes if a.estado.value == 'morto'),
            'passos_total': sum(a.passos for a in agentes),
            'passos_medio': sum(a.passos for a in agentes) / len(agentes) if agentes else 0,
            'bombas_acionadas_total': sum(a.bombas_acionadas for a in agentes),
            'tesouros_coletados_total': sum(a.tesouros_coletados for a in agentes),
            'celulas_exploradas_total': len(set().union(*(a.celulas_exploradas for a in agentes))),
            'celulas_seguras_total': len(set().union(*(a.celulas_seguras for a in agentes))),
        }
        
        self.metricas_grupo[grupo_id] = metricas
    
    def obter_metricas_grupo(self, grupo_id: int) -> Dict:
        """Obtém métricas de um grupo"""
        return self.metricas_grupo.get(grupo_id, {})
    
    def obter_comparacao_grupos(self) -> Dict:
        """Obtém comparação de desempenho entre grupos"""
        comparacao = {}
        for grupo_id, config in self.grupos.items():
            self.atualizar_metricas_grupo(grupo_id)
            metricas = self.metricas_grupo[grupo_id]
            comparacao[config.nome] = {
                'tipo': config.tipo.value,
                'tipos_agentes': config.tipos_agentes,
                'metricas': metricas
            }
        return comparacao
    
    def _inicializar_metricas(self) -> Dict:
        """Inicializa dicionário de métricas"""
        return {
            'total_agentes': 0,
            'agentes_ativos': 0,
            'agentes_mortos': 0,
            'passos_total': 0,
            'passos_medio': 0,
            'bombas_acionadas_total': 0,
            'tesouros_coletados_total': 0,
            'celulas_exploradas_total': 0,
            'celulas_seguras_total': 0,
        }
    
    def listar_grupos(self) -> List[Tuple[int, ConfiguracaoGrupo]]:
        """Lista todos os grupos"""
        return list(self.grupos.items())
