"""
Definição de modos de jogo e verificação de objetivos.
"""


class ModosDeJogo:
    """Define os 3 modos de jogo e condições de sucesso"""

    MODO_A = "A"
    MODO_B = "B"
    MODO_C = "C"

    @staticmethod
    def verificar_objetivo_modo_a(tesouros_coletados, total_tesouros):
        """
        Modo A: Coletar 50% dos tesouros
        
        Args:
            tesouros_coletados: Número de tesouros já coletados
            total_tesouros: Total de tesouros no mapa
            
        Returns:
            bool: True se objetivo alcançado
        """
        if total_tesouros == 0:
            return False
        return tesouros_coletados >= (total_tesouros * 0.5)

    @staticmethod
    def verificar_objetivo_modo_b(celulas_exploradas, total_celulas, agentes_vivos):
        """
        Modo B: Explorar 80%+ do mapa e manter agentes vivos
        
        Args:
            celulas_exploradas: Número de células exploradas
            total_celulas: Total de células no mapa
            agentes_vivos: Quantos agentes ainda estão vivos
            
        Returns:
            bool: True se objetivo alcançado
        """
        cobertura = (celulas_exploradas / total_celulas) * 100 if total_celulas > 0 else 0
        return cobertura >= 80.0 and agentes_vivos > 0

    @staticmethod
    def verificar_objetivo_modo_c(bandeira_encontrada):
        """
        Modo C: Encontrar a bandeira
        
        Args:
            bandeira_encontrada: bool indicando se bandeira foi encontrada
            
        Returns:
            bool: True se objetivo alcançado
        """
        return bandeira_encontrada

    @staticmethod
    def obter_descricao_modo(modo):
        """Retorna descrição textual do modo"""
        descricoes = {
            "A": "Coletar 50% dos tesouros",
            "B": "Explorar 80% do mapa e sobreviver",
            "C": "Encontrar a bandeira"
        }
        return descricoes.get(modo, "Modo desconhecido")


