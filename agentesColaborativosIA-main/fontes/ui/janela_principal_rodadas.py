"""
Janela Principal - Sistema de Rodadas Progressivas.

Características:
- Separação clara: Rodadas (progressão 2→10 agentes)
- Todos os grupos começam com mesmo número de agentes
- Grupos não se influenciam (ambientes isolados)
- Interface limpa: seletor de abordagem único
- Métricas claras e detalhadas por rodada
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QGroupBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QSpinBox,
    QFrame, QCheckBox, QScrollArea
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QColor

from .grid_mapa import GridMapa
from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from agentes.base.agente_base import EstadoAgente
from metricas import GestorMetricas
from utils.constantes import ModoJogo


class JanelaPrincipalRodadas(QWidget):
    """Janela com sistema de rodadas progressivas"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulação Multi-Agentes - Sistema de Rodadas Progressivas v2.0")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background-color: white;")

        # Estado interno
        self.gerenciador = GerenciadorGrupos()
        self.grid_mapa = None
        self.turno_atual = 0
        self.rodada_atual = 1  # NOVA: Rastreamento de rodadas
        self.simulacao_ativa = False
        self.abordagem_selecionada = 0
        
        # Gestor de métricas: {abordagem_id: {grupo_id: GestorMetricas}}
        self.gestores_metricas = {}
        self.resultados_rodadas = {}  # {rodada: {abordagem_id: {grupo_id: resultado}}}
        self.tabs_grupos = {}  # {grupo_id: painel}
        
        # Sistema de escalamento progressivo
        self.rodada_atual = 1
        self.num_agentes_atual = 2
        self.percentagem_bombas_atual = 50.0
        self.grupos_completados_nesta_rodada = 0
        self.grupos_totais_nesta_rodada = 0
        self.abordagens_selecionadas = []  # Quais abordagens foram selecionadas
        
        # Cores para grupos (10 cores distintas)
        self.cores_grupos = [
            "#FF4444", "#4444FF", "#44FF44", "#FFAA00",
            "#FF44FF", "#00CCAA", "#FF8800", "#0088FF",
            "#AAFF00", "#FF0088"
        ]
        
        # Timer para atualização visual
        self.timer = QTimer()
        self.timer.timeout.connect(self.executar_turno)

        # Build UI
        self._criar_ui()

    def _criar_ui(self):
        """Cria interface do usuário"""
        layout_principal = QHBoxLayout()

        # ========== PAINEL ESQUERDO - CONTROLES ==========
        painel_controles = self._criar_painel_controles()
        layout_principal.addWidget(painel_controles, 1)

        # ========== PAINEL CENTRAL - SIMULAÇÃO ==========
        painel_central = self._criar_painel_central()
        layout_principal.addLayout(painel_central, 2)

        # ========== PAINEL DIREITO - MÉTRICAS ==========
        painel_metricas = self._criar_painel_metricas()
        layout_principal.addWidget(painel_metricas, 1)

        self.setLayout(layout_principal)

    def _criar_painel_controles(self):
        """Cria painel de controles"""
        grupo = QGroupBox("⚙️ CONTROLES DE SIMULAÇÃO")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #222; border: 2px solid #2196F3; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        layout = QVBoxLayout()

        # COMBO DE ABORDAGENS (IGUAL A VELOCIDADE)
        layout.addWidget(QLabel("📋 Abordagem:"))
        self.combo_abordagem = QComboBox()
        self.combo_abordagem.addItems(["A: Tesouros", "B: Sobrevivência", "C: Bandeira"])
        self.combo_abordagem.setCurrentIndex(0)
        self.combo_abordagem.setStyleSheet("color: #222; background: white; border: 1px solid #ccc; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.combo_abordagem)

        # Velocidade
        layout.addSpacing(15)
        layout.addWidget(QLabel("⚡ Velocidade (ms/turno):"))
        self.combo_velocidade = QComboBox()
        self.combo_velocidade.addItems([
            "0ms (Máximo)", "100ms (Rápido)", "200ms (Normal)", 
            "500ms (Lento)", "1000ms (Muito Lento)"
        ])
        self.combo_velocidade.setCurrentIndex(2)
        self.combo_velocidade.setStyleSheet("color: #222; background: white; border: 1px solid #ccc; padding: 5px; border-radius: 3px;")
        layout.addWidget(self.combo_velocidade)

        # Botões principais
        layout.addSpacing(15)
        self.btn_iniciar = QPushButton("▶ INICIAR SIMULAÇÃO")
        self.btn_iniciar.clicked.connect(self.iniciar_simulacao)
        self.btn_iniciar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                font-weight: bold;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3d8b40; }
        """)
        self.btn_iniciar.setMinimumHeight(45)
        layout.addWidget(self.btn_iniciar)

        self.btn_pausar = QPushButton("⏸ PAUSAR")
        self.btn_pausar.clicked.connect(self.pausar_simulacao)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:enabled:hover { background-color: #e68900; }
        """)
        layout.addWidget(self.btn_pausar)

        self.btn_resetar = QPushButton("🔄 RESETAR")
        self.btn_resetar.clicked.connect(self.resetar_simulacao)
        self.btn_resetar.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #da190b; }
        """)
        layout.addWidget(self.btn_resetar)

        # Info legenda
        legenda = """
CORES POR GRUPO:
━━━━━━━━━━━━━━━━
Cada grupo tem cor única
no mapa para fácil
identificação.

SISTEMA DE RODADAS:
━━━━━━━━━━━━━━━━
Rodada 1: 2 agentes (50% bombas)
Rodada 2: 3 agentes (53.75% bombas)
...
Rodada 9: 10 agentes (80% bombas)

Grupos progridem juntos.
        """
        label_legenda = QLabel(legenda)
        label_legenda.setFont(QFont("Courier", 8))
        label_legenda.setStyleSheet("""
            background: #f0f8ff;
            color: #333;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #2196F3;
        """)
        layout.addWidget(label_legenda)

        layout.addStretch()
        grupo.setLayout(layout)
        return grupo

    def _criar_painel_central(self):
        """Cria painel central com mapa e info"""
        layout = QVBoxLayout()

        # Status da simulação
        self.label_status = QLabel("⏳ Aguardando inicialização...")
        self.label_status.setFont(QFont("Arial", 12, QFont.Bold))
        self.label_status.setStyleSheet("color: white; background: #1976D2; padding: 12px; border-radius: 5px; font-weight: bold;")
        layout.addWidget(self.label_status)

        # Info de rodada e turno
        info_rodada = QHBoxLayout()
        self.label_rodada = QLabel("📍 Rodada: 1/9 | Agentes: 2 | Bombas: 50%")
        self.label_rodada.setFont(QFont("Arial", 11, QFont.Bold))
        self.label_rodada.setStyleSheet("color: #222;")
        self.label_turno = QLabel("⏱️ Turno: 0")
        self.label_turno.setFont(QFont("Arial", 11, QFont.Bold))
        self.label_turno.setStyleSheet("color: #222;")
        info_rodada.addWidget(self.label_rodada)
        info_rodada.addStretch()
        info_rodada.addWidget(self.label_turno)
        layout.addLayout(info_rodada)

        # Grid do mapa
        layout_mapa = QVBoxLayout()
        layout_mapa.addStretch()
        
        self.container_grid = QWidget()
        self.layout_container = QVBoxLayout()
        self.layout_container.addWidget(QLabel("🗺️ Mapa será exibido aqui..."))
        self.layout_container.setContentsMargins(0, 0, 0, 0)
        self.layout_container.setSpacing(0)
        self.container_grid.setLayout(self.layout_container)
        self.container_grid.setMinimumSize(500, 500)
        self.container_grid.setMaximumSize(600, 600)
        self.container_grid.setStyleSheet("background: white; border: 2px solid #2196F3; border-radius: 5px;")
        
        layout_mapa.addWidget(self.container_grid, alignment=Qt.AlignCenter)
        layout_mapa.addStretch()
        
        layout.addLayout(layout_mapa)

        return layout

    def _criar_painel_metricas(self):
        """Cria painel de métricas com auto-display"""
        grupo = QGroupBox("📊 MÉTRICAS POR GRUPO")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #222; border: 2px solid #2196F3; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        layout = QVBoxLayout()

        # NOTA: SEM SELETOR AQUI - MÉTRICAS ATUALIZAM AUTOMATICAMENTE
        layout.addWidget(QLabel("📌 Abordagem:"))
        self.label_abordagem_atual = QLabel("Nenhuma")
        self.label_abordagem_atual.setStyleSheet("color: #222; font-weight: bold; font-size: 11px;")
        layout.addWidget(self.label_abordagem_atual)

        # Abas para grupos
        self.tabs_metricas = QTabWidget()
        self.tabs_metricas.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ddd; }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 8px 15px;
                border: 1px solid #ddd;
                color: #222;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 3px solid #2196F3;
                font-weight: bold;
            }
        """)
        
        widget_vazio = QWidget()
        layout_vazio = QVBoxLayout()
        label_aguarda = QLabel("Abas aparecerão após iniciar simulação")
        label_aguarda.setStyleSheet("color: #666;")
        layout_vazio.addWidget(label_aguarda)
        widget_vazio.setLayout(layout_vazio)
        self.tabs_metricas.addTab(widget_vazio, "Aguardando...")
        
        layout.addWidget(self.tabs_metricas)
        grupo.setLayout(layout)
        return grupo

    def _criar_painel_grupo(self, grupo_id, abordagem_id, grupo_numero):
        """Cria painel de métricas para um grupo (grupo_numero começa em 1, não 0)"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Cabeçalho com cor
        cor_hex = self.cores_grupos[grupo_numero % len(self.cores_grupos)]
        titulo = QLabel(f"Grupo {grupo_numero}")  # AQUI: Começa em 1
        titulo.setStyleSheet(f"""
            background-color: {cor_hex};
            color: white;
            font-weight: bold;
            font-size: 13px;
            padding: 10px;
            border-radius: 5px;
        """)
        layout.addWidget(titulo)

        # Labels para métricas (contraste melhorado)
        label_objetivo = QLabel("Objetivo: -")
        label_objetivo.setFont(QFont("Arial", 10, QFont.Bold))
        label_objetivo.setStyleSheet("color: #222; padding: 3px;")
        
        label_turno_grupo = QLabel("Turno: 0")
        label_turno_grupo.setStyleSheet("color: #333; padding: 3px;")
        
        label_explorado = QLabel("Explorado: 0%")
        label_explorado.setStyleSheet("color: #333; padding: 3px;")
        
        label_mortalidade = QLabel("Mortalidade: 0%")
        label_mortalidade.setStyleSheet("color: #333; padding: 3px;")
        
        label_eficiencia = QLabel("Eficiência: 0.0")
        label_eficiencia.setStyleSheet("color: #333; padding: 3px;")
        
        layout.addWidget(label_objetivo)
        layout.addWidget(label_turno_grupo)
        layout.addWidget(label_explorado)
        layout.addWidget(label_mortalidade)
        layout.addWidget(label_eficiencia)

        # Tabela de agentes
        tabela_agentes = QTableWidget()
        tabela_agentes.setColumnCount(6)
        tabela_agentes.setHorizontalHeaderLabels([
            "ID", "Tipo", "Status", "Passos", "Tesouros", "Efic."
        ])
        tabela_agentes.setMaximumHeight(200)
        tabela_agentes.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #eee;
                background: white;
                color: #222;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #222;
                font-weight: bold;
                padding: 5px;
                border: none;
            }
            QTableWidget::item {
                padding: 3px;
                color: #222;
                border: none;
                border-right: 1px solid #eee;
            }
        """)
        layout.addWidget(QLabel("👥 Agentes:"))
        layout.addWidget(tabela_agentes)

        layout.addStretch()
        widget.setLayout(layout)

        # Armazena referências
        widget.label_objetivo = label_objetivo
        widget.label_turno_grupo = label_turno_grupo
        widget.label_explorado = label_explorado
        widget.label_mortalidade = label_mortalidade
        widget.label_eficiencia = label_eficiencia
        widget.tabela_agentes = tabela_agentes
        widget.abordagem_id = abordagem_id
        widget.grupo_id = grupo_id
        widget.cor_hex = cor_hex
        widget.numero_grupo = grupo_numero

        return widget

    def _criar_aba_resumo_geral(self):
        """Cria aba com resumo geral e comparação de algoritmos"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel(f"📊 RESUMO GERAL - RODADA {self.rodada_atual}/9")
        titulo.setStyleSheet("font-weight: bold; font-size: 14px; color: #222; padding: 10px;")
        layout.addWidget(titulo)
        
        # Tabela de resumo por grupo
        tabela_resumo = QTableWidget()
        tabela_resumo.setColumnCount(7)
        tabela_resumo.setHorizontalHeaderLabels([
            "Grupo", "Abordagem", "Algoritmo", "Explorado", "Vivos", "Objetivos", "Eficiência"
        ])
        tabela_resumo.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #eee;
                border: 1px solid #ddd;
                color: #222;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
        tabela_resumo.setMaximumHeight(250)
        
        # Preencher tabela
        rodada = self.resultados_rodadas.get(self.rodada_atual, {})
        nomes_abord = {0: 'Tesouros', 1: 'Sobrevivência', 2: 'Bandeira'}
        row = 0
        
        for abordagem_id in self.abordagens_selecionadas:
            grupos_abordagem = rodada.get(abordagem_id, {})
            
            for grupo_id, info in grupos_abordagem.items():
                numero = info["grupo_numero"]
                abordagem_nome = nomes_abord.get(abordagem_id, "Desconhecida")
                algoritmo = info.get("algoritmo_em_uso", "N/A")
                explorado = info.get("explorado_pct", 0)
                vivos = info.get("agentes_vivos", 0)
                objetivos = "✅" if info.get("objetivo_alcancado", False) else "❌"
                eficiencia = info.get("eficiencia", 0.0)
                
                tabela_resumo.insertRow(row)
                tabela_resumo.setItem(row, 0, QTableWidgetItem(f"G{numero}"))
                tabela_resumo.setItem(row, 1, QTableWidgetItem(abordagem_nome))
                tabela_resumo.setItem(row, 2, QTableWidgetItem(str(algoritmo)))
                tabela_resumo.setItem(row, 3, QTableWidgetItem(f"{explorado:.1f}%"))
                tabela_resumo.setItem(row, 4, QTableWidgetItem(str(vivos)))
                tabela_resumo.setItem(row, 5, QTableWidgetItem(objetivos))
                tabela_resumo.setItem(row, 6, QTableWidgetItem(f"{eficiencia:.2f}"))
                row += 1
        
        layout.addWidget(QLabel("📋 Métricas por Grupo:"))
        layout.addWidget(tabela_resumo)
        
        # Tabela de comparação de algoritmos
        layout.addWidget(QLabel("🔀 Comparação de Algoritmos:"))
        tabela_algoritmos = QTableWidget()
        tabela_algoritmos.setColumnCount(5)
        tabela_algoritmos.setHorizontalHeaderLabels([
            "Algoritmo", "Usos", "Sucessos", "Taxa Sucesso", "Efic. Média"
        ])
        tabela_algoritmos.setStyleSheet(tabela_resumo.styleSheet())
        tabela_algoritmos.setMaximumHeight(200)
        
        # Agregar dados por algoritmo
        stats_algoritmo = {}
        for abordagem_id in self.abordagens_selecionadas:
            grupos_abordagem = rodada.get(abordagem_id, {})
            for grupo_id, info in grupos_abordagem.items():
                algoritmo = info.get("algoritmo_em_uso", "N/A")
                if algoritmo not in stats_algoritmo:
                    stats_algoritmo[algoritmo] = {"usos": 0, "sucessos": 0, "eficiencias": []}
                
                stats_algoritmo[algoritmo]["usos"] += 1
                if info.get("objetivo_alcancado", False):
                    stats_algoritmo[algoritmo]["sucessos"] += 1
                stats_algoritmo[algoritmo]["eficiencias"].append(info.get("eficiencia", 0.0))
        
        row = 0
        for algoritmo, stats in sorted(stats_algoritmo.items()):
            taxa = (stats["sucessos"] / stats["usos"] * 100) if stats["usos"] > 0 else 0
            efic_media = sum(stats["eficiencias"]) / len(stats["eficiencias"]) if stats["eficiencias"] else 0
            
            tabela_algoritmos.insertRow(row)
            tabela_algoritmos.setItem(row, 0, QTableWidgetItem(str(algoritmo)))
            tabela_algoritmos.setItem(row, 1, QTableWidgetItem(str(stats["usos"])))
            tabela_algoritmos.setItem(row, 2, QTableWidgetItem(str(stats["sucessos"])))
            tabela_algoritmos.setItem(row, 3, QTableWidgetItem(f"{taxa:.1f}%"))
            tabela_algoritmos.setItem(row, 4, QTableWidgetItem(f"{efic_media:.2f}"))
            row += 1
        
        layout.addWidget(tabela_algoritmos)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    def iniciar_simulacao(self):
        """Inicia simulação com abordagens selecionadas"""
        print("\n" + "="*70)
        print("▶ INICIANDO SIMULAÇÃO - SISTEMA DE RODADAS PROGRESSIVAS")
        print("="*70)
        
        try:
            # Obtém abordagem selecionada do COMBO
            self.abordagens_selecionadas = [self.combo_abordagem.currentIndex()]
            
            if not self.abordagens_selecionadas:
                self.label_status.setText("❌ Selecione uma abordagem!")
                self.label_status.setStyleSheet("color: white; background: #f44336; padding: 12px; border-radius: 5px; font-weight: bold;")
                return
            
            nomes = {0: 'A (Tesouros)', 1: 'B (Sobrevivência)', 2: 'C (Bandeira)'}
            print(f"✅ Abordagens: {', '.join(nomes[i] for i in self.abordagens_selecionadas)}")
            
            # Reset de estado
            self.turno_atual = 0
            self.rodada_atual = 1
            self.num_agentes_atual = 2
            self.percentagem_bombas_atual = 50.0
            self.simulacao_ativa = True
            self.gerenciador = GerenciadorGrupos()
            self.gestores_metricas = {}
            self.resultados_rodadas = {}
            self.tabs_grupos.clear()
            
            # Criar grupos para PRIMEIRA RODADA
            print(f"\n📍 RODADA 1 - Criando grupos...")
            self._criar_grupos_rodada_atual()
            
            # Criar grid visual
            print("🗺️ Criando visualização do mapa...")
            if self.grid_mapa:
                self.layout_container.removeWidget(self.grid_mapa)
                self.grid_mapa.deleteLater()
            
            primeiro_grupo = list(self.gerenciador.grupos.values())[0]
            mapa_base = primeiro_grupo['mapa_original']
            self.grid_mapa = GridMapa(mapa_base, cores_grupos=self.cores_grupos)
            self.layout_container.addWidget(self.grid_mapa)
            
            # Atualizar interface (AUTOMÁTICO - SEM COMBO)
            self._atualizar_abas_grupos()
            self._atualizar_labels()
            
            # Iniciar timer
            velocidade_ms = self._obter_velocidade_ms()
            self.timer.start(velocidade_ms)
            
            self.btn_iniciar.setEnabled(False)
            self.btn_pausar.setEnabled(True)
            self.label_status.setText("▶ Simulação em execução...")
            self.label_status.setStyleSheet("color: white; background: #4CAF50; padding: 12px; border-radius: 5px; font-weight: bold;")
            
            print("\n✅ SIMULAÇÃO INICIADA COM SUCESSO!")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar: {e}")
            import traceback
            traceback.print_exc()
            self.label_status.setText(f"❌ Erro: {str(e)}")
            self.label_status.setStyleSheet("color: white; background: #f44336; padding: 12px; border-radius: 5px; font-weight: bold;")

    def _criar_grupos_rodada_atual(self):
        """Cria grupos para a rodada atual com grupos diversos por abordagem"""
        abordagens = {
            0: AbordagensPadrao.obter_abordagem_a(),
            1: AbordagensPadrao.obter_abordagem_b(),
            2: AbordagensPadrao.obter_abordagem_c(),
        }
        
        self.resultados_rodadas[self.rodada_atual] = {}
        numero_grupo_global = 1  # COMEÇA EM 1
        
        for abordagem_id in self.abordagens_selecionadas:
            abordagem = abordagens[abordagem_id]
            print(f"\n  📌 Abordagem {chr(65+abordagem_id)} ({abordagem.tipo.value})")
            
            if abordagem_id not in self.gestores_metricas:
                self.gestores_metricas[abordagem_id] = {}
            
            self.resultados_rodadas[self.rodada_atual][abordagem_id] = {}
            
            # ESTRATÉGIAS - TODAS AS ABORDAGENS TÊM MÚLTIPLOS GRUPOS AGORA
            estrategias = self._obter_estrategias_abordagem(abordagem_id)
            
            for estrategia_nome, factory in estrategias:
                grupo_id = f"R{self.rodada_atual}_A{abordagem_id}_G{numero_grupo_global}"
                
                print(f"    ✓ {estrategia_nome} (GRUPO {numero_grupo_global})")
                print(f"      Config: {self.num_agentes_atual} agentes, {self.percentagem_bombas_atual:.2f}% bombas")
                
                # CRIAR GRUPO ISOLADO (com regeneração)
                self.gerenciador.criar_grupo(
                    grupo_id=grupo_id,
                    abordagem=abordagem.tipo.value,
                    modo=abordagem.modo_jogo,
                    agentes_factory=factory,
                    num_agentes=self.num_agentes_atual,
                    percentagem_bombas=self.percentagem_bombas_atual,
                    numero_grupo=numero_grupo_global
                )
                
                # Criar gestor de métricas
                self.gestores_metricas[abordagem_id][grupo_id] = GestorMetricas()
                
                agentes = self.gerenciador.obter_agentes_por_grupo(grupo_id)
                print(f"      {len(agentes)} agentes criados")
                
                # Inicializar métricas
                grupo_metricas = self.gestores_metricas[abordagem_id][grupo_id].criar_grupo(
                    grupo_id, abordagem.modo_jogo, 0
                )
                for agente in agentes:
                    grupo_metricas.adicionar_agente(agente.id, agente.__class__.__name__)
                
                # Armazenar info do grupo
                self.resultados_rodadas[self.rodada_atual][abordagem_id][grupo_id] = {
                    "estrategia": estrategia_nome,
                    "num_agentes": len(agentes),
                    "tipos": [a.__class__.__name__ for a in agentes],
                    "grupo_numero": numero_grupo_global
                }
                
                numero_grupo_global += 1
        
        self.grupos_totais_nesta_rodada = len(self.gerenciador.grupos)
        self.grupos_completados_nesta_rodada = 0

    def _obter_estrategias_abordagem(self, abordagem_id):
        """Retorna estratégias para uma abordagem - TODOS TÊM 2+ GRUPOS"""
        if abordagem_id == 0:  # Tesouros - BFS + KNN
            return [
                ("Exploração BFS", GeradorAgentesAbordagem.criar_grupo_bfs),
                ("Busca KNN", GeradorAgentesAbordagem.criar_grupo_knn),
            ]
        elif abordagem_id == 1:  # Sobrevivência - Padrão + BFS
            return [
                ("Estratégia Padrão", GeradorAgentesAbordagem.criar_para_abordagem_b),
                ("Busca Defensiva", GeradorAgentesAbordagem.criar_grupo_bfs),
            ]
        elif abordagem_id == 2:  # Bandeira - KNN + Padrão
            return [
                ("Busca Focada", GeradorAgentesAbordagem.criar_grupo_knn),
                ("Busca Metódica", GeradorAgentesAbordagem.criar_grupo_bfs),
            ]
        return []

    def _atualizar_abas_grupos(self):
        """Atualiza abas de métricas - MOSTRA TODOS GRUPOS SELECIONADOS (AUTO)"""
        # Limpar abas antigas
        while self.tabs_metricas.count() > 1:
            self.tabs_metricas.removeTab(0)
        
        self.tabs_grupos.clear()
        
        # Criar aba de RESUMO GERAL (primeira aba)
        aba_resumo = self._criar_aba_resumo_geral()
        self.tabs_metricas.insertTab(0, aba_resumo, "📊 RESUMO GERAL")
        
        # Mostrar TODAS rodadas atuais
        rodada = self.resultados_rodadas.get(self.rodada_atual, {})
        
        # Iterar sobre TODAS abordagens selecionadas
        for abordagem_id in self.abordagens_selecionadas:
            grupos_abordagem = rodada.get(abordagem_id, {})
            nomes_abord = {0: 'Tesouros', 1: 'Sobrevivência', 2: 'Bandeira'}
            
            for grupo_id, info in grupos_abordagem.items():
                numero = info["grupo_numero"]
                painel = self._criar_painel_grupo(grupo_id, abordagem_id, numero)
                self.tabs_grupos[grupo_id] = painel
                
                # Inserir aba
                self.tabs_metricas.addTab(
                    painel,
                    f"G{numero} - {nomes_abord[abordagem_id]}"
                )
        
        # Atualizar label de abordagem
        abords_nomes = {0: 'A', 1: 'B', 2: 'C'}
        self.label_abordagem_atual.setText(f"Ativas: {', '.join(abords_nomes[a] for a in self.abordagens_selecionadas)}")

    def executar_turno(self):
        """Executa um turno para todos os grupos"""
        if not self.simulacao_ativa:
            return
        
        try:
            resultado_turno = self.gerenciador.executar_turno_todos()
            self.turno_atual += 1
            
            # Atualizar mapa visual
            todos_agentes = self.gerenciador.obter_todos_agentes()
            if self.grid_mapa:
                self.grid_mapa.atualizar(list(todos_agentes.values()))
            
            # Atualizar métricas de cada grupo
            for grupo_id in self.gerenciador.grupos.keys():
                self._atualizar_metricas_grupo(grupo_id)
            
            # Atualizar labels
            self._atualizar_labels()
            
            # Verificar se TODOS os grupos completaram (condição de vitória)
            total_grupos = len(self.gerenciador.grupos)
            grupos_completados = sum(1 for r in resultado_turno.values() if r.get('terminou', False))
            
            # Rodada completa quando TODOS os grupos terminarem ou max turnos
            MAX_TURNOS_POR_RODADA = 200
            if self.turno_atual >= MAX_TURNOS_POR_RODADA or grupos_completados == total_grupos:
                # Rodada completada - MUDAr para próxima APENAS quando todos terminarem
                self._processar_fim_rodada()
                
        except Exception as e:
            print(f"❌ Erro em turno {self.turno_atual}: {e}")
            import traceback
            traceback.print_exc()

    def _atualizar_metricas_grupo(self, grupo_id):
        """Atualiza métricas de um grupo"""
        if grupo_id not in self.gerenciador.grupos:
            return
        
        grupo_info = self.gerenciador.grupos[grupo_id]
        agentes = grupo_info['agentes']
        
        # Encontrar abordagem
        abordagem_id = None
        for abord_id in self.abordagens_selecionadas:
            if abord_id in self.resultados_rodadas.get(self.rodada_atual, {}):
                if grupo_id in self.resultados_rodadas[self.rodada_atual][abord_id]:
                    abordagem_id = abord_id
                    break
        
        if abordagem_id is None:
            return
        
        if grupo_id not in self.tabs_grupos:
            return
        
        painel = self.tabs_grupos[grupo_id]
        
        if abordagem_id not in self.gestores_metricas or grupo_id not in self.gestores_metricas[abordagem_id]:
            return
        
        gestor = self.gestores_metricas[abordagem_id][grupo_id]
        grupo_metricas = gestor.obter_grupo(grupo_id)
        grupo_metricas.avanca_turno()
        
        # Nomes de objetivos
        objetivos = {
            0: "Coletar Tesouros + Bandeira",
            1: "Explorar 80% do mapa",
            2: "Encontrar Bandeira"
        }
        
        # Atualizar labels (cores melhoradas)
        painel.label_objetivo.setText(f"Objetivo: {objetivos.get(abordagem_id, '-')}")
        painel.label_turno_grupo.setText(f"Turno: {self.turno_atual}")
        painel.label_explorado.setText(f"Explorado: {grupo_metricas.obter_cobertura_mapa():.1f}%")
        painel.label_mortalidade.setText(f"Mortalidade: {grupo_metricas.obter_taxa_mortalidade():.1f}%")
        painel.label_eficiencia.setText(f"Eficiência: {grupo_metricas.obter_eficiencia_exploracao():.2f}")
        
        # Atualizar tabela de agentes
        painel.tabela_agentes.setRowCount(len(agentes))
        for i, agente in enumerate(agentes):
            metricas = agente.obter_metricas()
            painel.tabela_agentes.setItem(i, 0, QTableWidgetItem(str(agente.id)))
            painel.tabela_agentes.setItem(i, 1, QTableWidgetItem(agente.__class__.__name__))
            painel.tabela_agentes.setItem(i, 2, QTableWidgetItem(
                "VIVO" if agente.estado != EstadoAgente.MORTO else "MORTO"
            ))
            painel.tabela_agentes.setItem(i, 3, QTableWidgetItem(str(metricas.get("passos", 0))))
            painel.tabela_agentes.setItem(i, 4, QTableWidgetItem(str(metricas.get("tesouros", 0))))
            painel.tabela_agentes.setItem(i, 5, QTableWidgetItem(f"{metricas.get('eficiencia', 0):.1f}"))

    def _atualizar_labels(self):
        """Atualiza labels de rodada e turno"""
        self.label_rodada.setText(
            f"📍 Rodada: {self.rodada_atual}/9 | Agentes: {self.num_agentes_atual} | Bombas: {self.percentagem_bombas_atual:.2f}%"
        )
        self.label_turno.setText(f"⏱️ Turno: {self.turno_atual}")

    def _processar_fim_rodada(self):
        """Processa fim de uma rodada - COLETA MÉTRICAS FINAIS E REGENERA MAPA"""
        print(f"\n✅ RODADA {self.rodada_atual} COMPLETADA")
        
        # Coletar métricas finais de cada grupo ANTES de resetar
        for abordagem_id in self.abordagens_selecionadas:
            grupos_abordagem = self.resultados_rodadas[self.rodada_atual].get(abordagem_id, {})
            for grupo_id, info in grupos_abordagem.items():
                if grupo_id in self.gerenciador.grupos:
                    grupo_info = self.gerenciador.grupos[grupo_id]
                    agentes = grupo_info['agentes']
                    motor = grupo_info['motor']
                    
                    # Obter algoritmo em uso
                    algoritmo_em_uso = "Múltiplos"
                    if agentes:
                        algoritmo_em_uso = getattr(agentes[0], 'algoritmo_em_uso', 'N/A')
                    
                    # Obter gestor de métricas
                    if abordagem_id in self.gestores_metricas and grupo_id in self.gestores_metricas[abordagem_id]:
                        gestor = self.gestores_metricas[abordagem_id][grupo_id]
                        grupo_metricas = gestor.obter_grupo(grupo_id)
                        
                        # Armazenar métricas finais
                        info.update({
                            "algoritmo_em_uso": str(algoritmo_em_uso),
                            "explorado_pct": grupo_metricas.obter_cobertura_mapa(),
                            "agentes_vivos": sum(1 for a in agentes if a.esta_vivo()),
                            "objetivo_alcancado": motor.condicao_vitoria_alcancada() if hasattr(motor, 'condicao_vitoria_alcancada') else False,
                            "eficiencia": grupo_metricas.obter_eficiencia_exploracao(),
                            "taxa_mortalidade": grupo_metricas.obter_taxa_mortalidade()
                        })
        
        if self.rodada_atual < 9:
            # Próxima rodada
            self.rodada_atual += 1
            self.num_agentes_atual += 1
            self.percentagem_bombas_atual = 50 + (30 * (self.num_agentes_atual - 2) / 8)
            self.turno_atual = 0
            
            print(f"\n⬆️ ESCALANDO para Rodada {self.rodada_atual}")
            print(f"   Agentes: {self.num_agentes_atual}")
            print(f"   Bombas: {self.percentagem_bombas_atual:.2f}%")
            
            # Resetar gerenciador para nova rodada (força regeneração)
            self.gerenciador = GerenciadorGrupos()
            self._criar_grupos_rodada_atual()
            
            # REGENERAR MAPA COM NOVAS BOMBAS
            if self.grid_mapa:
                self.layout_container.removeWidget(self.grid_mapa)
                self.grid_mapa.deleteLater()
            
            primeiro_grupo = list(self.gerenciador.grupos.values())[0]
            mapa_base = primeiro_grupo['mapa_original']
            self.grid_mapa = GridMapa(mapa_base, cores_grupos=self.cores_grupos)
            self.layout_container.addWidget(self.grid_mapa)
            
            self._atualizar_abas_grupos()
            
        else:
            # Fim da simulação
            self._finalizar_simulacao()

    def _finalizar_simulacao(self):
        """Finaliza simulação"""
        self.timer.stop()
        self.simulacao_ativa = False
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        
        self.label_status.setText("✅ Simulação completada com sucesso!")
        self.label_status.setStyleSheet("color: white; background: #4CAF50; padding: 12px; border-radius: 5px; font-weight: bold;")
        
        print("\n" + "="*70)
        print("✅ SIMULAÇÃO FINALIZADA")
        print(f"   Total de Rodadas: {self.rodada_atual}")
        print(f"   Total de Turnos: {self.turno_atual}")
        print("="*70)

    def pausar_simulacao(self):
        """Pausa/continua simulação"""
        if self.simulacao_ativa:
            self.timer.stop()
            self.simulacao_ativa = False
            self.btn_pausar.setText("▶ CONTINUAR")
            self.label_status.setText("⏸ Simulação pausada")
            self.label_status.setStyleSheet("color: white; background: #FF9800; padding: 12px; border-radius: 5px; font-weight: bold;")
        else:
            self.simulacao_ativa = True
            self.timer.start()
            self.btn_pausar.setText("⏸ PAUSAR")
            self.label_status.setText("▶ Simulação em execução...")
            self.label_status.setStyleSheet("color: white; background: #4CAF50; padding: 12px; border-radius: 5px; font-weight: bold;")

    def resetar_simulacao(self):
        """Reseta simulação"""
        self.timer.stop()
        self.simulacao_ativa = False
        self.turno_atual = 0
        self.rodada_atual = 1
        self.num_agentes_atual = 2
        self.percentagem_bombas_atual = 50.0
        
        self.gerenciador = GerenciadorGrupos()
        self.gestores_metricas = {}
        self.resultados_rodadas = {}
        self.tabs_grupos.clear()
        
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.setText("⏸ PAUSAR")
        
        self.label_status.setText("⏳ Aguardando inicialização...")
        self.label_status.setStyleSheet("color: white; background: #1976D2; padding: 12px; border-radius: 5px; font-weight: bold;")
        self.label_rodada.setText("📍 Rodada: 1/9 | Agentes: 2 | Bombas: 50%")
        self.label_turno.setText("⏱️ Turno: 0")
        self.label_abordagem_atual.setText("Nenhuma")
        
        # Limpar grid
        if self.grid_mapa:
            self.layout_container.removeWidget(self.grid_mapa)
            self.grid_mapa.deleteLater()
            self.grid_mapa = None
        
        # Reset abas
        while self.tabs_metricas.count() > 1:
            self.tabs_metricas.removeTab(0)
        
        print("\n🔄 Simulação resetada")

    def _obter_velocidade_ms(self):
        """Obtém velocidade em ms"""
        velocidades = [0, 100, 200, 500, 1000]
        idx = self.combo_velocidade.currentIndex()
        return velocidades[idx] if idx < len(velocidades) else 200
