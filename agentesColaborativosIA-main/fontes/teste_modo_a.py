"""
TESTE: Modo A (Tesouros) - Coletar >50% dos tesouros descobertos
Agentes BFS focados em encontrar e coletar tesouros
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao, TipoAbordagem

print("\n" + "=" * 70)
print("TESTE: Modo A (Tesouros) - Coletar >50% dos descobertos")
print("=" * 70)

gerenciador = GerenciadorGrupos()
abordagem_a = AbordagensPadrao.obter_abordagem_a()

# Obter factory de agentes para Modo A
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
factory = GeradorAgentesAbordagem.obter_factory_por_abordagem("A")

gerenciador.criar_grupo(
    grupo_id=1,
    abordagem="A",
    modo="A_TESOUROS",
    agentes_factory=factory,
    num_agentes=5
)

agentes = gerenciador.obter_agentes_por_grupo(1)
memoria = gerenciador.grupos[1]['memoria']

# Obter mapa através do motor ou agentes
mapa = agentes[0].mapa if agentes else None

print(f"\nMapa Modo A:")
if mapa:
    print(f"  - Tamanho: {mapa.tamanho}x{mapa.tamanho}")
    print(f"  - (0,0): {repr(mapa.ver((0, 0)))}")
    
    # Conta tesouros totais no mapa
    tesouros_totais = sum(1 for i in range(mapa.tamanho) for j in range(mapa.tamanho) 
                          if mapa.ver((i, j)) == "T")
    print(f"  - Tesouros totais no mapa: {tesouros_totais}")
else:
    print("  - Mapa não disponível")

print(f"\nAgentes: {[a.nome for a in agentes]}")
print(f"Tipos de agentes: {set(a.__class__.__name__ for a in agentes)}")

# Debug detalhado do turno 1
print(f"\n*** TURNO 1 DETALHADO ***")
gerenciador.executar_turno_todos()
print(f"Tesouros descobertos: {memoria.obter_tesouros(grupo_id=1)}")
print(f"Posições coletadas: {memoria.grupos[1]['posicoes_tesouro_coletado']}")
for ag in agentes:
    print(f"  {ag.nome}: pos={ag.posicao()}, coletados={ag.tesouros_coletados}")
print()

print(f"\nExecutando 300 turnos (máx para Modo A)...")
print("-" * 70)

for turno in range(1, 301):
    resultado = gerenciador.executar_turno_todos()
    
    tesouros_descobertos = len(memoria.obter_tesouros(grupo_id=1))
    tesouros_coletados = memoria.obter_tesouros_coletados(grupo_id=1)
    agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
    exploradas = len(memoria.obter_exploradas(grupo_id=1))
    
    # Mostra cada 20 turnos
    if turno % 20 == 0 or turno == 1:
        if tesouros_descobertos > 0:
            pct_coletado = (tesouros_coletados / tesouros_descobertos) * 100
        else:
            pct_coletado = 0
        print(f"Turno {turno:3d}: Exploradas={exploradas:2d}, Descobertos={tesouros_descobertos:2d}, " +
              f"Coletados={tesouros_coletados:2d} ({pct_coletado:.0f}%), " +
              f"Vivos={agentes_vivos}/{len(agentes)}")
    
    # Verifica se objetivo alcançado (>50%)
    if tesouros_descobertos > 0:
        if tesouros_coletados > tesouros_descobertos * 0.5:
            print(f"\n*** OBJETIVO ALCANÇADO NO TURNO {turno}! ***")
            break

print("\n" + "=" * 70)
print("RESULTADO FINAL:")
print("=" * 70)

tesouros_descobertos = len(memoria.obter_tesouros(grupo_id=1))
tesouros_coletados = memoria.obter_tesouros_coletados(grupo_id=1)

if tesouros_descobertos > 0:
    pct_coletado = (tesouros_coletados / tesouros_descobertos) * 100
    print(f"Tesouros descobertos: {tesouros_descobertos}")
    print(f"Tesouros coletados: {tesouros_coletados}")
    print(f"Percentual coletado: {pct_coletado:.1f}%")
    print(f"Objetivo (>50%): {'SIM' if tesouros_coletados > tesouros_descobertos * 0.5 else 'NAO'}")
else:
    print("NENHUM TESOURO FOI DESCOBERTO!")

agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
print(f"Agentes vivos: {agentes_vivos}/{len(agentes)}")
print("=" * 70)
