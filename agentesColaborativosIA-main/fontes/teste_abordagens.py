"""
Script de teste para validar que as 3 abordagens conseguem gerar mapas
"""
import sys
from ambientes import GeradorMapaValido
from utils.constantes import ModoJogo

def testar_geracao(modo, nome_abordagem, tentativas=5):
    """Testa a geração de mapas para uma abordagem"""
    print(f"\n{'='*60}")
    print(f"Testando {nome_abordagem}")
    print(f"{'='*60}")
    
    sucessos = 0
    falhas = 0
    acessibilidades = []
    
    for i in range(tentativas):
        gerador = GeradorMapaValido(10, modo)
        mapa, relatorio = gerador.gerar_com_relatorio()
        
        sucesso = relatorio.get('sucesso', False)
        mensagem = relatorio.get('mensagem', 'N/A')
        percentual = relatorio.get('percentual_acessivel', 0)
        
        if sucesso:
            sucessos += 1
            acessibilidades.append(percentual)
            status = "✅ OK"
        else:
            falhas += 1
            status = "❌ FALHA"
        
        print(f"  Tentativa {i+1}: {status} - {percentual:.1f}% acessível - {mensagem}")
    
    print(f"\n  RESUMO: {sucessos}/{tentativas} sucessos ({100*sucessos/tentativas:.0f}%)")
    if acessibilidades:
        media = sum(acessibilidades) / len(acessibilidades)
        minima = min(acessibilidades)
        maxima = max(acessibilidades)
        print(f"  Acessibilidade: Média={media:.1f}% | Min={minima:.1f}% | Max={maxima:.1f}%")
    
    return sucessos == tentativas

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTE DE GERAÇÃO DE MAPAS - TODAS AS ABORDAGENS")
    print("="*60)
    
    # Testa cada abordagem
    resultados = {}
    
    resultados['A'] = testar_geracao(
        ModoJogo.A_TESOUROS,
        "ABORDAGEM A (Tesouros >50%)",
        tentativas=5
    )
    
    resultados['B'] = testar_geracao(
        ModoJogo.B_SOBREVIVENCIA,
        "ABORDAGEM B (Exploração >80%)",
        tentativas=5
    )
    
    resultados['C'] = testar_geracao(
        ModoJogo.C_BANDEIRA,
        "ABORDAGEM C (Bandeira)",
        tentativas=5
    )
    
    # Resumo final
    print(f"\n{'='*60}")
    print("RESUMO FINAL")
    print(f"{'='*60}")
    print(f"Abordagem A (Tesouros):      {'✅ PASSA' if resultados['A'] else '❌ FALHA'}")
    print(f"Abordagem B (Sobrevivência): {'✅ PASSA' if resultados['B'] else '❌ FALHA'}")
    print(f"Abordagem C (Bandeira):      {'✅ PASSA' if resultados['C'] else '❌ FALHA'}")
    
    todos_ok = all(resultados.values())
    print(f"\nResultado Overall: {'✅ TUDO OK!' if todos_ok else '❌ ALGUMAS FALHAS'}")
    
    sys.exit(0 if todos_ok else 1)
