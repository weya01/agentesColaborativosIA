"""
Validador de mapas para garantir integridade das simulações.
Verifica conectividade, acessibilidade de objetivos, etc.
"""
from collections import deque
from utils.constantes import ModoJogo

# Constantes de tipo de célula (compatível com gerador_de_mapa.py)
LIVRE = "L"
BOMBA = "B"
TESOURO = "T"
BANDEIRA = "F"


class ValidadorMapa:
    """Valida mapas gerados para garantir condições de jogo"""

    def __init__(self, matriz_mapa, tamanho=10, modo=ModoJogo.A_TESOUROS):
        """
        Args:
            matriz_mapa: Matriz 2D com tipos de célula
            tamanho: Dimensão do mapa
            modo: Modo de jogo
        """
        self.matriz = matriz_mapa
        self.tamanho = tamanho
        self.modo = modo

    def validar(self):
        """
        Valida o mapa de acordo com o modo de jogo.
        
        Returns:
            Tupla (válido: bool, mensagem: str)
        """
        # Validações básicas
        if not self._validar_tamanho():
            return False, "Mapa tem tamanho incorreto"
        
        if not self._validar_inicio():
            return False, "Célula inicial (0,0) não é livre"
        
        # Validações específicas do modo
        if self.modo == ModoJogo.A_TESOUROS:
            return self._validar_modo_tesouros()
        elif self.modo == ModoJogo.B_SOBREVIVENCIA:
            return self._validar_modo_sobrevivencia()
        elif self.modo == ModoJogo.C_BANDEIRA:
            return self._validar_modo_bandeira()
        
        return True, "Mapa válido"

    # =====================================================================
    # VALIDAÇÕES BÁSICAS
    # =====================================================================

    def _validar_tamanho(self):
        """Verifica se matriz tem tamanho correto"""
        if len(self.matriz) != self.tamanho:
            return False
        for linha in self.matriz:
            if len(linha) != self.tamanho:
                return False
        return True

    def _validar_inicio(self):
        """Verifica se início é sempre livre"""
        return self.matriz[0][0] == LIVRE

    # =====================================================================
    # VALIDAÇÕES POR MODO
    # =====================================================================

    def _validar_modo_tesouros(self):
        """
        Modo A: Necessário ter:
        - Pelo menos 5 tesouros acessíveis
        - Conectividade do mapa
        """
        # Valida conectividade
        visitados = self._flood_fill_bfs()
        
        # Conta tesouros acessíveis
        tesouros_acessiveis = 0
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.matriz[i][j] == TESOURO and (i, j) in visitados:
                    tesouros_acessiveis += 1
        
        if tesouros_acessiveis < 5:
            return False, f"Apenas {tesouros_acessiveis} tesouros acessíveis (mínimo 5)"
        
        return True, "Modo Tesouros válido"

    def _validar_modo_sobrevivencia(self):
        """
        Modo B: Necessário ter:
        - Mapa completamente conectado a partir de (0,0)
        - Pelo menos 50% do mapa acessível
        """
        visitados = self._flood_fill_bfs()
        
        # Verifica percentual acessível
        total_acessivel = len(visitados)
        total_celulas = self.tamanho * self.tamanho
        percentual = (total_acessivel / total_celulas) * 100
        
        if percentual < 50:
            return False, f"Apenas {percentual:.1f}% do mapa acessível (mínimo 50%)"
        
        return True, "Modo Sobrevivência válido"

    def _validar_modo_bandeira(self):
        """
        Modo C: Necessário ter:
        - Bandeira acessível a partir de (0,0)
        - Bandeira deve existir no mapa
        """
        # Localiza bandeira
        bandeira_pos = None
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.matriz[i][j] == BANDEIRA:
                    bandeira_pos = (i, j)
                    break
        
        if bandeira_pos is None:
            return False, "Bandeira não encontrada no mapa"
        
        # Verifica se bandeira é acessível
        visitados = self._flood_fill_bfs()
        if bandeira_pos not in visitados:
            return False, f"Bandeira em {bandeira_pos} não é acessível"
        
        return True, "Modo Bandeira válido"

    # =====================================================================
    # ALGORITMOS DE VALIDAÇÃO
    # =====================================================================

    def _flood_fill_bfs(self, inicio=(0, 0)):
        """
        Implementa BFS (Flood Fill) para encontrar todas as células acessíveis.
        
        Args:
            inicio: Posição inicial (padrão: (0,0))
            
        Returns:
            Set de posições acessíveis
        """
        fila = deque([inicio])
        visitados = set([inicio])

        while fila:
            x, y = fila.popleft()

            # Explora 4 vizinhos (sem diagonais)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                # Verifica limites
                if 0 <= nx < self.tamanho and 0 <= ny < self.tamanho:
                    # Já visitado?
                    if (nx, ny) not in visitados:
                        # Bomba bloqueia passagem
                        if self.matriz[nx][ny] != BOMBA:
                            visitados.add((nx, ny))
                            fila.append((nx, ny))

        return visitados

    def _contar_elementos(self, tipo):
        """Conta quantos elementos de um tipo existem no mapa"""
        count = 0
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.matriz[i][j] == tipo:
                    count += 1
        return count

    # =====================================================================
    # ANÁLISE E RELATÓRIO
    # =====================================================================

    def obter_relatorio(self):
        """Retorna análise completa do mapa"""
        visitados = self._flood_fill_bfs()
        
        relatorio = {
            "tamanho": self.tamanho,
            "modo": self.modo,
            "total_bombas": self._contar_elementos(BOMBA),
            "total_tesouros": self._contar_elementos(TESOURO),
            "tem_bandeira": self._contar_elementos(BANDEIRA) > 0,
            "celulas_acessiveis": len(visitados),
            "percentual_acessivel": (len(visitados) / (self.tamanho * self.tamanho)) * 100,
        }
        
        return relatorio