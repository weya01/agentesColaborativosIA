"""
TESTE: Movimento de Agentes com Aleatorio Seguro
Verifica se agentes evitam celeblulas exploradas
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\nTESTANDO MOVIMENTO DE AGENTES:\n")

try:
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
    
    print(f"Agentes: {[a.nome for a in agentes]}")
    print(f"\nDetalhes de cada agente:")
    for ag in agentes:
        print(f"  {ag.nome}: {ag.__class__.__name__}")
        print(f"    - tem algoritmo_em_uso: {hasattr(ag, 'algoritmo_em_uso')}")
        if hasattr(ag, 'algoritmo_em_uso'):
            print(f"    - algoritmo_em_uso: {ag.algoritmo_em_uso}")
        if hasattr(ag, 'algoritmos_disponiveis'):
            print(f"    - algoritmos_disponiveis: {ag.algoritmos_disponiveis}")
    print()
    
    posicoes_visitadas = {a.nome: set() for a in agentes}
    
    for turno in range(1, 26):
        resultado = gerenciador.executar_turno_todos()
        
        # Registra posições
        for agente in agentes:
            if agente.estado.value == "ativo":
                pos = (agente.x, agente.y)
                posicoes_visitadas[agente.nome].add(pos)
        
        exploradas = len(memoria.obter_exploradas(grupo_id=1))
        
        if turno in [1, 5, 10, 15, 20, 25]:
            print(f"Turno {turno:2d}:")
            for agente in agentes:
                if agente.estado.value == "ativo":
                    print(f"  {agente.nome}: pos ({agente.x},{agente.y}) | Células visitadas: {len(posicoes_visitadas[agente.nome])}")
                else:
                    print(f"  {agente.nome}: MORTO")
            print(f"  Total exploradas: {exploradas}/100")
            print()
    
    print("\nRESUMO FINAL:")
    for agente in agentes:
        print(f"{agente.nome}: {len(posicoes_visitadas[agente.nome])} células visitadas")
    
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()
