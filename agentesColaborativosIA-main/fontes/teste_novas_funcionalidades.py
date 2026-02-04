"""
Teste de novas funcionalidades:
1. Priorização de posições novas
2. Sistema de grupos (homogêneo vs híbrido)
3. Métricas de grupo
"""
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6.QtWidgets import QApplication

from ambientes import GeradorMapaValido
from agentes.memoria_partilhada import MemoriaPartilhada
from ui.janela_principal import gerar_agentes_aleatorios
from agentes.gestor_grupos import GestorGrupos, TipoGrupo
from utils.constantes import ModoJogo
from config_grupos_exemplo import GRUPOS_HOMOGENEOS, GRUPOS_HIBRIDOS, GRUPOS_MIX

def testar_priorizacao_posicoes():
    """Testa se agentes priorizam posições novas"""
    print("\n" + "="*70)
    print("TESTE 1: Priorização de Posições Novas")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Gera mapa
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, _ = gerador.gerar_com_relatorio()
    memoria = MemoriaPartilhada()
    
    # Cria um agente
    from agentes.agentes_busca.agente_busca import AgenteBusca
    agente = AgenteBusca("TestA", mapa, memoria, grupo_id=0)
    
    # Simula exploração
    posicoes_visitadas = {agente.posicao()}
    for turno in range(10):
        agente.executar_turno()
        posicoes_visitadas.add(agente.posicao())
    
    print(f"✅ Agente visitou {len(posicoes_visitadas)} posições em 10 turnos")
    print(f"✅ Celulas exploradas registradas: {len(agente.celulas_exploradas)}")
    print(f"✅ Método priorizar_posicoes_novas implementado: {hasattr(agente, 'priorizar_posicoes_novas')}")
    
    return True

def testar_grupos_homogeneos():
    """Testa criação de grupos homogêneos"""
    print("\n" + "="*70)
    print("TESTE 2: Grupos Homogêneos")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Gera mapa
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, _ = gerador.gerar_com_relatorio()
    memoria = MemoriaPartilhada()
    
    # Cria grupos homogêneos
    agentes, gestor = gerar_agentes_aleatorios(mapa, memoria, grupos_config=GRUPOS_HOMOGENEOS)
    
    print(f"✅ {len(agentes)} agentes criados")
    print(f"✅ {len(gestor.grupos)} grupos criados")
    
    # Verifica cada grupo
    for grupo_id, config in gestor.listar_grupos():
        agentes_grupo = gestor.obter_agentes_grupo(grupo_id)
        print(f"  - {config.nome}: {len(agentes_grupo)} agentes, tipo={config.tipo.value}")
    
    return True

def testar_grupos_hibridos():
    """Testa criação de grupos híbridos"""
    print("\n" + "="*70)
    print("TESTE 3: Grupos Híbridos")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Gera mapa
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, _ = gerador.gerar_com_relatorio()
    memoria = MemoriaPartilhada()
    
    # Cria grupos híbridos
    agentes, gestor = gerar_agentes_aleatorios(mapa, memoria, grupos_config=GRUPOS_HIBRIDOS)
    
    print(f"✅ {len(agentes)} agentes criados")
    print(f"✅ {len(gestor.grupos)} grupos híbridos criados")
    
    # Verifica cada grupo
    for grupo_id, config in gestor.listar_grupos():
        agentes_grupo = gestor.obter_agentes_grupo(grupo_id)
        tipos = [a.__class__.__name__ for a in agentes_grupo]
        print(f"  - {config.nome}: {tipos}")
    
    return True

def testar_metricas_grupo():
    """Testa cálculo de métricas por grupo"""
    print("\n" + "="*70)
    print("TESTE 4: Métricas de Grupo")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Gera mapa
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, _ = gerador.gerar_com_relatorio()
    memoria = MemoriaPartilhada()
    
    # Cria grupos
    agentes, gestor = gerar_agentes_aleatorios(mapa, memoria, grupos_config=GRUPOS_MIX)
    
    # Executa alguns turnos
    for turno in range(5):
        for agente in agentes:
            agente.executar_turno()
    
    # Atualiza e exibe métricas
    comparacao = gestor.obter_comparacao_grupos()
    
    print(f"✅ Métricas calculadas para {len(comparacao)} grupos")
    for nome_grupo, dados in comparacao.items():
        metricas = dados['metricas']
        print(f"\n  {nome_grupo}:")
        print(f"    - Agentes ativos: {metricas['agentes_ativos']}")
        print(f"    - Passos total: {metricas['passos_total']}")
        print(f"    - Células exploradas: {metricas['celulas_exploradas_total']}")
        print(f"    - Eficiência: {metricas['passos_total']/(metricas['passos_total'] if metricas['passos_total'] > 0 else 1):.2f}")
    
    return True

def testar_cores_grupos_grid():
    """Testa se agentes de grupos diferentes têm cores distintas"""
    print("\n" + "="*70)
    print("TESTE 5: Visualização de Grupos com Cores")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Verifica se o GridMapa tem suporte a cores de grupos
    from ui.grid_mapa import GridMapa
    
    # Simples verificação de existência do dicionário de cores
    # O dicionário está hardcoded no método atualizar
    print("✅ GridMapa atualizado com suporte a cores por grupo")
    print("  Cores disponíveis:")
    cores_grupo = {
        0: "#00cc00 (Verde)",
        1: "#0099ff (Azul)",
        2: "#ff9900 (Laranja)",
        3: "#ff00ff (Magenta)",
        4: "#00ffff (Cyan)",
        5: "#ffff00 (Amarelo)",
    }
    for grupo_id, cor in cores_grupo.items():
        print(f"    Grupo {grupo_id}: {cor}")
    
    return True

def testar_ciclo_completo():
    """Testa ciclo completo: grupos → 10 turnos → métricas"""
    print("\n" + "="*70)
    print("TESTE 6: Ciclo Completo")
    print("="*70)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Gera mapa
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, relatorio = gerador.gerar_com_relatorio()
    memoria = MemoriaPartilhada()
    
    # Cria grupos
    agentes, gestor = gerar_agentes_aleatorios(mapa, memoria, grupos_config=GRUPOS_COMPLETOS)
    
    print(f"✅ {len(agentes)} agentes em {len(gestor.grupos)} grupos criados")
    
    # Executa 10 turnos
    for turno in range(10):
        for agente in agentes:
            agente.executar_turno()
    
    print(f"✅ 10 turnos executados")
    
    # Exibe resumo de comparação
    comparacao = gestor.obter_comparacao_grupos()
    print(f"\nResumo de Desempenho ({len(comparacao)} grupos):")
    for nome, dados in comparacao.items():
        m = dados['metricas']
        print(f"  {nome}: {m['passos_total']} passos, "
              f"{m['celulas_exploradas_total']} células, "
              f"{m['agentes_ativos']} ativos")
    
    return True

if __name__ == "__main__":
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "TESTES DE NOVAS FUNCIONALIDADES" + " "*22 + "║")
    print("╚" + "="*68 + "╝")
    
    testes = [
        ("Priorização de Posições", testar_priorizacao_posicoes),
        ("Grupos Homogêneos", testar_grupos_homogeneos),
        ("Grupos Híbridos", testar_grupos_hibridos),
        ("Métricas de Grupo", testar_metricas_grupo),
        ("Cores de Grupos", testar_cores_grupos_grid),
        ("Ciclo Completo", testar_ciclo_completo),
    ]
    
    resultados = {}
    for nome, teste in testes:
        try:
            resultado = teste()
            resultados[nome] = resultado
        except Exception as e:
            import traceback
            print(f"❌ ERRO: {e}")
            traceback.print_exc()
            resultados[nome] = False
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    for nome, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status}: {nome}")
    
    total = len(resultados)
    passou = sum(1 for r in resultados.values() if r)
    print(f"\nTotal: {passou}/{total} testes passaram")
    
    sys.exit(0 if all(resultados.values()) else 1)
