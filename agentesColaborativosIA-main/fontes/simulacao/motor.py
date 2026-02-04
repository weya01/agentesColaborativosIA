"""
Motor de simulação para coordenar múltiplas simulações.
Gerencia turnos, verificação de objetivos e coleta de resultados.
"""


class MotorSimulacao:
    """Coordena a execução de uma simulação completa"""

    def __init__(self, mapa, agentes, memoria, modo="A", max_turnos=500, grupo_id=0):
        """
        Args:
            mapa: Objeto Mapa
            agentes: Lista de agentes
            memoria: Memória partilhada
            modo: Modo de jogo (A/B/C)
            max_turnos: Máximo de turnos permitidos
            grupo_id: ID do grupo de agentes
        """
        self.mapa = mapa
        self.agentes = agentes
        self.memoria = memoria
        self.modo = modo
        self.grupo_id = grupo_id
        self.turno_atual = 0
        self.max_turnos = max_turnos
        self.objetivo_alcancado = False

    def executar(self):
        """Executa simulação completa até objetivo ou limite"""
        while not self._fim():
            self.executar_um_turno()
        
        return self._coletar_resultados()

    def executar_um_turno(self):
        """Executa um turno para todos os agentes"""
        self.turno_atual += 1
        
        # Cada agente executa seu turno
        for agente in self.agentes:
            if agente.estado.value == "ativo":
                agente.executar_turno()
        
        # Verifica se objetivo foi alcançado
        if self._verificar_objetivo():
            self.objetivo_alcancado = True

    def verificar_objetivo_rapido(self):
        """
        Verifica objetivo de forma rápida (para UI).
        Retorna True se objetivo foi alcançado.
        """
        return self._verificar_objetivo()

    def _verificar_objetivo(self):
        """
        Verifica se objetivo foi alcançado segundo o modo.
        
        MODO A (Tesouros): >50% (não >=) dos tesouros DESCOBERTOS devem ser coletados
        MODO B (Sobrevivência): >80% das células exploradas
        MODO C (Bandeira): Bandeira encontrada
        """
        if self.modo == "A":
            return self._verificar_modo_a()
        elif self.modo == "B":
            return self._verificar_modo_b()
        elif self.modo == "C":
            return self._verificar_modo_c()
        
        return False

    def _verificar_modo_a(self):
        """
        MODO A: Coletar >50% dos tesouros DESCOBERTOS
        (não da população total)
        """
        # Tesouros descobertos = na memória do grupo
        tesouros_descobertos = len(self.memoria.obter_tesouros(grupo_id=self.grupo_id))
        
        if tesouros_descobertos == 0:
            # Sem tesouros descobertos, não pode completar
            return False
        
        # Tesouros coletados
        tesouros_coletados = self.memoria.obter_tesouros_coletados(grupo_id=self.grupo_id)
        
        # > 50% (não >=)
        limiar = tesouros_descobertos * 0.5
        return tesouros_coletados > limiar

    def _verificar_modo_b(self):
        """
        MODO B: Explorar >80% das células E pelo menos 1 agente vivo
        """
        # Verifica se há agentes vivos
        agentes_vivos = [ag for ag in self.agentes if ag.estado.value == "ativo"]
        if not agentes_vivos:
            return False
        
        # Explora células através da memória do grupo
        explorados = len(self.memoria.obter_exploradas(grupo_id=self.grupo_id))
        total = self.mapa.tamanho * self.mapa.tamanho
        limiar = total * 0.8
        
        return explorados > limiar

    def _verificar_modo_c(self):
        """
        MODO C: Encontrar e chegar à bandeira
        Qualquer agente que chegue à bandeira completa a missão.
        """
        # Verifica se algum agente chegou ao objetivo (bandeira)
        for agente in self.agentes:
            if agente.chegou_objetivo:
                return True
        
        # Também verifica pela memória (bandeira descoberta)
        bandeira = self.memoria.obter_bandeira(grupo_id=self.grupo_id)
        return bandeira is not None and len(bandeira) > 0

    def _contar_tesouros_mapa(self):
        """Conta total de tesouros no mapa"""
        count = 0
        for i in range(self.mapa.tamanho):
            for j in range(self.mapa.tamanho):
                if self.mapa.ver((i, j)) == "T":
                    count += 1
        return count

    def _get_celulas_exploradas_grupo(self):
        """Retorna conjunto de células exploradas por todos os agentes"""
        exploradas = set()
        for agente in self.agentes:
            exploradas.update(agente.celulas_exploradas)
        return exploradas

    def _fim(self):
        """Verifica se simulação deve terminar"""
        # Termina se objetivo alcançado
        if self.objetivo_alcancado:
            return True
        
        # Termina se todos os agentes morreu ou completaram
        if all(ag.estado.value != "ativo" for ag in self.agentes):
            return True
        
        # Termina se estourou limite de turnos
        if self.turno_atual >= self.max_turnos:
            return True
        
        return False

    def _coletar_resultados(self):
        """Coleta métricas finais de todos os agentes"""
        resultados = {
            "turno_final": self.turno_atual,
            "objetivo_alcancado": self.objetivo_alcancado,
            "modo": self.modo,
            "agentes": {}
        }
        
        for agente in self.agentes:
            resultados["agentes"][agente.nome] = agente.obter_metricas()
        
        return resultados
