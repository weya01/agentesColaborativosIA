"""
TESTE: Modo C (Bandeira) - Encontrar a bandeira
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from utils.constantes import ModoJogo

print("\n" + "=" * 70)
print("TESTE: Modo C (Bandeira) - Encontrar a Bandeira")
print("=" * 70)

gerenciador = GerenciadorGrupos()
abordagem_c = AbordagensPadrao.obter_abordagem_c()

# Obter factory de agentes para Modo C
factory = GeradorAgentesAbordagem.obter_factory_por_abordagem("C")

gerenciador.criar_grupo(
    grupo_id=3,
    abordagem="C",
    modo=ModoJogo.C_BANDEIRA,
    agentes_factory=factory,
    num_agentes=5
)

agentes = gerenciador.obter_agentes_por_grupo(3)
memoria = gerenciador.grupos[3]['memoria']

# Obter mapa através do agente
mapa = agentes[0].mapa if agentes else None

print(f"\nMapa Modo C:")
if mapa:
    print(f"  - Tamanho: {mapa.tamanho}x{mapa.tamanho}")
    print(f"  - (0,0): {repr(mapa.ver((0, 0)))}")
    
    # Procura bandeira no mapa
    bandeira_pos = None
    for i in range(mapa.tamanho):
        for j in range(mapa.tamanho):
            if mapa.ver((i, j)) == "F":
                bandeira_pos = (i, j)
                break
    
    if bandeira_pos:
        print(f"  - Bandeira em: {bandeira_pos}")
    else:
        print(f"  - Bandeira: NÃO ENCONTRADA NO MAPA!")
else:
    print("  - Mapa não disponível")

print(f"\nAgentes criados: {[a.nome for a in agentes]}")
print(f"Tipos de agentes: {set(a.__class__.__name__ for a in agentes)}")

print(f"\nExecutando até 500 turnos (máx para Modo C)...")
print("-" * 70)

for turno in range(1, 501):
    resultado = gerenciador.executar_turno_todos()
    
    bandeira_encontrada = memoria.obter_bandeira(grupo_id=3) is not None
    agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
    exploradas = len(memoria.obter_exploradas(grupo_id=3))
    
    # Mostra cada 50 turnos ou se bandeira encontrada
    if turno % 50 == 0 or turno == 1 or bandeira_encontrada:
        print(f"Turno {turno:3d}: Exploradas={exploradas:2d}/100, " +
              f"Bandeira={'SIM' if bandeira_encontrada else 'NAO'}, " +
              f"Vivos={agentes_vivos}/{len(agentes)}")
    
    # Verifica se objetivo alcançado
    if bandeira_encontrada:
        print(f"\n*** BANDEIRA ENCONTRADA NO TURNO {turno}! ***")
        break
    
    # Termina se todos morreram
    if agentes_vivos == 0:
        print(f"\nTodos os agentes morreram no turno {turno}")
        break

print("\n" + "=" * 70)
print("RESULTADO FINAL:")
print("=" * 70)

bandeira_encontrada = memoria.obter_bandeira(grupo_id=3)
exploradas = len(memoria.obter_exploradas(grupo_id=3))
agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())

print(f"Bandeira encontrada: {'SIM' if bandeira_encontrada else 'NAO'}")
if bandeira_encontrada:
    print(f"Bandeira em: {bandeira_encontrada}")
print(f"Cells exploradas: {exploradas}/100")
print(f"Agentes vivos: {agentes_vivos}/{len(agentes)}")
print(f"Objetivo alcancado: {'SIM' if bandeira_encontrada else 'NAO'}")
print("=" * 70)
