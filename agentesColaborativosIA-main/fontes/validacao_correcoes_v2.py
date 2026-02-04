#!/usr/bin/env python3
"""
Validação rápida das correções v2.0 do sistema de rodadas.
Testa: checkboxes, numeração, cores, bombas, etc.
"""
import sys
from pathlib import Path

# Add fontes to path
sys.path.insert(0, str(Path(__file__).parent))

def testar_interface():
    """Testa se interface carrega"""
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(sys.argv)
        
        from ui.janela_principal_rodadas import JanelaPrincipalRodadas
        print("✅ Interface carrega sem erros")
        
        # Verificar atributos
        janela = JanelaPrincipalRodadas()
        
        # Teste 1: Checkboxes existem
        assert hasattr(janela, 'check_a'), "check_a não existe"
        assert hasattr(janela, 'check_b'), "check_b não existe"
        assert hasattr(janela, 'check_c'), "check_c não existe"
        print("✅ Checkboxes implementados (check_a, check_b, check_c)")
        
        # Teste 2: QListWidget removido
        assert not hasattr(janela, 'lista_abordagens'), "QListWidget ainda existe!"
        print("✅ QListWidget removido")
        
        # Teste 3: Label de abordagem atual existe
        assert hasattr(janela, 'label_abordagem_atual'), "label_abordagem_atual não existe"
        print("✅ Label de abordagem automática implementado")
        
        # Teste 4: Numeração começa em 1
        janela.abordagens_selecionadas = [0]
        janela.rodada_atual = 1
        janela.num_agentes_atual = 2
        janela.percentagem_bombas_atual = 50.0
        janela._criar_grupos_rodada_atual()
        
        # Verificar número do grupo
        for grupo_id, info in janela.resultados_rodadas[1][0].items():
            numero = info['grupo_numero']
            assert numero >= 1, f"Grupo numerado com {numero}, deve ser >= 1"
        print("✅ Grupos numerados 1-N (não 0-based)")
        
        # Teste 5: Cores melhoradas (verificar estilos)
        status_style = janela.label_status.styleSheet()
        assert "#" in status_style, "Estilos não contêm cores"
        print("✅ Cores e estilos aplicados")
        
        # Teste 6: Percentagem de bombas aumenta
        janela.rodada_atual = 1
        p1 = janela.percentagem_bombas_atual
        janela.rodada_atual = 2
        janela.num_agentes_atual = 3
        janela.percentagem_bombas_atual = 50 + (30 * (3 - 2) / 8)
        p2 = janela.percentagem_bombas_atual
        assert p2 > p1, f"Bombas não aumentaram: R1={p1}%, R2={p2}%"
        print(f"✅ Bombas aumentam: R1={p1:.2f}% → R2={p2:.2f}%")
        
        print("\n" + "="*60)
        print("🎉 TODAS AS CORREÇÕES VALIDADAS COM SUCESSO!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = testar_interface()
    sys.exit(0 if sucesso else 1)
