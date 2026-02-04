"""
Agentes que não usam algoritmos de busca formais.
Usam estratégias simples: aleatória, exploração, KNN.
"""
import random
from ..base.agente_base import AgenteBase


class AgenteAleatorio(AgenteBase):
    """
    Agente que toma decisões aleatórias.
    Escolhe entre algoritmos: movimento aleatório puro e exploração aleatória.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, algoritmos=None):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.algoritmos_disponiveis = algoritmos or ["aleatorio_puro", "aleatorio_seguro", "aleatorio_cauteloso"]
        self.indice_algoritmo_atual = 0
        self.algoritmo_em_uso = self.algoritmos_disponiveis[0]

    def _decidir_acao_interna(self):
        """Decide ação usando estratégia aleatória"""
        algoritmo = self.algoritmos_disponiveis[self.indice_algoritmo_atual]
        self.algoritmo_em_uso = algoritmo

        if algoritmo == "aleatorio_puro":
            return self._aleatorio_puro()
        elif algoritmo == "aleatorio_seguro":
            return self._aleatorio_seguro()
        elif algoritmo == "aleatorio_cauteloso":
            return self._aleatorio_cauteloso()
        
        return self._aleatorio_puro()

    def _aleatorio_puro(self):
        """
        Movimento completamente aleatório.
        Pode entrar em bombas.
        """
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)

    def _aleatorio_seguro(self):
        """
        Movimento aleatório evitando bombas conhecidas.
        PRIORIZA posições novas sobre exploradas.
        
        ESTRATÉGIA - POR ORDEM DE PREFERÊNCIA:
        1. Posições NUNCA VISTAS (não em celulas_exploradas) - OBRIGATÓRIO
        2. Se nenhuma posição nova disponível, FICA NO LUGAR ou TERMINA
        
        NUNCA entra em bomba conhecida!
        NUNCA revisa célula já explorada!
        """
        direcoes = [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]
        bombas_conhecidas = self.memoria_grupo.obter_bombas(self.grupo_id)

        # Coleta apenas posições NOVAS (nunca exploradas)
        posicoes_novas = []
        
        for acao, dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            
            # Verifica validade
            if not self._posicao_valida(novo_x, novo_y):
                continue
            
            pos = (novo_x, novo_y)
            
            # NUNCA entrar em bomba conhecida
            if pos in bombas_conhecidas:
                continue
            
            # NUNCA revisar célula já explorada
            if pos in self.celulas_exploradas:
                continue
            
            # Esta é uma posição nova
            posicoes_novas.append(acao)

        # Se há posições novas, escolhe uma aleatoriamente
        if posicoes_novas:
            return random.choice(posicoes_novas)
        
        # Se não há posições novas, termina exploração para este agente
        # (não há mais aonde ir)
        return None  # Sinifica que completou sua exploração

    def _aleatorio_cauteloso(self):
        """
        Movimento cauteloso: prioriza células SABIDAMENTE SEGURAS.
        
        ESTRATÉGIA - POR ORDEM DE PREFERÊNCIA:
        1. Posições NOVAS E SEGURAS (conhecidas como seguras)
        2. Posições NOVAS (desconhecidas)
        3. Posições SEGURAS (já vistas e são seguras)
        4. Nenhuma ação
        
        Nunca entra em bomba conhecida!
        """
        direcoes = [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]
        bombas_conhecidas = self.memoria_grupo.obter_bombas(self.grupo_id)

        posicoes_novas_seguras = []
        posicoes_novas = []
        posicoes_seguras_vistas = []
        
        for acao, dx, dy in direcoes:
            novo_x, novo_y = self.x + dx, self.y + dy
            
            if not self._posicao_valida(novo_x, novo_y):
                continue
            
            pos = (novo_x, novo_y)
            
            if pos in bombas_conhecidas:
                continue
            
            explorada = pos in self.celulas_exploradas
            segura = pos in self.celulas_seguras
            
            if not explorada and segura:
                posicoes_novas_seguras.append(acao)
            elif not explorada:
                posicoes_novas.append(acao)
            elif segura:
                posicoes_seguras_vistas.append(acao)

        # Retorna por ordem de prioridade
        if posicoes_novas_seguras:
            return random.choice(posicoes_novas_seguras)
        elif posicoes_novas:
            return random.choice(posicoes_novas)
        elif posicoes_seguras_vistas:
            return random.choice(posicoes_seguras_vistas)
        
        return None


class AgenteExploracao(AgenteBase):
    """
    Agente focado em exploração do mapa.
    Implementa múltiplos algoritmos de exploração: espiral, por camadas, aleatória dirigida.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, algoritmos=None):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.algoritmos_disponiveis = algoritmos or ["espiral", "camadas", "aleatorio_dirigido"]
        self.indice_algoritmo_atual = 0
        self.caminho_explorado = []
        self.camadas_exploradas = 0

    def _decidir_acao_interna(self):
        """Decide ação com base em estratégia de exploração"""
        algoritmo = self.algoritmos_disponiveis[self.indice_algoritmo_atual]
        self.algoritmo_em_uso = algoritmo

        if algoritmo == "espiral":
            return self._explorar_espiral()
        elif algoritmo == "camadas":
            return self._explorar_camadas()
        elif algoritmo == "aleatorio_dirigido":
            return self._aleatorio_dirigido()

        return self._aleatorio_dirigido()

    def _explorar_espiral(self):
        """
        Exploração em espiral a partir do centro.
        Move em padrão quadrado expandindo para fora.
        """
        # Distância do centro (4.5, 4.5)
        centro_x, centro_y = 4.5, 4.5
        dist_centro = abs(self.x - centro_x) + abs(self.y - centro_y)

        # Tenta se afastar do centro
        melhor_acao = None
        max_dist = -1

        for acao, dx, dy in [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y) and self.mapa.ver((novo_x, novo_y)) != "B":
                nova_dist = abs(novo_x - centro_x) + abs(novo_y - centro_y)
                if nova_dist > max_dist:
                    max_dist = nova_dist
                    melhor_acao = acao

        return melhor_acao if melhor_acao else self._acao_aleatoria()

    def _explorar_camadas(self):
        """
        Exploração em camadas concêntricas.
        Explora camada por camada afastando-se do centro.
        """
        camada_atual = max(abs(self.x - 4.5), abs(self.y - 4.5))
        
        # Tenta se mover para camada mais distante
        for acao, dx, dy in [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y):
                nova_camada = max(abs(novo_x - 4.5), abs(novo_y - 4.5))
                if nova_camada > camada_atual and self.mapa.ver((novo_x, novo_y)) != "B":
                    return acao

        return self._acao_aleatoria()

    def _aleatorio_dirigido(self):
        """
        Aleatoriedade dirigida: prefere e EXIGE células não exploradas.
        
        Se não há células não exploradas disponíveis, retorna None
        para indicar que exploração completou.
        """
        celulas_nao_exploradas = []
        
        for acao, dx, dy in [("CIMA", -1, 0), ("BAIXO", 1, 0), ("ESQUERDA", 0, -1), ("DIREITA", 0, 1)]:
            novo_x, novo_y = self.x + dx, self.y + dy
            if self._posicao_valida(novo_x, novo_y):
                pos = (novo_x, novo_y)
                if pos not in self.celulas_exploradas and self.mapa.ver(pos) != "B":
                    celulas_nao_exploradas.append(acao)

        if celulas_nao_exploradas:
            return random.choice(celulas_nao_exploradas)
        
        # Nenhuma posição nova disponível - exploração completada
        return None

    def _acao_aleatoria(self):
        """Ação completamente aleatória"""
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)


class AgenteKNN(AgenteBase):
    """
    Agente que usa KNN (K-Nearest Neighbors) para decisão.
    Encontra objetivos usando célula mais próxima conhecida.
    Implementa: KNN puro, KNN com peso, KNN ponderado.
    """

    def __init__(self, nome, mapa, memoria_grupo, grupo_id=0, k=3, algoritmos=None):
        super().__init__(nome, mapa, memoria_grupo, grupo_id)
        self.k = k
        self.algoritmos_disponiveis = algoritmos or ["knn_puro", "knn_peso", "knn_ponderado"]
        self.indice_algoritmo_atual = 0

    def _decidir_acao_interna(self):
        """Decide ação usando KNN"""
        algoritmo = self.algoritmos_disponiveis[self.indice_algoritmo_atual]
        self.algoritmo_em_uso = algoritmo

        if algoritmo == "knn_puro":
            return self._knn_puro()
        elif algoritmo == "knn_peso":
            return self._knn_peso()
        elif algoritmo == "knn_ponderado":
            return self._knn_ponderado()

        return self._knn_puro()

    def _knn_puro(self):
        """
        KNN simples: encontra K tesouros mais próximos e vai para o mais próximo.
        """
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        if not tesouros:
            return self._acao_aleatoria()

        # Encontra K tesouros mais próximos
        distancias = [(t, self._distancia_manhattan(t)) for t in tesouros]
        k_proximos = sorted(distancias, key=lambda x: x[1])[:self.k]

        if k_proximos:
            objetivo = k_proximos[0][0]  # Mais próximo
            return self._mover_para(objetivo)

        return self._acao_aleatoria()

    def _knn_peso(self):
        """
        KNN com peso: média ponderada pelos K mais próximos.
        """
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        if not tesouros:
            return self._acao_aleatoria()

        distancias = [(t, self._distancia_manhattan(t)) for t in tesouros]
        k_proximos = sorted(distancias, key=lambda x: x[1])[:self.k]

        if not k_proximos:
            return self._acao_aleatoria()

        # Calcula média ponderada invertida por distância
        soma_pesos = sum(1 / (d + 1) for _, d in k_proximos)
        x_medio = sum((t[0] / (d + 1)) for t, d in k_proximos) / soma_pesos
        y_medio = sum((t[1] / (d + 1)) for t, d in k_proximos) / soma_pesos

        objetivo = (int(round(x_medio)), int(round(y_medio)))
        return self._mover_para(objetivo)

    def _knn_ponderado(self):
        """
        KNN com peso gaussiano: maior peso aos mais próximos.
        """
        import math
        tesouros = self.memoria_grupo.obter_tesouros(self.grupo_id)
        
        if not tesouros:
            return self._acao_aleatoria()

        distancias = [(t, self._distancia_manhattan(t)) for t in tesouros]
        k_proximos = sorted(distancias, key=lambda x: x[1])[:self.k]

        if not k_proximos:
            return self._acao_aleatoria()

        # Pesos gaussianos
        soma_pesos = 0
        x_medio = 0
        y_medio = 0

        for t, d in k_proximos:
            peso = math.exp(-(d ** 2) / (2 * self.k ** 2))
            soma_pesos += peso
            x_medio += t[0] * peso
            y_medio += t[1] * peso

        if soma_pesos > 0:
            x_medio /= soma_pesos
            y_medio /= soma_pesos
            objetivo = (int(round(x_medio)), int(round(y_medio)))
            return self._mover_para(objetivo)

        return self._acao_aleatoria()

    def _mover_para(self, objetivo):
        """Move uma unidade em direção ao objetivo"""
        x_obj, y_obj = objetivo
        
        if x_obj < self.x:
            return "CIMA"
        elif x_obj > self.x:
            return "BAIXO"
        elif y_obj < self.y:
            return "ESQUERDA"
        elif y_obj > self.y:
            return "DIREITA"
        
        return self._acao_aleatoria()

    def _distancia_manhattan(self, ponto):
        """Calcula distância Manhattan"""
        return abs(ponto[0] - self.x) + abs(ponto[1] - self.y)

    def _acao_aleatoria(self):
        """Ação aleatória"""
        acoes = ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]
        return random.choice(acoes)
