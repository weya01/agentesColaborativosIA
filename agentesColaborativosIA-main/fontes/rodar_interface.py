"""
Teste completo da interface com rodadas progressivas.
Execute este script para validar o sistema.
"""

import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def testar_interface_rodadas():
    """Teste visual da interface de rodadas"""
    
    print("\n" + "="*70)
    print("🧪 TESTE COMPLETO DA INTERFACE DE RODADAS")
    print("="*70 + "\n")
    
    print("✅ Importando componentes...")
    try:
        from ui.janela_principal_clean import JanelaPrincipal
        from simulacao.abordagens import AbordagensPadrao
        from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
        print("   ✅ Todos os componentes importados com sucesso\n")
    except Exception as e:
        print(f"   ❌ Erro ao importar: {e}")
        return False
    
    print("✅ Criando aplicação...")
    app = QApplication(sys.argv)
    
    print("✅ Inicializando interface...")
    try:
        janela = JanelaPrincipal()
        janela.show()
        print("   ✅ Interface criada e exibida\n")
    except Exception as e:
        print(f"   ❌ Erro ao criar interface: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("="*70)
    print("✅ INTERFACE PRONTA PARA USO!")
    print("="*70)
    print("\n📋 INSTRUÇÕES:")
    print("   1. Selecione as abordagens desejadas (A, B, e/ou C)")
    print("   2. Escolha a velocidade de simulação")
    print("   3. Clique em 'INICIAR SIMULAÇÃO'")
    print("   4. Observe:")
    print("      • Mapa sendo preenchido com agentes (cores diferentes)")
    print("      • Rodadas progredindo (2→10 agentes)")
    print("      • Bombas aumentando (50%→80%)")
    print("      • Métricas sendo atualizadas em tempo real")
    print("   5. Use 'Visualizar:' para trocar entre abordagens")
    print("\n" + "="*70 + "\n")
    
    # Executa a aplicação
    sys.exit(app.exec())


if __name__ == "__main__":
    testar_interface_rodadas()
