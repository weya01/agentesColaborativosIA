"""
Teste de renderização e alternância entre abordagens
Verifica se GridMapa consegue renderizar sem crashes
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PySide6.QtCore import Qt

from ambientes import GeradorMapaValido
from ambientes.memoria_partilhada import MemoriaPartilhada
from ui.grid_mapa import GridMapa
from agentes.gerador_agentes import gerar_agentes_aleatorios
from utils.constantes import ModoJogo

class TestadorGridMapa(QMainWindow):
    """Testa renderização e alternância de GridMapa"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste GridMapa - Renderização e Alternância")
        self.setGeometry(100, 100, 600, 800)
        
        # Setup central widget
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        
        # Controles
        layout_controles = QHBoxLayout()
        
        label_abordagem = QLabel("Selecione Abordagem:")
        self.combo_abordagem = QComboBox()
        self.combo_abordagem.addItem("A - Tesouros", ModoJogo.A_TESOUROS)
        self.combo_abordagem.addItem("B - Sobrevivência", ModoJogo.B_SOBREVIVENCIA)
        self.combo_abordagem.addItem("C - Bandeira", ModoJogo.C_BANDEIRA)
        self.combo_abordagem.currentIndexChanged.connect(self.gerar_novo_mapa)
        
        layout_controles.addWidget(label_abordagem)
        layout_controles.addWidget(self.combo_abordagem)
        layout_controles.addStretch()
        
        layout_principal.addLayout(layout_controles)
        
        # Label de status
        self.label_status = QLabel("Inicializando...")
        layout_principal.addWidget(self.label_status)
        
        # Container para GridMapa
        self.widget_mapa = QWidget()
        self.layout_mapa = QVBoxLayout(self.widget_mapa)
        self.layout_mapa.setContentsMargins(0, 0, 0, 0)
        layout_principal.addWidget(self.widget_mapa)
        
        # Variáveis
        self.grid_mapa = None
        self.mapa = None
        self.memoria = None
        self.agentes = []
        
        # Gera primeira abordagem
        self.gerar_novo_mapa()
    
    def gerar_novo_mapa(self):
        """Gera novo mapa para a abordagem selecionada"""
        try:
            modo = self.combo_abordagem.currentData()
            modo_nome = self.combo_abordagem.currentText()
            
            self.label_status.setText(f"Gerando mapa para {modo_nome}...")
            
            # Limpa GridMapa anterior
            if self.grid_mapa is not None:
                try:
                    self.layout_mapa.removeWidget(self.grid_mapa)
                    self.grid_mapa.deleteLater()
                except:
                    pass
                self.grid_mapa = None
            
            # Gera mapa
            gerador = GeradorMapaValido(10, modo)
            self.mapa, relatorio = gerador.gerar_com_relatorio()
            
            if not relatorio.get('sucesso', False):
                self.label_status.setText(
                    f"❌ FALHA: {relatorio.get('mensagem')}"
                )
                return
            
            # Cria memória e agentes
            self.memoria = MemoriaPartilhada()
            self.agentes = gerar_agentes_aleatorios(self.mapa, self.memoria)
            
            # Cria GridMapa
            self.grid_mapa = GridMapa(self.mapa, self.memoria)
            self.layout_mapa.addWidget(self.grid_mapa)
            
            # Atualiza renderização
            self.grid_mapa.atualizar(self.agentes)
            
            # Status
            num_agentes = len(self.agentes)
            pct_acessivel = relatorio.get('percentual_acessivel', 0)
            bombas = relatorio.get('total_bombas', 0)
            tesouros = relatorio.get('total_tesouros', 0)
            
            self.label_status.setText(
                f"✅ Mapa OK: {pct_acessivel:.0f}% acessível, "
                f"{bombas} bombas, {tesouros} tesouros, "
                f"{num_agentes} agentes"
            )
            
            print(f"✅ {modo_nome} renderizado com sucesso")
            
        except Exception as e:
            import traceback
            self.label_status.setText(f"❌ ERRO: {str(e)}")
            print(f"❌ ERRO ao gerar mapa: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TestadorGridMapa()
    janela.show()
    
    print("\n" + "="*60)
    print("TESTE DE RENDERIZAÇÃO E ALTERNÂNCIA")
    print("="*60)
    print("Instruções:")
    print("  1. Verifique se o mapa renderiza sem erros (sem crashes)")
    print("  2. Alterne entre as 3 abordagens (A, B, C)")
    print("  3. Observe se:")
    print("     - Mapas geram corretamente")
    print("     - GridMapa renderiza sem crashes")
    print("     - Células mostram cores diferentes (vermelho=bomba, ouro=tesouro)")
    print("     - Agentes aparecem em verde com número")
    print("     - Colunas estão alinhadas (sem espaços entre)")
    print("\nFechando teste em 10 segundos...\n")
    
    # Auto-close after 10 seconds for automated testing
    import threading
    def auto_close():
        import time
        time.sleep(10)
        app.quit()
    
    thread = threading.Thread(target=auto_close, daemon=True)
    thread.start()
    
    sys.exit(app.exec())
