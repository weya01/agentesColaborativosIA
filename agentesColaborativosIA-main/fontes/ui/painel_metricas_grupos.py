"""
Painel de métricas de grupos de agentes.
Mostra comparação de desempenho entre grupos.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QTabWidget, QLabel, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor


class PainelMetricasGrupos(QWidget):
    """Painel para visualizar métricas e comparação de grupos"""
    
    def __init__(self):
        super().__init__()
        self.gestor_grupos = None
        self._criar_ui()
    
    def _criar_ui(self):
        """Cria interface do painel"""
        layout = QVBoxLayout(self)
        
        # Abas para diferentes visualizações
        tabs = QTabWidget()
        
        # Aba 1: Resumo de grupos
        self.tabela_grupos = QTableWidget()
        self.tabela_grupos.setColumnCount(4)
        self.tabela_grupos.setHorizontalHeaderLabels(
            ["Grupo", "Tipo", "Tipos de Agentes", "Total de Agentes"]
        )
        tabs.addTab(self.tabela_grupos, "Grupos")
        
        # Aba 2: Comparação de desempenho
        self.tabela_comparacao = QTableWidget()
        self.tabela_comparacao.setColumnCount(9)
        self.tabela_comparacao.setHorizontalHeaderLabels([
            "Grupo", "Ativos", "Mortos", "Passos (Total)",
            "Passos (Médio)", "Bombas", "Tesouros", "Células Exploradas", "Eficiência"
        ])
        tabs.addTab(self.tabela_comparacao, "Desempenho")
        
        # Aba 3: Métricas detalhadas por grupo
        self.tabela_detalhes = QTableWidget()
        self.tabela_detalhes.setColumnCount(9)
        self.tabela_detalhes.setHorizontalHeaderLabels([
            "Grupo", "Métrica", "Valor Total", "Valor Médio", 
            "Mínimo", "Máximo", "Desvio", "Status", "Observações"
        ])
        tabs.addTab(self.tabela_detalhes, "Detalhes")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def atualizar_metricas(self, gestor_grupos):
        """Atualiza métricas com dados do gestor"""
        self.gestor_grupos = gestor_grupos
        
        self._atualizar_tabela_grupos()
        self._atualizar_comparacao()
        self._atualizar_detalhes()
    
    def _atualizar_tabela_grupos(self):
        """Atualiza tabela com resumo de grupos"""
        grupos = self.gestor_grupos.listar_grupos()
        self.tabela_grupos.setRowCount(len(grupos))
        
        for row, (grupo_id, config) in enumerate(grupos):
            agentes = self.gestor_grupos.obter_agentes_grupo(grupo_id)
            
            self.tabela_grupos.setItem(row, 0, 
                QTableWidgetItem(config.nome))
            self.tabela_grupos.setItem(row, 1, 
                QTableWidgetItem(config.tipo.value))
            self.tabela_grupos.setItem(row, 2, 
                QTableWidgetItem(", ".join(config.tipos_agentes)))
            self.tabela_grupos.setItem(row, 3, 
                QTableWidgetItem(str(len(agentes))))
    
    def _atualizar_comparacao(self):
        """Atualiza tabela de comparação de desempenho"""
        comparacao = self.gestor_grupos.obter_comparacao_grupos()
        self.tabela_comparacao.setRowCount(len(comparacao))
        
        for row, (nome_grupo, dados) in enumerate(comparacao.items()):
            metricas = dados['metricas']
            
            self.tabela_comparacao.setItem(row, 0, 
                QTableWidgetItem(nome_grupo))
            self.tabela_comparacao.setItem(row, 1, 
                QTableWidgetItem(str(metricas['agentes_ativos'])))
            self.tabela_comparacao.setItem(row, 2, 
                QTableWidgetItem(str(metricas['agentes_mortos'])))
            self.tabela_comparacao.setItem(row, 3, 
                QTableWidgetItem(str(metricas['passos_total'])))
            self.tabela_comparacao.setItem(row, 4, 
                QTableWidgetItem(f"{metricas['passos_medio']:.1f}"))
            self.tabela_comparacao.setItem(row, 5, 
                QTableWidgetItem(str(metricas['bombas_acionadas_total'])))
            self.tabela_comparacao.setItem(row, 6, 
                QTableWidgetItem(str(metricas['tesouros_coletados_total'])))
            self.tabela_comparacao.setItem(row, 7, 
                QTableWidgetItem(str(metricas['celulas_exploradas_total'])))
            
            # Calcula eficiência
            if metricas['passos_total'] > 0:
                eficiencia = metricas['tesouros_coletados_total'] / metricas['passos_total']
            else:
                eficiencia = 0
            self.tabela_comparacao.setItem(row, 8, 
                QTableWidgetItem(f"{eficiencia:.3f}"))
    
    def _atualizar_detalhes(self):
        """Atualiza tabela de detalhes por grupo"""
        # Por enquanto, apenas preenche com resumo
        # Pode ser expandido para análises estatísticas
        grupos = self.gestor_grupos.listar_grupos()
        self.tabela_detalhes.setRowCount(len(grupos))
        
        for row, (grupo_id, config) in enumerate(grupos):
            metricas = self.gestor_grupos.obter_metricas_grupo(grupo_id)
            
            self.tabela_detalhes.setItem(row, 0, 
                QTableWidgetItem(config.nome))
            self.tabela_detalhes.setItem(row, 1, 
                QTableWidgetItem("Geral"))
            self.tabela_detalhes.setItem(row, 2, 
                QTableWidgetItem(str(metricas.get('passos_total', 0))))
            self.tabela_detalhes.setItem(row, 3, 
                QTableWidgetItem(f"{metricas.get('passos_medio', 0):.1f}"))
            
            agentes = self.gestor_grupos.obter_agentes_grupo(grupo_id)
            if agentes:
                passos_min = min(a.passos for a in agentes)
                passos_max = max(a.passos for a in agentes)
                self.tabela_detalhes.setItem(row, 4, 
                    QTableWidgetItem(str(passos_min)))
                self.tabela_detalhes.setItem(row, 5, 
                    QTableWidgetItem(str(passos_max)))
            
            status = "Ativo" if metricas.get('agentes_ativos', 0) > 0 else "Completo"
            self.tabela_detalhes.setItem(row, 7, 
                QTableWidgetItem(status))
