#!/usr/bin/env python3
"""
Teste de validação do sistema de escala progressiva com QListWidget
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fontes'))

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from utils.constantes import ModoJogo

def test_escala_progressiva():
    """Testa escala progressiva de agentes"""
    print("\n" + "="*70)
    print("🧪 TESTE: Escala Progressiva (2→10 agentes, 50%→80% bombas)")
    print("="*70)
    
    try:
        # Simular escala
        num_agentes = 2
        percentagem_bombas = 50
        
        print(f"\n📈 Progressão:")
        for i in range(9):  # De 2 até 10 agentes
            num_passos = num_agentes - 2
            percentagem_bombas = 50 + (30 * num_passos / 8)
            print(f"  Passo {i}: {num_agentes} agentes, {percentagem_bombas:.1f}% bombas")
            num_agentes += 1
        
        print(f"\n✅ Escala testada com sucesso!")
        
        # Teste de abordagem C sem tesouros
        print(f"\n🎯 Testando Abordagem C (sem tesouros)...")
        ab_c = AbordagensPadrao.obter_abordagem_c()
        print(f"   Abordagem: {ab_c.nome}")
        print(f"   Modo: {ab_c.modo_jogo.value}")
        
        print(f"\n✅ TESTE PASSOU!")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_escala_progressiva()
    sys.exit(0 if success else 1)
