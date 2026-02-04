"""
Grid visual do mapa para interface gráfica.
"""
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .cores import CORES


class GridMapa(QWidget):
    """Renderiza o mapa em grid visual"""

    def __init__(self, mapa, memoria=None, cores_grupos=None):
        """
        Args:
            mapa: Objeto Mapa para renderizar (ou lista 2D)
            memoria: Memória partilhada para mostrar exploração (opcional)
            cores_grupos: Lista de cores para grupos (opcional)
        """
        super().__init__()
        self.mapa = mapa
        self.memoria = memoria
        self.cores_grupos = cores_grupos or [
            "#FF4444", "#4444FF", "#44FF44", "#FFAA00",
            "#FF44FF", "#00CCAA", "#FF8800", "#0088FF",
            "#AAFF00", "#FF0088"
        ]
        
        # Detecta se mapa é lista ou objeto
        if isinstance(mapa, list):
            self.tamanho = len(mapa)
            self.eh_lista = True
        else:
            self.tamanho = mapa.tamanho
            self.eh_lista = False
        
        self.layout = QGridLayout()
        self.celulas = {}

        self.setLayout(self.layout)
        self._criar_grid()

    def _criar_grid(self):
        """Cria grid de células com tamanho fixo"""
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                label = QLabel()
                label.setFixedSize(40, 40)  # Maior para ver melhor
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("border: 1px solid #333;")
                label.setFont(QFont("Arial", 8, QFont.Bold))
                self.layout.addWidget(label, i, j)
                self.celulas[(i, j)] = label

        # Remove espaçamento entre células
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)

    def atualizar(self, agentes, grupo_id=0):
        """
        Atualiza visualização do grid.
        
        Mostra:
        - Tipo de célula (L=branco, B=vermelho, T=ouro, F=roxo)
        - Agentes por grupo (cores diferentes)
        
        Args:
            agentes: Lista de agentes a renderizar
            grupo_id: ID do grupo para consultar memória
        """
        if not self.mapa:
            return

        # Renderiza mapa base
        for (x, y), label in self.celulas.items():
            try:
                # Obtém valor da célula
                if self.eh_lista:
                    valor = self.mapa[x][y]
                else:
                    valor = self.mapa.ver((x, y))
                
                # Cor base da célula
                if valor == "B":
                    cor_base = "#ff4444"  # Vermelho para bomba
                    simbolo = "💣"
                elif valor == "T":
                    cor_base = "#ffcc00"  # Ouro para tesouro
                    simbolo = "💰"
                elif valor == "F":
                    cor_base = "#cc44ff"  # Roxo para bandeira
                    simbolo = "🚩"
                else:  # "L" (livre)
                    cor_base = "#ffffff"
                    simbolo = ""
                
                # Sempre mostra a cor da célula
                label.setStyleSheet(
                    f"background-color: {cor_base}; "
                    f"border: 1px solid #333;"
                )
                
                label.setText(simbolo)
                label.setFont(QFont("Arial", 16))
                
            except Exception as e:
                label.setStyleSheet("background-color: #ff0000;")
                label.setText("E")

        # Renderiza agentes por grupo (com cores distintas)
        for agente in agentes:
            try:
                # NÃO renderiza agentes mortos
                if not agente.esta_vivo():
                    continue
                
                pos = agente.posicao()
                if pos in self.celulas:
                    label = self.celulas[pos]
                    # Obtém cor do grupo usando o número do grupo
                    numero_grupo = getattr(agente, 'numero_grupo', None)
                    grupo_id_agente = getattr(agente, 'grupo_id', 0)
                    
                    # Usa numero_grupo se disponível, senão usa grupo_id
                    indice_cor = numero_grupo if numero_grupo is not None else grupo_id_agente
                    
                    # Garante que é um índice válido
                    if isinstance(indice_cor, int):
                        indice_cor = indice_cor % len(self.cores_grupos)
                    else:
                        indice_cor = 0
                    
                    cor_grupo = self.cores_grupos[indice_cor]
                    
                    # Mostra ID do agente
                    numero = str(agente.id).replace("G", "").replace("A", "")
                    label.setText(numero)
                    label.setFont(QFont("Arial", 12, QFont.Bold))
                    label.setStyleSheet(
                        f"background-color: {cor_grupo}; "
                        "color: black; "
                        "border: 2px solid #000; "
                        "font-weight: bold;"
                    )
            except:
                pass

