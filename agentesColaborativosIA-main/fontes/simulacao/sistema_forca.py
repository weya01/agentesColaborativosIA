"""
Sistema de Estado do Agente com Força.

Implementa a lógica de agente ganhar força ao encontrar tesouro
e usar essa força para desativar a próxima bomba.
"""
from enum import Enum
from typing import Tuple


class EstadoForca(Enum):
    """Estado de força do agente"""
    NORMAL = 0
    COM_FORCA = 1


class SistemaForca:
    """Gerencia força dos agentes"""
    
    def __init__(self):
        # {agente_id: {'forca': bool, 'bombas_desativadas': int}}
        self.estado_agentes = {}
    
    def criar_agente(self, agente_id: str):
        """Cria novo agente com estado de força"""
        self.estado_agentes[agente_id] = {
            'forca': False,
            'bombas_desativadas': 0,
            'tesouros_coletados': 0
        }
    
    def ganhar_forca(self, agente_id: str):
        """Agente ganha força ao encontrar tesouro"""
        if agente_id in self.estado_agentes:
            self.estado_agentes[agente_id]['forca'] = True
            self.estado_agentes[agente_id]['tesouros_coletados'] += 1
            return True
        return False
    
    def usar_forca(self, agente_id: str) -> bool:
        """
        Agente usa força para desativar bomba.
        Retorna True se tinha força e a usou.
        """
        if agente_id in self.estado_agentes:
            if self.estado_agentes[agente_id]['forca']:
                self.estado_agentes[agente_id]['forca'] = False
                self.estado_agentes[agente_id]['bombas_desativadas'] += 1
                return True
        return False
    
    def tem_forca(self, agente_id: str) -> bool:
        """Verifica se agente tem força"""
        if agente_id in self.estado_agentes:
            return self.estado_agentes[agente_id]['forca']
        return False
    
    def obter_estado(self, agente_id: str) -> dict:
        """Obtém estado de força de um agente"""
        return self.estado_agentes.get(agente_id, {})
    
    def resetar(self, agente_id: str):
        """Reseta estado de força (quando agente morre ou completa)"""
        if agente_id in self.estado_agentes:
            self.estado_agentes[agente_id]['forca'] = False
    
    def obter_metricas(self, agente_id: str) -> dict:
        """Retorna métricas de força"""
        estado = self.estado_agentes.get(agente_id, {})
        return {
            'tem_forca': estado.get('forca', False),
            'bombas_desativadas': estado.get('bombas_desativadas', 0),
            'tesouros_coletados': estado.get('tesouros_coletados', 0),
            'estado_forca': EstadoForca.COM_FORCA if estado.get('forca') else EstadoForca.NORMAL
        }

