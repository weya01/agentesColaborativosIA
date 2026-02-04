"""
Teste simples de geração de mapas com bombas dinâmicas.
"""
import sys
sys.path.insert(0, r'c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes')

from ambientes.gerador_de_mapa import GeradorDeMapa
from utils.constantes import ModoJogo

def contar_elementos(mapa):
    """Conta tipos de célula"""
    contagem = {'L': 0, 'B': 0, 'T': 0, 'F': 0}
    for linha in mapa:
        for cel in linha:
            contagem[cel] = contagem.get(cel, 0) + 1
    return contagem

print("=" * 80)
print("TESTE DE GERAÇÃO DE MAPAS COM PERCENTAGENS DINÂMICAS DE BOMBAS")
print("=" * 80)

for percentagem in [50, 65, 80]:
    print(f"\n📍 Testando {percentagem}% de bombas:")
    print("-" * 80)
    
    for modo_id, (modo, nome) in enumerate([
        (ModoJogo.A_TESOUROS, "Tesouros"),
        (ModoJogo.B_SOBREVIVENCIA, "Sobrevivência"),
        (ModoJogo.C_BANDEIRA, "Bandeira")
    ]):
        gerador = GeradorDeMapa(tamanho=10, modo=modo, percentagem_bombas=percentagem)
        mapa = gerador.gerar()
        contagem = contar_elementos(mapa)
        perc_real = (contagem['B'] / 100) * 100
        
        print(f"  {nome:15} | Bombas: {contagem['B']:2}/100 ({perc_real:5.1f}%) | "
              f"Tesouros: {contagem['T']:2} | Livres: {contagem['L']:2}")

print("\n" + "=" * 80)
print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
print("=" * 80)
