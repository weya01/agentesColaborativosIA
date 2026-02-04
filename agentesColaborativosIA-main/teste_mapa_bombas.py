"""
Teste rápido para validar geração de mapas com bombas dinâmicas.
"""
from fontes.ambientes.gerador_de_mapa import GeradorDeMapa
from fontes.utils.constantes import ModoJogo

def contar_tipos_mapa(mapa):
    """Conta tipos de célula no mapa"""
    contagem = {'L': 0, 'B': 0, 'T': 0, 'F': 0}
    for linha in mapa:
        for célula in linha:
            contagem[célula] = contagem.get(célula, 0) + 1
    
    total = sum(contagem.values())
    porcentagens = {k: (v/total)*100 for k, v in contagem.items()}
    return contagem, porcentagens

# Teste com percentagem dinâmica
print("=" * 60)
print("TESTE DE GERAÇÃO DE MAPAS COM BOMBAS DINÂMICAS")
print("=" * 60)

for perc in [50, 65, 80]:
    print(f"\n🎯 Testando com {perc}% de bombas:")
    print("-" * 60)
    
    for modo, nome in [(ModoJogo.A_TESOUROS, "Tesouros"), 
                        (ModoJogo.B_SOBREVIVENCIA, "Sobrevivência"),
                        (ModoJogo.C_BANDEIRA, "Bandeira")]:
        gerador = GeradorDeMapa(tamanho=10, modo=modo, percentagem_bombas=perc)
        mapa = gerador.gerar()
        
        contagem, porcentagens = contar_tipos_mapa(mapa)
        
        print(f"  {nome:15} | B: {contagem['B']:3} ({porcentagens['B']:5.1f}%) | "
              f"T: {contagem['T']:3} ({porcentagens['T']:5.1f}%) | "
              f"F: {contagem['F']:1} | L: {contagem['L']:3}")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
print("=" * 60)
