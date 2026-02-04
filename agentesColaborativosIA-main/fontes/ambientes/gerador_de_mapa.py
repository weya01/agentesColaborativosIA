"""
Gerador e gerenciador de mapas para as simulações.
Cria mapas adaptados para cada modo de jogo.
"""
from utils.constantes import ModoJogo
import random
from copy import deepcopy

# Constantes de tipo de célula
LIVRE = "L"
BOMBA = "B"
TESOURO = "T"
BANDEIRA = "F"


class GeradorDeMapa:
    """Gera mapas aleatórios adaptados para cada modo de jogo"""

    def __init__(self, tamanho=10, modo=ModoJogo.A_TESOUROS, percentagem_bombas=None):
        """
        Args:
            tamanho: Dimensão do mapa (10x10)
            modo: Modo de jogo (A_TESOUROS, B_SOBREVIVENCIA, C_BANDEIRA)
            percentagem_bombas: Percentagem de bombas (50-80). Se None, usa padrão.
        """
        self.tamanho = tamanho
        self.modo = modo
        self.percentagem_bombas = percentagem_bombas

    def gerar(self):
        """Gera mapa adaptado ao modo de jogo"""
        if self.modo == ModoJogo.A_TESOUROS:
            return self._mapa_tesouros()
        elif self.modo == ModoJogo.B_SOBREVIVENCIA:
            return self._mapa_sobrevivencia()
        elif self.modo == ModoJogo.C_BANDEIRA:
            return self._mapa_bandeira()
        else:
            return self._mapa_tesouros()

    # =====================================================================
    # MODOS DE JOGO
    # =====================================================================

    def _mapa_tesouros(self):
        """
        Modo A: Objetivo é coletar 50% dos tesouros.
        Menos bombas, mais tesouros.
        """
        prob_bomba = self.percentagem_bombas / 100 if self.percentagem_bombas else 0.25
        return self._gerar_mapa(
            prob_bomba=prob_bomba,
            prob_tesouro=0.35,
            com_bandeira=False
        )

    def _mapa_sobrevivencia(self):
        """
        Modo B: Objetivo é explorar tudo e sobreviver.
        MUITO poucas bombas para permitir exploração >80% com sobrevivência.
        """
        prob_bomba = self.percentagem_bombas / 100 if self.percentagem_bombas else 0.02
        return self._gerar_mapa(
            prob_bomba=prob_bomba,
            prob_tesouro=0.10,
            com_bandeira=False
        )

    def _mapa_bandeira(self):
        """
        Modo C: Objetivo é encontrar a bandeira.
        Com agentes aleatórios defensivos, precisa de poucas bombas para viabilizar.
        """
        prob_bomba = self.percentagem_bombas / 100 if self.percentagem_bombas else 0.10
        return self._gerar_mapa(
            prob_bomba=prob_bomba,
            prob_tesouro=0.0,
            com_bandeira=True
        )

    # =====================================================================
    # FUNÇÃO BASE DE GERAÇÃO
    # =====================================================================

    def _gerar_mapa(self, prob_bomba, prob_tesouro, com_bandeira):
        """
        Gera matriz aleatória com probabilidades definidas.
        Garante que (0,0) seja sempre livre.
        
        As probabilidades são tratadas como proporções:
        - Bombas: prob_bomba
        - Tesouros: prob_tesouro
        - Livres: resto
        """
        mapa = []
        
        # Normaliza probabilidades para garantir que a soma não exceda 1.0
        # Ajusta proporção de tesouros se necessário
        prob_tesouro_ajustada = min(prob_tesouro, 1.0 - prob_bomba)

        # Gera cada célula aleatoriamente
        for i in range(self.tamanho):
            linha = []
            for j in range(self.tamanho):
                r = random.random()
                if r < prob_bomba:
                    linha.append(BOMBA)
                elif r < prob_bomba + prob_tesouro_ajustada:
                    linha.append(TESOURO)
                else:
                    linha.append(LIVRE)
            mapa.append(linha)

        # Garante que início é sempre livre
        mapa[0][0] = LIVRE

        # Coloca bandeira se necessário
        if com_bandeira:
            self._colocar_bandeira(mapa)

        return mapa

    def _colocar_bandeira(self, mapa):
        """Coloca bandeira em posição aleatória livre"""
        tentativas = 0
        while tentativas < 100:
            x = random.randint(0, self.tamanho - 1)
            y = random.randint(0, self.tamanho - 1)
            if mapa[x][y] == LIVRE and (x, y) != (0, 0):
                mapa[x][y] = BANDEIRA
                return
            tentativas += 1


class Mapa:
    """Gerencia o mapa durante a simulação"""

    def __init__(self, tamanho=10, modo=ModoJogo.A_TESOUROS):
        """
        Args:
            tamanho: Dimensão do mapa
            modo: Modo de jogo
        """
        self.tamanho = tamanho
        self.modo = modo
        self.gerador = GeradorDeMapa(tamanho, modo)
        self.matriz = self.gerador.gerar()

    def regenerar(self):
        """Regenera um novo mapa"""
        self.matriz = self.gerador.gerar()

    def ver(self, pos):
        """
        Vê o conteúdo de uma célula.
        
        Args:
            pos: Tupla (x, y)
            
        Returns:
            Tipo de célula: "L" (livre), "B" (bomba), "T" (tesouro), "F" (bandeira)
        """
        x, y = pos
        if self._posicao_valida(x, y):
            return self.matriz[x][y]
        return None

    def vizinhos(self, pos):
        """
        Retorna lista de posições vizinhas válidas (4 direções).
        
        Args:
            pos: Tupla (x, y)
            
        Returns:
            Lista de tuplas (x, y) válidas
        """
        x, y = pos
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # CIMA, BAIXO, ESQUERDA, DIREITA
        validos = []
        
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if self._posicao_valida(nx, ny):
                validos.append((nx, ny))
        
        return validos

    def vizinhos_com_diagonais(self, pos):
        """
        Retorna lista de posições vizinhas válidas (8 direções incluindo diagonais).
        
        Args:
            pos: Tupla (x, y)
            
        Returns:
            Lista de tuplas (x, y) válidas
        """
        x, y = pos
        direcoes = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # 4 direções principais
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # 4 diagonais
        ]
        validos = []
        
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if self._posicao_valida(nx, ny):
                validos.append((nx, ny))
        
        return validos

    def obter_distancia(self, pos1, pos2):
        """
        Calcula distância Manhattan entre duas posições.
        
        Args:
            pos1, pos2: Tuplas (x, y)
            
        Returns:
            Distância Manhattan
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def obter_dimensoes(self):
        """Retorna tupla (tamanho, tamanho)"""
        return (self.tamanho, self.tamanho)

    def _posicao_valida(self, x, y):
        """Verifica se posição está dentro dos limites"""
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    def obter_matriz_copia(self):
        """Retorna cópia da matriz para análise"""
        return deepcopy(self.matriz)
