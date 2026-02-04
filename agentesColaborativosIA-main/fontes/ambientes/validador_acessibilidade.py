"""
Validador de acessibilidade de mapa usando flood fill.
Garante que todas as células importantes (bandeira, tesouros) são acessíveis a partir de (0,0).
"""


class ValidadorAcessibilidade:
    """Valida a acessibilidade de um mapa usando flood fill"""

    def __init__(self, mapa):
        """
        Args:
            mapa: Objeto Mapa com matriz de células
        """
        self.mapa = mapa
        self.tamanho = mapa.tamanho

    def validar(self):
        """
        Valida se todas as células não-bomba são acessíveis a partir de (0,0).
        
        Returns:
            Dicionário com resultados:
            {
                "valido": bool,
                "acessiveis": set de posições acessíveis,
                "inacessiveis": set de posições não acessíveis (que não são bombas)
            }
        """
        # Encontra todas as células acessíveis a partir de (0,0)
        acessiveis = self._flood_fill((0, 0))
        
        # Encontra células inacessíveis que não são bombas
        inacessiveis = set()
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                celula = self.mapa.ver((i, j))
                # Se não é bomba e não é acessível, é problema
                if celula != "B" and (i, j) not in acessiveis:
                    inacessiveis.add((i, j))
        
        resultado = {
            "valido": len(inacessiveis) == 0,
            "acessiveis": acessiveis,
            "inacessiveis": inacessiveis,
            "total_acessiveis": len(acessiveis),
            "total_inacessiveis": len(inacessiveis)
        }
        
        return resultado

    def _flood_fill(self, inicio):
        """
        Executa flood fill a partir de uma posição.
        Explora todas as células acessíveis (não-bombas).
        
        Args:
            inicio: Tupla (x, y) de início
            
        Returns:
            Set de posições acessíveis
        """
        visitadas = set()
        fila = [inicio]
        
        while fila:
            pos = fila.pop(0)
            if pos in visitadas:
                continue
            
            x, y = pos
            
            # Valida coordenadas
            if not self._pos_valida(x, y):
                continue
            
            # Se é bomba, não segue por aqui
            if self.mapa.ver(pos) == "B":
                continue
            
            # Marca como visitada
            visitadas.add(pos)
            
            # Explora vizinhos (4 direções)
            vizinhos = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]
            
            for vizinho in vizinhos:
                if vizinho not in visitadas:
                    fila.append(vizinho)
        
        return visitadas

    def _pos_valida(self, x, y):
        """Valida se posição está dentro do mapa"""
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    def garantir_acessibilidade(self, mapa_obj):
        """
        Tenta garantir acessibilidade regenerando mapa se necessário.
        Tenta até 10 vezes.
        
        Args:
            mapa_obj: Objeto Mapa
            
        Returns:
            True se conseguiu criar mapa acessível, False senão
        """
        for tentativa in range(10):
            mapa_obj.regenerar()
            resultado = self.validar()
            if resultado["valido"]:
                return True
        
        return False
