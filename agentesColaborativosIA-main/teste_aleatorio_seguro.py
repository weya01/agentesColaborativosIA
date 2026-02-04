"""
Teste simples: Verificar se o agente AgenteAleatorio está funcionando corretamente
com aleatorio_seguro
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "=" * 70)
print("TESTE: AgenteAleatorio com aleatorio_seguro")
print("=" * 70)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem

# Cria grupo B com 2 agentes
gerenciador = GerenciadorGrupos()
abordagem_b = AbordagensPadrao.obter_abordagem_b()
factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(TipoAbordagem.B.value)

gerenciador.criar_grupo(
    grupo_id=1,
    abordagem=TipoAbordagem.B.value,
    modo=abordagem_b.modo_jogo,
    agentes_factory=factory,
    num_agentes=2  # Apenas 2 agentes para acompanhar
)

agentes = gerenciador.obter_agentes_por_grupo(1)
memoria = gerenciador.grupos[1]['memoria']
mapa = gerenciador.grupos[1]['mapa']

print(f"\nAgentes criados:")
for ag in agentes:
    print(f"  - {ag.nome}: {ag.__class__.__name__}")
    if hasattr(ag, 'algoritmos_disponiveis'):
        print(f"    Algoritmos: {ag.algoritmos_disponiveis}")
        print(f"    Algoritmo atual: {ag.algoritmo_em_uso}")

print(f"\nMapa: Tamanho {mapa.tamanho}x{mapa.tamanho}")
print(f"(0,0) = {repr(mapa.ver((0, 0)))}")

print(f"\nExecutando 25 turnos...")
print("-" * 70)

for turno in range(1, 26):
    resultado = gerenciador.executar_turno_todos()
    
    exploradas = len(memoria.obter_exploradas(grupo_id=1))
    
    print(f"\nTurno {turno} (Exploradas: {exploradas}/100):")
    for ag in agentes:
        estado = "VIVO" if ag.esta_vivo() else "MORTO"
        print(f"  {ag.nome}({estado}): Posição {ag.posicao()}, " +
              f"Células: {len(ag.celulas_exploradas)}, " +
              f"Algoritmo: {ag.algoritmo_em_uso}")

print("\n" + "=" * 70)
print("RESULTADO FINAL:")
print("=" * 70)

print(f"Total de células exploradas: {len(memoria.obter_exploradas(grupo_id=1))}/100")
print(f"Agentes vivos: {sum(1 for ag in agentes if ag.esta_vivo())}/{len(agentes)}")

for ag in agentes:
    metricas = ag.obter_metricas()
    print(f"\n{ag.nome}:")
    print(f"  - Passos: {metricas['passos']}")
    print(f"  - Bombas: {metricas['bombas_acionadas']}")
    print(f"  - Células exploradas: {metricas['celulas_exploradas']}")
    print(f"  - Vivo: {metricas['vivo']}")
    print(f"  - Algoritmo: {metricas['algoritmo_usado']}")
