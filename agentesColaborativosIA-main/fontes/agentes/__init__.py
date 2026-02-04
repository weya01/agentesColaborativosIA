"""
Módulo com todos os agentes inteligentes do sistema.

Estrutura:
- base: Classe base AgenteBase com ciclo IA
- agentes_busca: Agentes com algoritmos de busca (BFS, DFS, A*, Gulosa)
- agentes_nao_busca: Agentes com estratégias simples (Aleatório, KNN, Exploração)
- agentes_hibridos: Agentes que combinam múltiplas estratégias (Híbrido, Adaptativo, Combinado)

Memória:
- memoria_partilhada: Memória partilhada por grupo de agentes
"""

from .base.agente_base import AgenteBase, EstadoAgente
from .agentes_busca.agente_busca import AgenteBusca, AgenteArvoreBusca
from .agentes_nao_busca.agente_nao_busca import AgenteAleatorio, AgenteExploracao, AgenteKNN
from .agentes_hibridos.agente_hibrido import AgenteHibrido, AgenteAdaptativo, AgenteCombinado
from .memoria_partilhada import MemoriaPartilhada

__all__ = [
    # Base
    'AgenteBase',
    'EstadoAgente',
    # Busca
    'AgenteBusca',
    'AgenteArvoreBusca',
    # Não-busca
    'AgenteAleatorio',
    'AgenteExploracao',
    'AgenteKNN',
    # Híbridos
    'AgenteHibrido',
    'AgenteAdaptativo',
    'AgenteCombinado',
    # Memória
    'MemoriaPartilhada'
]
