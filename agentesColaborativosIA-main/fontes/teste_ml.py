"""
TESTE: Agentes com Modelos ML
Verifica se AgenteML funciona com cada uma das 3 técnicas.
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

from simulacao.gerenciador_corridas import GerenciadorGrupos
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
from agentes.modelos_ml import TecnicaML
from utils.constantes import ModoJogo

print("\n" + "=" * 70)
print("TESTE: Agentes com Modelos de Aprendizagem de Máquina")
print("=" * 70)

# Testa cada técnica ML
for tecnica in [TecnicaML.ARVORE_DECISAO, TecnicaML.KNN, TecnicaML.NAIVE_BAYES]:
    print(f"\n[TEST] Técnica: {tecnica.value.upper()}")
    print("-" * 70)
    
    gerenciador = GerenciadorGrupos()
    
    # Cria factory customizada para ML
    factory = lambda m, mem, n: GeradorAgentesAbordagem.criar_agentes_com_ml(
        m, mem, n, tecnica_ml=tecnica
    )
    
    gerenciador.criar_grupo(
        grupo_id=1,
        abordagem="B",
        modo=ModoJogo.B_SOBREVIVENCIA,
        agentes_factory=factory,
        num_agentes=3
    )
    
    agentes = gerenciador.obter_agentes_por_grupo(1)
    memoria = gerenciador.grupos[1]['memoria']
    
    print(f"Agentes criados: {[a.nome for a in agentes]}")
    print(f"Tipo: {agentes[0].__class__.__name__}")
    print(f"Algoritmo: {agentes[0].algoritmo_em_uso}")
    
    # Executa 30 turnos
    print("\nExecutando 30 turnos...")
    for turno in range(1, 31):
        resultado = gerenciador.executar_turno_todos()
        
        exploradas = len(memoria.obter_exploradas(grupo_id=1))
        agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
        
        if turno in [1, 5, 10, 15, 20, 25, 30]:
            print(f"  Turno {turno:2d}: Exploradas={exploradas:2d}, Vivos={agentes_vivos}/{len(agentes)}")
    
    exploradas = len(memoria.obter_exploradas(grupo_id=1))
    agentes_vivos = sum(1 for ag in agentes if ag.esta_vivo())
    print(f"\nRESULTADO: {exploradas} células, {agentes_vivos} agentes vivos")
    print(f"Status: {'OK' if agentes_vivos > 0 else 'FALHOU'}")

print("\n" + "=" * 70)
print("TESTE COMPLETO!")
print("=" * 70)
