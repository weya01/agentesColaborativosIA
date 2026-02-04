"""
TESTE: Exploração de 100 turnos com AgenteAleatorio + aleatorio_seguro
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem

print("\n" + "=" * 70)
print("TESTE: 100 TURNOS COM AGENTES ALEATORIO_SEGURO")
print("=" * 70)

gerenciador = GerenciadorGrupos()
abordagem_b = AbordagensPadrao.obter_abordagem_b()
factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(TipoAbordagem.B.value)

gerenciador.criar_grupo(
    grupo_id=1,
    abordagem=TipoAbordagem.B.value,
    modo=abordagem_b.modo_jogo,
    agentes_factory=factory,
    num_agentes=5  # Aumentar para 5 agentes
)

agentes = gerenciador.obter_agentes_por_grupo(1)
memoria = gerenciador.grupos[1]['memoria']

print(f"\nAgentes: {[a.nome for a in agentes]}")
print(f"\nExecutando 100 turnos...")

for turno in range(1, 101):
    resultado = gerenciador.executar_turno_todos()
    
    exploradas = len(memoria.obter_exploradas(grupo_id=1))
    agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
    
    # Mostra cada 10 turnos
    if turno % 10 == 0 or turno == 1:
        print(f"Turno {turno:3d}: {exploradas:3d}/100 exploradas ({exploradas:.0%}) | " +
              f"{agentes_vivos}/{len(agentes)} vivos")

print("\n" + "=" * 70)
exploradas = len(memoria.obter_exploradas(grupo_id=1))
agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())

print(f"RESULTADO FINAL: {exploradas}/100 células ({exploradas:.0%})")
print(f"Agentes vivos: {agentes_vivos}/{len(agentes)}")
print(f"Modo B requer: >80% exploração + 1 vivo")
print(f"Objetivo alcançado: {exploradas > 80 and agentes_vivos >= 1}")
print("=" * 70)
