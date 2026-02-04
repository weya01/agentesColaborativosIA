"""
Janela principal - Versão nova multi-grupo.
Redireciona para janela_principal_multi_grupo.
"""

from .janela_principal_multi_grupo import JanelaPrincipalMultiGrupo as JanelaPrincipal

__all__ = ['JanelaPrincipal']


        # Reseta UI
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.setText("⏸ Pausar")
        self.combo_abordagem.setEnabled(True)
        self.combo_tipo.setEnabled(False)  # Sempre desabilitado
        self.spin_agentes.setEnabled(True)
        self.label_turno.setText("Turno: 0")
        self.texto_resumo.clear()
        self.tabela_agentes.setRowCount(0)
        self.texto_detalhes.clear()

    def atualizar_turno(self):
        """Executa um turno da simulação"""
        if not self.simulacao_ativa or not self.agentes:
            return

        # Executa turno para cada agente
        for agente in self.agentes:
            if agente.estado != EstadoAgente.MORTO:
                agente.executar_turno()

        self.turno_atual += 1

        # Atualiza visualização do mapa com memória do grupo
        if self.grid_mapa and self.memoria:
            self.grid_mapa.atualizar(self.agentes, grupo_id=0)

        # Verifica objetivo
        objetivo_alcancado = self._verificar_objetivo()

        # Atualiza UI
        self._atualizar_metricas()

        if objetivo_alcancado:
            self.timer.stop()
            self.simulacao_ativa = False
            self.btn_exportar.setEnabled(True)
            self.label_turno.setText(f"Turno: {self.turno_atual} - ✓ OBJETIVO ALCANÇADO!")

    def _verificar_objetivo(self):
        """Verifica se objetivo foi alcançado usando o MotorSimulacao"""
        if not self.motor:
            return False
        
        # Delega verificação para o motor (lógica centralizada)
        return self.motor.verificar_objetivo_rapido()

    def _atualizar_metricas(self):
        """Atualiza display de métricas"""
        grupo = self.gestor_metricas.obter_grupo(0)
        grupo.avanca_turno()

        # Atualiza label de turno
        self.label_turno.setText(f"Turno: {self.turno_atual}")

        # Atualiza tabela de agentes
        self.tabela_agentes.setRowCount(len(self.agentes))
        for i, agente in enumerate(self.agentes):
            metrics = agente.obter_metricas()
            self.tabela_agentes.setItem(i, 0, QTableWidgetItem(agente.id))
            self.tabela_agentes.setItem(i, 1, QTableWidgetItem(metrics["tipo"]))
            self.tabela_agentes.setItem(i, 2, QTableWidgetItem(
                "VIVO" if agente.estado != EstadoAgente.MORTO else "MORTO"
            ))
            self.tabela_agentes.setItem(i, 3, QTableWidgetItem(str(metrics["passos"])))
            self.tabela_agentes.setItem(i, 4, QTableWidgetItem(str(metrics["tesouros"])))
            self.tabela_agentes.setItem(i, 5, QTableWidgetItem(f"{metrics['eficiencia']:.2f}"))

        # Atualiza métricas de grupos (NOVO)
        if hasattr(self, 'gestor_grupos'):
            self.painel_grupos.atualizar_metricas(self.gestor_grupos)

        # Atualiza resumo
        resumo = f"""SIMULAÇÃO - TURNO {self.turno_atual}
            
Tesouros coletados: {grupo.obter_tesouros_coletados()}
Células exploradas: {grupo.obter_celulas_exploradas()}
Cobertura do mapa: {grupo.obter_cobertura_mapa():.1f}%
Agentes vivos: {grupo.obter_agentes_vivos()}
Agentes mortos: {grupo.obter_agentes_mortos()}
Taxa mortalidade: {grupo.obter_taxa_mortalidade():.1f}%
Eficiência exploração: {grupo.obter_eficiencia_exploracao():.2f}
        """
        self.texto_resumo.setText(resumo)

        # Atualiza progresso
        cobertura = grupo.obter_cobertura_mapa()
        self.progresso.setValue(int(cobertura))

    def exportar_metricas(self):
        """Exporta métricas da simulação"""
        if self.gestor_metricas:
            resultado = self.gestor_metricas.salvar_relatorios("ultima_simulacao")
            self.texto_detalhes.setText(
                f"Métricas exportadas com sucesso!\n\n"
                f"Relatórios: {resultado['relatorios']}\n"
                f"Comparação: {resultado['comparacao']}"
            )
