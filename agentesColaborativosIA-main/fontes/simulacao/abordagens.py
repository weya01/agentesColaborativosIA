"""
Definições das 3 Abordagens (A, B, C).

Cada abordagem segue uma estratégia diferente de comportamento dos agentes.
"""
from enum import Enum


class TipoAbordagem(Enum):
    """Tipos de abordagem"""
    A = "A"  # Tesouros - Prioridade em coletar tesouros
    B = "B"  # Sobrevivência - Prioridade em exploração e sobreviver
    C = "C"  # Bandeira - Prioridade em encontrar objetivo


class ConfiguracaoAbordagem:
    """Define comportamento de uma abordagem"""
    
    def __init__(self, tipo, nome, descricao, modo_jogo, prioridades):
        """
        Args:
            tipo: TipoAbordagem
            nome: Nome descritivo
            descricao: Descrição textual
            modo_jogo: ModoJogo associado
            prioridades: Dict com pesos de decisão
        """
        self.tipo = tipo
        self.nome = nome
        self.descricao = descricao
        self.modo_jogo = modo_jogo
        self.prioridades = prioridades


class AbordagensPadrao:
    """Define as 3 abordagens padrão do projeto"""
    
    @staticmethod
    def obter_abordagem_a():
        """
        ABORDAGEM A: COLETA DE TESOUROS
        
        Objetivo: Coletar ≥50% dos tesouros descobertos
        Estratégia: Agentes priorizam localização e coleta de tesouros
        Ambiente: Menos bombas (25%), mais tesouros (35%)
        
        Prioridades:
        - Buscar tesouros conhecidos
        - Explorar células desconhecidas
        - Evitar bombas
        """
        from utils.constantes import ModoJogo
        
        return ConfiguracaoAbordagem(
            tipo=TipoAbordagem.A,
            nome="Abordagem A - Coleta de Tesouros",
            descricao="Objetivo: Coletar ≥50% dos tesouros descobertos. "
                     "Ambiente com menos bombas e mais tesouros.",
            modo_jogo=ModoJogo.A_TESOUROS,
            prioridades={
                'tesouro': 1.0,      # Máxima prioridade
                'explorar': 0.7,     # Alta prioridade
                'bomba': -0.9,       # Evitar ao máximo
                'seguranca': 0.6,    # Importância moderada
            }
        )
    
    @staticmethod
    def obter_abordagem_b():
        """
        ABORDAGEM B: SOBREVIVÊNCIA
        
        Objetivo: Explorar ≥80% do mapa E manter agentes vivos
        Estratégia: Agentes priorizam exploração abrangente com cautela
        Ambiente: Balanceado (35% bombas, 10% tesouros)
        
        Prioridades:
        - Explorar tudo sistematicamente
        - Manter agentes vivos
        - Mapear segurança
        """
        from utils.constantes import ModoJogo
        
        return ConfiguracaoAbordagem(
            tipo=TipoAbordagem.B,
            nome="Abordagem B - Sobrevivência",
            descricao="Objetivo: Explorar ≥80% do mapa mantendo agentes vivos. "
                     "Ambiente balanceado com risco moderado.",
            modo_jogo=ModoJogo.B_SOBREVIVENCIA,
            prioridades={
                'explorar': 1.0,     # Máxima prioridade
                'seguranca': 0.95,   # Muito importante
                'tesouro': 0.2,      # Baixa prioridade
                'bomba': -1.0,       # Máximo evitar
            }
        )
    
    @staticmethod
    def obter_abordagem_c():
        """
        ABORDAGEM C: LOCALIZAÇÃO DE BANDEIRA
        
        Objetivo: Encontrar e chegar à bandeira
        Estratégia: Agentes focam em encontrar objetivo específico
        Ambiente: Muitas bombas (45%), sem tesouros, bandeira aleatória
        
        Prioridades:
        - Encontrar bandeira
        - Navegar de forma segura
        - Exploração direcionada
        """
        from utils.constantes import ModoJogo
        
        return ConfiguracaoAbordagem(
            tipo=TipoAbordagem.C,
            nome="Abordagem C - Localização de Bandeira",
            descricao="Objetivo: Encontrar e atingir a bandeira. "
                     "Ambiente com muitas bombas e bandeira aleatória.",
            modo_jogo=ModoJogo.C_BANDEIRA,
            prioridades={
                'objetivo': 1.0,     # Máxima prioridade
                'seguranca': 0.85,   # Muito importante
                'explorar': 0.5,     # Moderada (para encontrar bandeira)
                'bomba': -0.95,      # Evitar quase sempre
            }
        )
    
    @staticmethod
    def obter_todas():
        """Retorna as 3 abordagens padrão"""
        return {
            'A': AbordagensPadrao.obter_abordagem_a(),
            'B': AbordagensPadrao.obter_abordagem_b(),
            'C': AbordagensPadrao.obter_abordagem_c(),
        }
    
    @staticmethod
    def obter_por_tipo(tipo):
        """
        Obtém abordagem por tipo.
        
        Args:
            tipo: 'A', 'B', 'C' ou TipoAbordagem
            
        Returns:
            ConfiguracaoAbordagem
        """
        if isinstance(tipo, TipoAbordagem):
            tipo = tipo.value
        
        abordagens = AbordagensPadrao.obter_todas()
        return abordagens.get(tipo)

