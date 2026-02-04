"""
Módulo de manutenção de mapas.
Garante que todos os mapas gerados sejam válidos antes de usar.
"""
from .gerador_de_mapa import GeradorDeMapa, Mapa
from .validador import ValidadorMapa
from utils.constantes import ModoJogo


class GeradorMapaValido:
    """Gera mapas garantindo que sejam válidos no primeiro giro"""

    def __init__(self, tamanho=10, modo=ModoJogo.A_TESOUROS, max_tentativas=50):
        """
        Args:
            tamanho: Dimensão do mapa
            modo: Modo de jogo
            max_tentativas: Quantas vezes tentar gerar antes de falhar
        """
        self.tamanho = tamanho
        self.modo = modo
        self.max_tentativas = max_tentativas

    def gerar(self):
        """
        Gera um mapa válido.
        
        Returns:
            Tupla (mapa: Mapa, válido: bool, mensagem: str)
        """
        for tentativa in range(self.max_tentativas):
            # Gera mapa candidato
            gerador = GeradorDeMapa(self.tamanho, self.modo)
            matriz = gerador.gerar()

            # Valida
            validador = ValidadorMapa(matriz, self.tamanho, self.modo)
            valido, mensagem = validador.validar()

            if valido:
                # Cria objeto Mapa com a matriz
                mapa = Mapa(self.tamanho, self.modo)
                mapa.matriz = matriz
                return mapa, True, f"Mapa gerado e validado (tentativa {tentativa + 1})"

        # Falhou em todas as tentativas
        return None, False, f"Falha ao gerar mapa válido após {self.max_tentativas} tentativas"

    def gerar_com_relatorio(self):
        """Gera mapa e retorna relatório detalhado"""
        mapa, valido, mensagem = self.gerar()

        if not valido:
            return None, {"sucesso": False, "mensagem": mensagem}

        validador = ValidadorMapa(mapa.matriz, self.tamanho, self.modo)
        relatorio = validador.obter_relatorio()
        relatorio["sucesso"] = True
        relatorio["mensagem"] = mensagem

        return mapa, relatorio
