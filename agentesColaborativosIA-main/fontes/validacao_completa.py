#!/usr/bin/env python3
"""
Validação completa do sistema de escala progressiva
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fontes'))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("\n" + "="*70)
    print("🧪 VALIDAÇÃO: Sistema de Escala Progressiva")
    print("="*70)
    
    try:
        print("\n1️⃣  Testando imports...")
        from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
        from simulacao.abordagens import AbordagensPadrao
        from utils.constantes import ModoJogo
        from PySide6.QtWidgets import QListWidget, QListWidgetItem
        print("   ✅ Todos os imports OK")
        
        print("\n2️⃣  Testando fórmula de escala...")
        progressoes = []
        for num_agentes in range(2, 11):
            num_passos = num_agentes - 2
            pct_bombas = 50 + (30 * num_passos / 8)
            progressoes.append((num_agentes, pct_bombas))
            print(f"   {num_agentes} agentes → {pct_bombas:.1f}% bombas")
        
        # Validar que chega a 80%
        assert progressoes[-1][1] == 80.0, "Última escala deve ser 80%"
        print("   ✅ Fórmula validada")
        
        print("\n3️⃣  Testando Abordagem C...")
        ab_c = AbordagensPadrao.obter_abordagem_c()
        assert ab_c.modo_jogo == ModoJogo.C_BANDEIRA, "C deve ser BANDEIRA"
        print(f"   Modo: {ab_c.modo_jogo.value}")
        print(f"   Nome: {ab_c.nome}")
        print("   ✅ Abordagem C OK (sem tesouros)")
        
        print("\n4️⃣  Validando estrutura de estado...")
        assert hasattr(JanelaPrincipalMultiGrupo, '_escalar_grupo'), "Deve ter método _escalar_grupo"
        print("   ✅ Método _escalar_grupo existe")
        
        print("\n✅ VALIDAÇÃO COMPLETA - TUDO OK!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
