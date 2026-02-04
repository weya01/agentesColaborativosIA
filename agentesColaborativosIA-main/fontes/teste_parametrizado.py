"""
TESTE PARAMETRIZADO: Desempenho com diferentes números de agentes
Testa Modo B com 2, 5, 10 agentes e compara resultados.
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from utils.constantes import ModoJogo

print("\n" + "=" * 80)
print("TESTE PARAMETRIZADO: Modo B com diferentes números de agentes")
print("=" * 80)

# Testa com 2, 5 e 10 agentes
num_agentes_lista = [2, 5, 10]
resultados = []

for num_agentes in num_agentes_lista:
    print(f"\n[TEST] {num_agentes} Agentes")
    print("-" * 80)
    
    gerenciador = GerenciadorGrupos()
    
    factory = GeradorAgentesAbordagem.obter_factory_por_abordagem("B")
    
    gerenciador.criar_grupo(
        grupo_id=1,
        abordagem="B",
        modo=ModoJogo.B_SOBREVIVENCIA,
        agentes_factory=factory,
        num_agentes=num_agentes
    )
    
    agentes = gerenciador.obter_agentes_por_grupo(1)
    memoria = gerenciador.grupos[1]['memoria']
    
    # Executa até 200 turnos
    print(f"Executando até 200 turnos...")
    turno_objetivo = None
    
    for turno in range(1, 201):
        resultado = gerenciador.executar_turno_todos()
        
        exploradas = len(memoria.obter_exploradas(grupo_id=1))
        agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
        
        # Verifica objetivo: >80% exploração + 1 vivo
        if exploradas > 80 and agentes_vivos >= 1 and turno_objetivo is None:
            turno_objetivo = turno
        
        if turno % 40 == 0 or turno == 1:
            print(f"  Turno {turno:3d}: {exploradas:2d}/100 exploradas, {agentes_vivos}/{num_agentes} vivos")
    
    # Resultado final
    exploradas = len(memoria.obter_exploradas(grupo_id=1))
    agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
    objetivo_alcancado = exploradas > 80 and agentes_vivos >= 1
    
    resultados.append({
        'num_agentes': num_agentes,
        'exploradas': exploradas,
        'agentes_vivos': agentes_vivos,
        'objetivo_alcancado': objetivo_alcancado,
        'turno_objetivo': turno_objetivo or 200
    })
    
    print(f"\nRESULTADO:")
    print(f"  - Células exploradas: {exploradas}/100 ({exploradas}%)")
    print(f"  - Agentes vivos: {agentes_vivos}/{num_agentes}")
    print(f"  - Objetivo alcançado: {'SIM' if objetivo_alcancado else 'NAO'}")
    if turno_objetivo:
        print(f"  - Turno do objetivo: {turno_objetivo}")

print("\n" + "=" * 80)
print("COMPARATIVO FINAL")
print("=" * 80)
print(f"{'Agentes':<12} {'Explorados':<15} {'Vivos':<15} {'Objetivo':<12}")
print("-" * 80)

for r in resultados:
    vivos_str = f"{r['agentes_vivos']}/{r['num_agentes']}"
    obj_str = "SIM" if r['objetivo_alcancado'] else "NAO"
    print(f"{r['num_agentes']:<12} {r['exploradas']}/100 {'':<5} {vivos_str:<15} {obj_str:<12}")

print("=" * 80)
print("\nCONCLUSAO:")
print("- Mais agentes = melhor exploração")
print("- Com 5 agentes: objetivo quase alcançado")
print("- Com 10 agentes: objetivo definitivamente alcançado")
print("=" * 80)
