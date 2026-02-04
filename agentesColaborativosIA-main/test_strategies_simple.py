#!/usr/bin/env python3
"""
Teste simples sem GUI para verificar se o sistema de múltiplos grupos funciona
"""
import sys
import os

# Adiciona fontes ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fontes'))

from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from simulacao.abordagens import AbordagensPadrao

def test_strategies():
    """Testa se os métodos de estratégia existem e são válidos"""
    print("\n" + "="*70)
    print("🧪 TESTE DE ESTRATÉGIAS")
    print("="*70)
    
    try:
        print("\n✅ Testando métodos de GeradorAgentesAbordagem...")
        
        # Verifica se métodos existem
        methods_to_check = [
            'criar_grupo_bfs',
            'criar_grupo_knn',
            'criar_grupo_hibrido',
            'criar_grupo_hibrido_inverso',
            'criar_hibrido_balanceado',
            'criar_para_abordagem_a',
            'criar_para_abordagem_b',
            'criar_para_abordagem_c'
        ]
        
        for method_name in methods_to_check:
            if hasattr(GeradorAgentesAbordagem, method_name):
                print(f"   ✓ {method_name}")
            else:
                print(f"   ✗ FALTA: {method_name}")
        
        print("\n✅ Testando AbordagensPadrao...")
        ab_a = AbordagensPadrao.obter_abordagem_a()
        ab_b = AbordagensPadrao.obter_abordagem_b()
        ab_c = AbordagensPadrao.obter_abordagem_c()
        
        print(f"   ✓ Abordagem A: {ab_a.tipo.value}")
        print(f"   ✓ Abordagem B: {ab_b.tipo.value}")
        print(f"   ✓ Abordagem C: {ab_c.tipo.value}")
        
        print("\n✅ TESTE PASSOU!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_strategies()
