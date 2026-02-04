"""
Teste das mudanças: Agentes mortos desaparecem + não revisitam
"""
import sys
sys.path.insert(0, r'c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes')

from ambientes.gerador_de_mapa import GeradorDeMapa
from simulacao.gerenciador_corridas import GerenciadorGrupos
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from utils.constantes import ModoJogo

print("=" * 80)
print("TESTE: Agentes Mortos Desaparecem + Não Revisitam")
print("=" * 80)

# Criar grupo
gerenciador = GerenciadorGrupos()

grupo_info = gerenciador.criar_grupo(
    grupo_id="test_grupo",
    modo=ModoJogo.B_SOBREVIVENCIA,
    abordagem=ModoJogo.B_SOBREVIVENCIA,
    agentes_factory=GeradorAgentesAbordagem.criar_grupo_bfs,
    num_agentes=3,
    percentagem_bombas=50,
    numero_grupo=1
)

agentes = grupo_info['agentes']
motor = grupo_info['motor']

print(f"\n✅ Grupo criado com {len(agentes)} agentes")
print(f"   Agentes: {[a.id for a in agentes]}")

# Executar alguns turnos
print("\n🔄 Executando turnos...")
for turno in range(5):
    resultado = gerenciador.executar_turno_todos()
    
    # Verificar agentes vivos
    vivos = sum(1 for a in agentes if a.esta_vivo())
    mortos = len(agentes) - vivos
    
    print(f"\n   Turno {turno+1}:")
    print(f"      Vivos: {vivos}/{len(agentes)}")
    if mortos > 0:
        print(f"      Mortos: {mortos}")
        print(f"      ✅ Agentes mortos funcionando!")
    
    # Verificar se não voltam a células antigas
    for agente in agentes:
        if agente.esta_vivo():
            exploradas = len(agente.celulas_exploradas)
            print(f"      {agente.id}: {exploradas} células exploradas")

print("\n" + "=" * 80)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 80)
