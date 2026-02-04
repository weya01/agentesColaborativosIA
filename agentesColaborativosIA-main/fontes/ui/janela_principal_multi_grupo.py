"""
Nova Janela Principal com suporte a  Grupos Isolados Simultâneos.

Sistema:
- A, B, C correm SIMULTANEAMENTE
- Cada grupo tem ambiente lógico ISOLADO
- Visualização no MESMO mapa (cores diferentes)
- Resultados comparáveis
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QGroupBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QProgressBar, QTextEdit,
    QFrame, QCheckBox, QListWidget, QListWidgetItem
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont

from .grid_mapa import GridMapa
from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from agentes.base.agente_base import EstadoAgente
from metricas import GestorMetricas
from utils.constantes import ModoJogo


class JanelaPrincipalMultiGrupo(QWidget):
    """Janela principal com simulação de  grupos simultâneos"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulação Multi-Agentes -  Abordagens Simultâneas")
        self.setGeometry(00, 00, 600, 900)

        # Estado interno
        self.gerenciador = GerenciadorGrupos()
        self.grid_mapa = None
        self.turno_atual = 0
        self.simulacao_ativa = False
        self.abordagem_selecionada = 0  # Qual abordagem está sendo visualizada
        
        # Gestor de métricas para cada abordagem
        self.gestores_metricas = {}  # {abordagem_id: {grupo_id: GestorMetricas}}
        self.resultados_abordagens = {}  # {abordagem_id: {grupo_id: resultado}}
        self.tabs_grupos = {}  # {grupo_id: widget_painel}
        
        # Sistema de escala progressiva
        self.num_agentes_atual = 2  # Começa com 2
        self.percentagem_bombas_atual = 50  # Começa com 50%
        self.grupos_objetivo_alcancados = 0  # Contador de grupos que alcançaram objetivo

        # Timer para atualização visual
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_turno)

        # Build UI
        self._criar_ui()

    def _criar_ui(self):
        """Cria interface do usuário"""
        layout_principal = QHBoxLayout()

        # ========== PAINEL ESQUERDO - CONTROLES ==========
        painel_controles = self._criar_painel_controles()
        layout_principal.addWidget(painel_controles, 1)

        # ========== PAINEL CENTRAL - SIMULAÇÃO ==========
        painel_central = QVBoxLayout()

        # Label de status
        self.label_status = QLabel("Aguardando inicialização...")
        self.label_status.setFont(QFont("Arial", 12, QFont.Bold))
        painel_central.addWidget(self.label_status)

        # Grid do mapa (será preenchido quando simulação inicia)
        self.container_grid = QWidget()
        self.layout_container = QVBoxLayout()
        self.layout_container.addWidget(QLabel("Mapa será exibido aqui"))
        self.layout_container.setContentsMargins(0, 0, 0, 0)
        self.layout_container.setSpacing(0)
        self.container_grid.setLayout(self.layout_container)
        self.container_grid.setMinimumSize(400, 400)
        self.container_grid.setStyleSheet("background: transparent;")
        painel_central.addWidget(self.container_grid)

        # Barra de informações
        self.label_turno = QLabel("Turno: 0")
        self.label_turno.setFont(QFont("Arial", 12, QFont.Bold))
        painel_central.addWidget(self.label_turno)

        layout_principal.addLayout(painel_central, 2)

        # ========== PAINEL DIREITO - MÉTRICAS ==========
        painel_metricas = self._criar_painel_metricas()
        layout_principal.addWidget(painel_metricas, 1)

        self.setLayout(layout_principal)

    def _criar_painel_controles(self):
        """Cria painel de controles"""
        grupo = QGroupBox("Controles de Simulação")
        layout = QVBoxLayout()

        # Escolha de abordagens (múltiplas) - QListWidget
        layout.addWidget(QLabel("Selecione as abordagens (múltiplas):"))
        
        self.lista_abordagens = QListWidget()
        self.lista_abordagens.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        self.lista_abordagens.setMaximumHeight(100)
        
        # Adicionar opções à lista
        item_a = QListWidgetItem("🟢 Abordagem A: Tesouros (Coleta de Recursos)")
        item_b = QListWidgetItem("🔵 Abordagem B: Sobrevivência (Exploração Máxima)")
        item_c = QListWidgetItem("🟠 Abordagem C: Bandeira (Sem Tesouros)")
        
        self.lista_abordagens.addItem(item_a)
        self.lista_abordagens.addItem(item_b)
        self.lista_abordagens.addItem(item_c)
        
        # Selecionar A por padrão
        self.lista_abordagens.setCurrentRow(0)
        self.lista_abordagens.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        layout.addWidget(self.lista_abordagens)
        
        # Seletor de abordagem para visualizar (após simulação)
        layout.addWidget(QLabel("Abordagem para visualizar:"))
        self.combo_visualizar = QComboBox()
        self.combo_visualizar.addItems(["A - Tesouros", "B - Sobrevivência", "C - Bandeira"])
        self.combo_visualizar.currentIndexChanged.connect(self._atualizar_visualizacao_abordagem)
        layout.addWidget(self.combo_visualizar)

        layout.addWidget(QLabel("Velocidade (ms por turno):"))
        self.combo_velocidade = QComboBox()
        self.combo_velocidade.addItems([
            "Muito Rápido (0ms)",
            "Rápido (100ms)",
            "Normal (200ms)",
            "Lento (500ms)",
            "Muito Lento (1000ms)"
        ])
        self.combo_velocidade.setCurrentIndex(2)  # Normal
        layout.addWidget(self.combo_velocidade)

        # Botões de controle
        layout.addSpacing(10)
        self.btn_iniciar = QPushButton("▶ Iniciar Simulação")
        self.btn_iniciar.clicked.connect(self.iniciar_simulacao)
        self.btn_iniciar.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        self.btn_iniciar.setMinimumHeight(40)
        layout.addWidget(self.btn_iniciar)

        self.btn_pausar = QPushButton("⏸ Pausar")
        self.btn_pausar.clicked.connect(self.pausar_simulacao)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.setMinimumHeight(0)
        layout.addWidget(self.btn_pausar)

        self.btn_resetar = QPushButton("🔄 Resetar")
        self.btn_resetar.clicked.connect(self.resetar_simulacao)
        self.btn_resetar.setMinimumHeight(0)
        layout.addWidget(self.btn_resetar)

        self.btn_comparar = QPushButton("📊 Comparar Resultados")
        self.btn_comparar.clicked.connect(self.comparar_resultados)
        self.btn_comparar.setEnabled(False)
        self.btn_comparar.setMinimumHeight(0)
        layout.addWidget(self.btn_comparar)

        layout.addSpacing(0)

        # Legenda de cores
        legenda_texto = """
LEGENDA DE CORES:
🟢 Verde = Abordagem A (Tesouros)
🔵 Azul = Abordagem B (Sobrevivência)
🟠 Laranja = Abordagem C (Bandeira)

Todos os grupos correm simultaneamente
no MESMO mapa visual, mas com
ambientes ISOLADOS.
        """
        label_legenda = QLabel(legenda_texto)
        label_legenda.setFont(QFont("Arial", 8))
        layout.addWidget(QGroupBox(label_legenda))

        layout.addStretch()
        grupo.setLayout(layout)
        return grupo

    def _criar_painel_metricas(self):
        """Cria painel de métricas para os grupos"""
        grupo = QGroupBox("Métricas das Simulações")
        layout = QVBoxLayout()

        # Abas dinâmicas para cada grupo
        self.tabs_metricas = QTabWidget()

        # Abas serão criadas dinamicamente quando a simulação inicia
        self.tabs_grupos = {}  # {grupo_id: widget}
        
        # Inicialmente mostra mensagem
        widget_vazio = QWidget()
        layout_vazio = QVBoxLayout()
        layout_vazio.addWidget(QLabel("Abas de grupos aparecerão quando simulação iniciar"))
        widget_vazio.setLayout(layout_vazio)
        self.tabs_metricas.addTab(widget_vazio, "Aguardando...")

        # Aba de Comparação entre grupos
        self.texto_comparacao = QTextEdit()
        self.texto_comparacao.setReadOnly(True)
        self.tabs_metricas.addTab(self.texto_comparacao, "📊 Comparação")

        layout.addWidget(self.tabs_metricas)
        grupo.setLayout(layout)
        return grupo

    def _criar_painel_grupo(self, grupo_id, abordagem_id, estrategia_nome):
        """Cria painel de métricas para um grupo específico"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Cabeçalho com informação do grupo
        titulo = QLabel(f"Grupo {grupo_id} - {estrategia_nome}")
        titulo.setStyleSheet("font-weight: bold; font-size: 12px; background: #f0f0f0; padding: 5px;")
        layout.addWidget(titulo)

        # Resumo
        texto_resumo = QTextEdit()
        texto_resumo.setReadOnly(True)
        texto_resumo.setMinimumHeight(120)
        layout.addWidget(QLabel("📋 Resumo"))
        layout.addWidget(texto_resumo)

        # Tabela de agentes
        tabela_agentes = QTableWidget()
        tabela_agentes.setColumnCount(6)
        tabela_agentes.setHorizontalHeaderLabels([
            "ID", "Tipo", "Status", "Passos", "Pontos", "Eficiência"
        ])
        layout.addWidget(QLabel("👥 Agentes"))
        layout.addWidget(tabela_agentes)

        widget.setLayout(layout)

        # Armazena referências para acesso posterior
        widget.texto_resumo = texto_resumo
        widget.tabela_agentes = tabela_agentes
        widget.abordagem_id = abordagem_id
        widget.grupo_id = grupo_id

        return widget

    def _atualizar_tabs_grupos(self):
        """Atualiza as abas para mostrar grupos da abordagem selecionada"""
        abordagem_selecionada = self.combo_visualizar.currentIndex()
        
        # Remove todas as abas exceto a de comparação
        while self.tabs_metricas.count() > 1:
            self.tabs_metricas.removeTab(0)
        
        # Se não há resultados ainda, mantém a aba vazia
        if abordagem_selecionada not in self.resultados_abordagens:
            return
        
        # Cria abas para cada grupo da abordagem selecionada
        resultados_abordagem = self.resultados_abordagens[abordagem_selecionada]
        for grupo_id in sorted(resultados_abordagem.keys()):
            estrategia = resultados_abordagem[grupo_id].get("estrategia", f"Grupo {grupo_id}")
            
            # Cria painel para o grupo
            painel = self._criar_painel_grupo(grupo_id, abordagem_selecionada, estrategia)
            self.tabs_grupos[grupo_id] = painel
            
            # Adiciona aba (antes da aba de comparação)
            tab_index = self.tabs_metricas.count() - 1
            self.tabs_metricas.insertTab(tab_index, painel, f"Grupo {grupo_id}")
        
        print(f"✅ Abas atualizadas para Abordagem {abordagem_selecionada} ({len(resultados_abordagem)} grupos)")

    def _obter_velocidade_ms(self):
        """Obtém velocidade em ms do combo"""
        velocidades = {
            0: 0,
            1: 100,
            2: 200,
            3: 500,
            4: 1000
        }
        return velocidades.get(self.combo_velocidade.currentIndex(), 100)

    def iniciar_simulacao(self):
        """Inicia simulação com múltiplas abordagens selecionadas"""
        print("\n" + "="*70)
        print("📌 INICIAR SIMULAÇÃO CLICADO")
        print("="*70)
        
        try:
            print("️⃣  Verificando abordagens selecionadas...")
            # Verifica quais abordagens foram selecionadas na QListWidget
            abordagens_selecionadas = []
            for idx, item in enumerate(self.lista_abordagens.selectedItems()):
                # Determina qual abordagem baseado na posição do item
                for i in range(self.lista_abordagens.count()):
                    if self.lista_abordagens.item(i) == item:
                        abordagens_selecionadas.append(i)
                        abord_nomes = {0: 'A', 1: 'B', 2: 'C'}
                        print(f"   ✅ Abordagem {abord_nomes[i]} selecionada")
                        break
            
            if len(abordagens_selecionadas) == 0:
                print("   ❌ Nenhuma abordagem selecionada")
                self.label_status.setText("❌ Selecione pelo menos uma abordagem!")
                return
            
            self.turno_atual = 0
            self.simulacao_ativa = True
            self.abordagem_selecionada = abordagens_selecionadas[0]
            self.combo_visualizar.setCurrentIndex(self.abordagem_selecionada)
            
            velocidade_ms = self._obter_velocidade_ms()
            
            print(f"\n️⃣  Criando grupos com diferentes algoritmos...")
            print(f"   Velocidade: {velocidade_ms}ms por turno")
            
            # Obtém abordagens
            abordagens = {
                0: AbordagensPadrao.obter_abordagem_a(),
                1: AbordagensPadrao.obter_abordagem_b(),
                2: AbordagensPadrao.obter_abordagem_c(),
            }

            # Cria múltiplos grupos (com diferentes combinações) para cada abordagem selecionada
            grupo_contador = 0
            for abordagem_id in abordagens_selecionadas:
                abordagem = abordagens[abordagem_id]
                print(f"\n📌 Abordagem {abordagem_id} - {abordagem.tipo.value}")
                
                # Definir diferentes estratégias de grupo para testar
                # Cada abordagem terá 3-4 grupos com combinações diferentes
                estrategias_grupo = self._definir_estrategias_grupo(abordagem_id)
                
                if abordagem_id not in self.gestores_metricas:
                    self.gestores_metricas[abordagem_id] = {}
                if abordagem_id not in self.resultados_abordagens:
                    self.resultados_abordagens[abordagem_id] = {}
                
                for estrategia_nome, factory in estrategias_grupo:
                    grupo_id = grupo_contador
                    grupo_contador += 1
                    
                    print(f"   ✓ Grupo {grupo_id}: {estrategia_nome}")
                    print(f"      Configuração: {self.num_agentes_atual} agentes, {self.percentagem_bombas_atual:.1f}% bombas")
                    
                    # Cria grupo isolado
                    self.gerenciador.criar_grupo(
                        grupo_id=grupo_id,
                        abordagem=abordagem.tipo.value,
                        modo=abordagem.modo_jogo,
                        agentes_factory=factory,
                        num_agentes=self.num_agentes_atual  # Usar número dinâmico
                    )
                    
                    # Cria gestor de métricas para este grupo
                    self.gestores_metricas[abordagem_id][grupo_id] = GestorMetricas()
                    
                    # Obtém agentes do grupo
                    agentes = self.gerenciador.obter_agentes_por_grupo(grupo_id)
                    print(f"      {len(agentes)} agentes criados")
                    
                    # Inicializa métricas para cada agente
                    grupo_metricas = self.gestores_metricas[abordagem_id][grupo_id].criar_grupo(grupo_id, abordagem.modo_jogo, 0)
                    for agente in agentes:
                        tipo_nome = agente.__class__.__name__
                        grupo_metricas.adicionar_agente(agente.id, tipo_nome)
                    
                    # Armazena informações do grupo
                    self.resultados_abordagens[abordagem_id][grupo_id] = {
                        "estrategia": estrategia_nome,
                        "num_agentes": len(agentes),
                        "tipos": [a.__class__.__name__ for a in agentes],
                        "objetivo_alcancado": False,
                        "turno_conclusao": None
                    }

            # Cria grid visual (mostra mapa base)
            print(f"\n️⃣  Criando visualização do mapa...")
            if self.grid_mapa is not None:
                try:
                    self.layout_container.removeWidget(self.grid_mapa)
                    self.grid_mapa.deleteLater()
                except:
                    pass
            
            # Obtém mapa do primeiro grupo
            primeiro_grupo_id = abordagens_selecionadas[0]
            mapa_base = self.gerenciador.grupos[primeiro_grupo_id]['mapa_original']
            self.grid_mapa = GridMapa(mapa_base)
            self.layout_container.addWidget(self.grid_mapa)
            print("   ✅ GridMapa criado")
            
            # Atualiza abas de métricas para mostrar grupos da abordagem selecionada
            print(f"\n️⃣  Criando abas de métricas...")
            self._atualizar_tabs_grupos()
            print("   ✅ Abas criadas")

            # Inicia timer
            print(f"\n️⃣  Iniciando timer ({velocidade_ms}ms)...")
            self.timer.start(velocidade_ms)
            print("   ✅ Timer iniciado")

            # Atualiza UI
            print(f"\n️⃣  Atualizando interface...")
            self.btn_iniciar.setEnabled(False)
            self.btn_pausar.setEnabled(True)
            self.label_status.setText("▶ Simulação ativa")
            self.label_status.setStyleSheet("color: green; font-weight: bold;")
            print("   ✅ UI atualizada")
            
            print("\n" + "="*70)
            print("✅ SIMULAÇÃO INICIADA COM SUCESSO!")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar simulação: {e}")
            import traceback
            traceback.print_exc()
            self.label_status.setText(f"❌ Erro: {str(e)}")
            self.label_status.setStyleSheet("color: red; font-weight: bold;")

    def pausar_simulacao(self):
        """Pausa/continua simulação"""
        if self.simulacao_ativa:
            self.timer.stop()
            self.simulacao_ativa = False
            self.btn_pausar.setText("▶ Continuar")
            self.label_status.setText("⏸ Simulação pausada")
            self.label_status.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.timer.start()
            self.simulacao_ativa = True
            self.btn_pausar.setText("⏸ Pausar")
            self.label_status.setText("▶ Simulação ativa")
            self.label_status.setStyleSheet("color: green; font-weight: bold;")

    def resetar_simulacao(self):
        """Reseta simulação"""
        self.timer.stop()
        self.simulacao_ativa = False
        self.turno_atual = 0
        
        # Reset do sistema de escala progressiva
        self.num_agentes_atual = 2
        self.percentagem_bombas_atual = 50
        self.grupos_objetivo_alcancados = 0
        
        self.gerenciador.resetar()
        self.gestores_metricas = {}

        # Limpa UI
        self.btn_iniciar.setEnabled(True)
        self.btn_pausar.setEnabled(False)
        self.btn_pausar.setText("⏸ Pausar")
        self.btn_comparar.setEnabled(False)
        self.label_turno.setText("Turno: 0")
        self.label_status.setText("Aguardando inicialização...")
        self.label_status.setStyleSheet("color: black;")
        
        # Limpa painéis de métricas dinâmicas
        self.tabs_grupos.clear()
        self.texto_comparacao.clear()

    def atualizar_turno(self):
        """Executa um turno para TODOS os grupos selecionados simultaneamente"""
        if not self.simulacao_ativa:
            return

        try:
            # Executa um turno para todos os grupos
            resultado_turno = self.gerenciador.executar_turno_todos()

            self.turno_atual += 1

            # Obtém todos os agentes (de todos os grupos)
            todos_agentes = self.gerenciador.obter_todos_agentes()

            # Atualiza visualização do mapa
            if self.grid_mapa:
                self.grid_mapa.atualizar(list(todos_agentes.values()))

            # Atualiza métricas apenas dos grupos que existem
            for grupo_id in self.gerenciador.grupos.keys():
                self._atualizar_metricas_grupo(grupo_id)

            # Atualiza label de turno
            self.label_turno.setText(f"Turno: {self.turno_atual}")

            # Verifica se algum grupo terminou e escala se necessário
            grupos_ativos = sum(1 for r in resultado_turno.values() if not r['terminou'])
            grupos_terminaram_agora = sum(1 for r in resultado_turno.values() if r.get('terminou_neste_turno', False))
            
            # Se algum grupo alcançou objetivo neste turno, escala
            if grupos_terminaram_agora > 0:
                self._escalar_grupo()
            
            if grupos_ativos == 0:
                # TODOS os grupos terminaram
                self.timer.stop()
                self.simulacao_ativa = False
                self.btn_iniciar.setEnabled(True)
                self.btn_pausar.setEnabled(False)
                self.btn_comparar.setEnabled(True)
                
                # Termina todos os grupos e coleta resultados
                self.gerenciador.terminar_grupos()
                
                self.label_status.setText("✓ Simulação completa!")
                self.label_status.setStyleSheet("color: darkgreen; font-weight: bold;")
                print(f"\n✅ Simulação completa no turno {self.turno_atual}")
        except Exception as e:
            print(f"❌ Erro ao atualizar turno {self.turno_atual}: {e}")
            import traceback
            traceback.print_exc()
            print(f"\n✓ Simulação finalizada em {self.turno_atual} turnos")

    def _atualizar_metricas_grupo(self, grupo_id):
        """Atualiza métricas de um grupo específico"""
        if grupo_id not in self.gerenciador.grupos:
            return
        
        grupo_info = self.gerenciador.grupos[grupo_id]
        agentes = grupo_info['agentes']
        memoria = grupo_info['memoria']
        
        # Encontra abordagem do grupo
        abordagem_id = None
        for abord_id, grupos_dict in self.resultados_abordagens.items():
            if grupo_id in grupos_dict:
                abordagem_id = abord_id
                break
        
        if abordagem_id is None:
            return  # Grupo não encontrado
        
        # Se o grupo não está sendo visualizado, não atualiza
        if abordagem_id != self.combo_visualizar.currentIndex():
            return
        
        # Obtém painel de métricas do grupo
        if grupo_id not in self.tabs_grupos:
            return  # Painel ainda não criado
        
        painel = self.tabs_grupos[grupo_id]
        
        # Obtém gestor de métricas
        if abordagem_id not in self.gestores_metricas or grupo_id not in self.gestores_metricas[abordagem_id]:
            return
        
        gestor = self.gestores_metricas[abordagem_id][grupo_id]
        grupo_metricas = gestor.obter_grupo(grupo_id)
        grupo_metricas.avanca_turno()
        
        # Nomes de objetivos por abordagem
        nomes_objetivos = {
            0: "Coletar ≥0% tesouros",
            1: "Explorar ≥80% do mapa",
            2: "Encontrar bandeira"
        }
        
        # Obtém estratégia do grupo
        estrategia = self.resultados_abordagens[abordagem_id][grupo_id].get("estrategia", f"Grupo {grupo_id}")
        
        resumo = f"""Estratégia: {estrategia}
Objetivo: {nomes_objetivos[abordagem_id]}

Turno: {self.turno_atual}
Tesouros coletados: {grupo_metricas.obter_tesouros_coletados()}
Células exploradas: {grupo_metricas.obter_celulas_exploradas()}
Cobertura: {grupo_metricas.obter_cobertura_mapa():.2f}%
Agentes vivos: {grupo_metricas.obter_agentes_vivos()}
Agentes mortos: {grupo_metricas.obter_agentes_mortos()}
Taxa mortalidade: {grupo_metricas.obter_taxa_mortalidade():.2f}%
Eficiência: {grupo_metricas.obter_eficiencia_exploracao():.2f}
        """
        painel.texto_resumo.setText(resumo)
        
        # Atualiza tabela de agentes
        painel.tabela_agentes.setRowCount(len(agentes))
        for i, agente in enumerate(agentes):
            metricas = agente.obter_metricas()
            painel.tabela_agentes.setItem(i, 0, QTableWidgetItem(agente.id))
            painel.tabela_agentes.setItem(i, 1, QTableWidgetItem(metricas["tipo"]))
            painel.tabela_agentes.setItem(i, 2, QTableWidgetItem(
                "VIVO" if agente.estado != EstadoAgente.MORTO else "MORTO"
            ))
            painel.tabela_agentes.setItem(i, 3, QTableWidgetItem(str(metricas["passos"])))
            painel.tabela_agentes.setItem(i, 4, QTableWidgetItem(str(metricas.get("tesouros", 0))))
            painel.tabela_agentes.setItem(i, 5, QTableWidgetItem(f"{metricas['eficiencia']:.1f}"))


    def comparar_resultados(self):
        """Compara resultados de todas as  abordagens"""
        comparacao = self.gerenciador.comparar_grupos()
        
        if not comparacao:
            self.texto_comparacao.setText("Nenhum resultado disponível ainda.")
            return
        
        texto = "COMPARAÇÃO FINAL DAS TRÊS ABORDAGENS\n"
        texto += "=" * 50 + "\n\n"
        
        # Exibe resultados de cada grupo
        nomes_grupos = {0: "A - Tesouros", 1: "B - Sobrevivência", 2: "C - Bandeira"}
        
        for grupo_id, info in comparacao.get('grupos', {}).items():
            abordagem = nomes_grupos.get(grupo_id, f"Grupo {grupo_id}")
            texto += f"🔹 {abordagem}\n"
            texto += f"   Objetivo alcançado: {'✓ SIM' if info['objetivo_alcancado'] else '✗ NÃO'}\n"
            texto += f"   Turnos: {info['turno_final']}\n"
            texto += f"   Agentes: {info['num_agentes']}\n"
            texto += "\n"
        
        # Exibe melhores desempenhos
        texto += "=" * 0 + "\n"
        texto += "MELHORES DESEMPENHOS:\n"
        
        if comparacao.get('melhor_objetivo'):
            texto += f"✓ Melhor objetivo: Abordagem {comparacao['melhor_objetivo']}\n"
        
        if comparacao.get('melhor_tempo'):
            texto += f"⚡ Mais rápido: Abordagem {comparacao['melhor_tempo']}\n"
        
        if comparacao.get('melhor_eficiencia'):
            texto += f"📈 Mais eficiente: Abordagem {comparacao['melhor_eficiencia']}\n"
        
        self.texto_comparacao.setText(texto)

    def _limpar_mapa(self):
        """Limpa o mapa de elementos de simulações anteriores"""
        # Reseta o gerenciador para remover grupos antigos
        self.gerenciador = GerenciadorGrupos()
        self.gestores_metricas = {}
        self.turno_atual = 0
        self.simulacao_ativa = False
        
        # Limpa o grid visual
        if self.grid_mapa:
            self.layout_container.removeWidget(self.grid_mapa)
            self.grid_mapa.deleteLater()
            self.grid_mapa = None
        
        # Reseta label status
        self.label_status.setText("✓ Mapa limpo - Pronto para nova simulação")
        self.label_turno.setText("Turno: 0")
        
        # Desabilita botões de controle
        self.btn_pausar.setEnabled(False)
        self.btn_comparar.setEnabled(False)
        self.btn_iniciar.setEnabled(True)
        
        # Para timer se ativo
        if self.timer.isActive():
            self.timer.stop()
        
        print("\n" + "="*70)
        print("🧹 MAPA LIMPO - Elementos de simulações anteriores removidos")
        print("="*70)

    def _definir_estrategias_grupo(self, abordagem_id):
        """Define diferentes estratégias de grupos para cada abordagem"""
        estrategias = []
        
        if abordagem_id == 0:  # Abordagem A - Tesouros
            estrategias = [
                ("Grupo 1: Exploração BFS", GeradorAgentesAbordagem.criar_grupo_bfs),
                ("Grupo 2: Localização KNN", GeradorAgentesAbordagem.criar_grupo_knn),
                ("Grupo 3: Abordagem Híbrida", GeradorAgentesAbordagem.criar_grupo_hibrido),
                ("Grupo 4: Exploração Inversa", GeradorAgentesAbordagem.criar_grupo_hibrido_inverso),
            ]
        elif abordagem_id == 1:  # Abordagem B - Sobrevivência
            estrategias = [
                ("Grupo 1: Estratégia Padrão", GeradorAgentesAbordagem.criar_para_abordagem_b),
                ("Grupo 2: Estratégia Agressiva", 
                 lambda mapa, mem, num_agentes=None: GeradorAgentesAbordagem.criar_para_abordagem_b(mapa, mem, num_agentes=7)),
                ("Grupo 3: Estratégia Conservadora", 
                 lambda mapa, mem, num_agentes=None: GeradorAgentesAbordagem.criar_para_abordagem_b(mapa, mem, num_agentes=3)),
            ]
        elif abordagem_id == 2:  # Abordagem C - Bandeira (SEM TESOUROS)
            # Abordagem C não tem tesouros - apenas exploração
            estrategias = [
                ("Grupo 1: Busca Focada", GeradorAgentesAbordagem.criar_grupo_knn),
                ("Grupo 2: Exploração Aleatória", GeradorAgentesAbordagem.criar_para_abordagem_c),
                ("Grupo 3: Abordagem Balanceada", GeradorAgentesAbordagem.criar_hibrido_balanceado),
            ]
        
        return estrategias


    def _atualizar_visualizacao_abordagem(self):
        """Atualiza visualização quando muda a abordagem selecionada"""
        self.abordagem_selecionada = self.combo_visualizar.currentIndex()
        print(f"\n📊 Visualizando Abordagem {self.abordagem_selecionada}")
        # Atualiza abas para mostrar grupos da abordagem selecionada
        self._atualizar_tabs_grupos()

    def _atualizar_estilo_abordagem(self):
        """Atualiza estilo dos botões de abordagem baseado em seleção"""
        # Atualiza visual dos botões
        self._atualizar_estilos_abordagem()

    def _escalar_grupo(self):
        """
        Escala o número de agentes e percentagem de bombas após um grupo alcançar objetivo.
        Progressão: 2 agentes (50% bombas) → 10 agentes (80% bombas)
        """
        if self.num_agentes_atual < 10:
            self.num_agentes_atual += 1
            # Aumentar bombas de 50% para 80% conforme aumenta agentes
            # Progressão linear: 50% + (30% / 8 passos) * num_passos
            num_passos = self.num_agentes_atual - 2
            self.percentagem_bombas_atual = 50 + (30 * num_passos / 8)
            
            print(f"\n⬆️  ESCALA PROGRESSIVA: {self.num_agentes_atual} agentes, {self.percentagem_bombas_atual:.1f}% bombas")
        else:
            print(f"\n✅ ESCALA MÁXIMA ATINGIDA: 10 agentes, 80% bombas")

