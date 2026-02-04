#!/usr/bin/env python3
"""
Script de teste - Ciclo de IA e simulação básica
"""
import sys
sys.path.insert(0, 'fontes')

from ambientes import GeradorMapaValido, Mapa, ValidadorAcessibilidade
from agentes.memoria_partilhada import MemoriaPartilhada
from agentes.agentes_busca.agente_busca import AgenteBusca
from agentes.agentes_nao_busca.agente_nao_busca import AgenteAleatorio
from simulacao.motor import MotorSimulacao
from utils.constantes import ModoJogo

print("=" * 60)
print("TESTE DE CICLO DE IA E SIMULAÇÃO")
print("=" * 60)

# 1. Gera mapa válido
print("\n1. Gerando mapa (Abordagem A)...")
gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
mapa, relatorio = gerador.gerar_com_relatorio()
print(f"   Mapa: {relatorio['mensagem']}")

# 2. Valida acessibilidade
print("\n2. Validando acessibilidade com flood fill...")
validador_acess = ValidadorAcessibilidade(mapa)
resultado_acess = validador_acess.validar()
print(f"   Válido: {resultado_acess['valido']}")
print(f"   Acessíveis: {resultado_acess['total_acessiveis']}/100")
print(f"   Inacessíveis: {resultado_acess['total_inacessiveis']}")

# 3. Cria agentes
print("\n3. Criando agentes...")
memoria = MemoriaPartilhada()
agentes = [
    AgenteBusca("A1", mapa, memoria, grupo_id=0),
    AgenteAleatorio("A2", mapa, memoria, grupo_id=0),
]
print(f"   Criados {len(agentes)} agentes")
print(f"   A1: {agentes[0].__class__.__name__}")
print(f"   A2: {agentes[1].__class__.__name__}")

# 4. Cria motor de simulação
print("\n4. Criando motor de simulação...")
motor = MotorSimulacao(
    mapa=mapa,
    agentes=agentes,
    memoria=memoria,
    modo=ModoJogo.A_TESOUROS,
    max_turnos=20,
    grupo_id=0
)
print("   Motor criado")

# 5. Executa alguns turnos
print("\n5. Executando 5 turnos...")
for turno in range(1, 6):
    print(f"\n   Turno {turno}:")
    
    # Executa turno para cada agente
    for agente in agentes:
        if agente.estado.value == "ativo":
            agente.executar_turno()
            print(f"      {agente.id}: passos={agente.passos}, exploradas={len(agente.celulas_exploradas)}")
    
    # Verifica objetivo
    objetivo = motor.verificar_objetivo_rapido()
    print(f"      Objetivo alcançado: {objetivo}")
    
    if objetivo:
        print("      ✓ Abordagem A completada!")
        break

print(f"\n6. Estatísticas finais:")
print(f"   Tesouros descobertos: {len(memoria.obter_tesouros(grupo_id=0))}")
print(f"   Células exploradas: {len(memoria.obter_exploradas(grupo_id=0))}")
print(f"   Agentes vivos: {sum(1 for a in agentes if a.estado.value == 'ativo')}")

print("\n" + "=" * 60)
print("✅ TESTE CONCLUÍDO COM SUCESSO!")
print("=" * 60)
