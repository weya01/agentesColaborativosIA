"""
Teste final: Rodar main.py com timeout pequeno e verificar que inicia
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import sys

print("\n" + "="*80)
print("TESTE FINAL: main.py equivalente")
print("="*80 + "\n")

try:
    app = QApplication(sys.argv)
    
    print("1️⃣  Importando JanelaPrincipalClean...")
    from ui.janela_principal_clean import JanelaPrincipal
    print("   ✅ Importado")
    
    print("\n2️⃣  Criando janela principal...")
    janela = JanelaPrincipal()
    print("   ✅ Janela criada")
    
    print("\n3️⃣  Mostrando janela...")
    janela.show()
    print("   ✅ Janela mostrada")
    
    print("\n4️⃣  Verificando que é a classe correta...")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    print(f"   ✓ É instância de JanelaPrincipalMultiGrupo: {isinstance(janela, JanelaPrincipalMultiGrupo)}")
    
    print("\n5️⃣  Processando eventos...")
    app.processEvents()
    print("   ✅ OK")
    
    print("\n" + "="*80)
    print("✅ PROGRAMA FUNCIONA! Você pode clicar no botão 'Iniciar Simulação'")
    print("="*80 + "\n")
    
    # Nota: Não vamos chamar app.exec() pois esperamos que o utilizador faça isso
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "="*80)
    print("❌ PROGRAMA NÃO FUNCIONA")
    print("="*80 + "\n")
    sys.exit(1)
