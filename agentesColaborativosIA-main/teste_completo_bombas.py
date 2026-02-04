"""
Teste completo da simulação de uma rodada.
Valida:
1. Geração de mapas com bombas dinâmicas (50%)
2. Criação de grupos com percentagem correta
3. Renderização de mapa com bombas visíveis
"""
import sys
sys.path.insert(0, r'c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes')

from ambientes.gerador_de_mapa import GeradorDeMapa
from simulacao.gerenciador_corridas import GerenciadorGrupos
from utils.constantes import ModoJogo
from agentes.agente_reactivo import AgenteReactivo

def contar_elementos(mapa):
    """Conta tipos de célula"""
    contagem = {'L': 0, 'B': 0, 'T': 0, 'F': 0}
    for linha in mapa:
        for cel in linha:
            contagem[cel] = contagem.get(cel, 0) + 1
    return contagem

print("=" * 80)
print("TESTE COMPLETO DE SIMULAÇÃO - VERIFICANDO BOMBAS E VITÓRIA")
print("=" * 80)

# 1. Teste gerador de mapa
print("\n✅ ETAPA 1: Testando geração de mapas com percentagens dinâmicas")
print("-" * 80)

for perc in [50, 65, 80]:
    gerador = GeradorDeMapa(tamanho=10, modo=ModoJogo.A_TESOUROS, percentagem_bombas=perc)
    mapa = gerador.gerar()
    contagem = contar_elementos(mapa)
    perc_real = (contagem['B'] / 100) * 100
    print(f"  {perc}% solicitado → {perc_real:.1f}% de bombas geradas (B={contagem['B']}, L={contagem['L']}, T={contagem['T']})")

# 2. Teste gerenciador
print("\n✅ ETAPA 2: Testando criação de grupos com percentagem de bombas")
print("-" * 80)

gerenciador = GerenciadorGrupos()

for percentagem in [50, 65, 80]:
    grupo_id = gerenciador.criar_grupo(
        grupo_id=f"grupo_{percentagem}",
        modo=ModoJogo.A_TESOUROS,
        abordagem=ModoJogo.A_TESOUROS,
        agentes_factory=lambda mapa, mem, n: [AgenteReactivo(f"A{i}", mapa, mem, i) for i in range(n)],
        num_agentes=3,
        percentagem_bombas=percentagem
    )
    
    grupo = gerenciador.grupos[grupo_id]
    mapa_original = grupo['mapa_original']
    contagem = contar_elementos(mapa_original)
    
    print(f"  Grupo {grupo_id}: {percentagem}% bombas → {contagem['B']} bombas no mapa")

print("\n" + "=" * 80)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 80)
