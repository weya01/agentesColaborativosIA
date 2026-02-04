"""
TESTE OTIMIZADO: Exploração com 100 turnos máximo
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "="*80)
print("TESTE EXPLORAÇÃO: 100 Turnos Máximo (prob_bomba=10%)")
print("="*80 + "\n")

try:
    from simulacao.gerenciador_corridas import GerenciadorGrupos
    from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    
    gerenciador = GerenciadorGrupos()
    abordagem_b = AbordagensPadrao.obter_abordagem_b()
    factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(TipoAbordagem.B.value)
    
    gerenciador.criar_grupo(
        grupo_id=1,
        abordagem=TipoAbordagem.B.value,
        modo=abordagem_b.modo_jogo,
        agentes_factory=factory,
        num_agentes=5
    )
    
    agentes = gerenciador.obter_agentes_por_grupo(1)
    memoria = gerenciador.grupos[1]['memoria']
    mapa = gerenciador.grupos[1]['mapa_original']
    total_celulas = len(mapa) * len(mapa[0])
    
    print(f"Testando exploração com 5 agentes em mapa 10x10 (100 células)")
    print(f"Objetivo: >80 células exploradas (>80%)")
    print(f"Máximo: 100 turnos\n")
    
    max_turnos = 100
    for turno in range(1, max_turnos + 1):
        resultado = gerenciador.executar_turno_todos()
        modo_b_resultado = resultado.get(1, {})
        
        exploradas = len(memoria.obter_exploradas(grupo_id=1))
        cobertura = (exploradas / total_celulas) * 100
        agentes_vivos = sum(1 for ag in agentes if ag.estado.value == "ativo")
        terminou = modo_b_resultado.get('terminou', False)
        objetivo = modo_b_resultado.get('objetivo_alcancado', False)
        
        if turno % 5 == 0 or turno == 1 or terminou:
            print(f"Turno {turno:3d}: {exploradas:3d}/100 ({cobertura:5.1f}%) | Vivos: {agentes_vivos}/5 | Terminou: {terminou}")
        
        if terminou:
            status = "✅ SUCESSO" if objetivo else "❌ FALHA"
            print(f"\n{status}: Simulação terminou no turno {turno}")
            print(f"Exploração final: {cobertura:.1f}%")
            print(f"Agentes vivos: {agentes_vivos}/5")
            break
    
    if not modo_b_resultado.get('terminou', False):
        print(f"\n⚠️  Não terminou em 100 turnos")
        print(f"Exploração final: {cobertura:.1f}%")
    
    print("\n" + "="*80)
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
