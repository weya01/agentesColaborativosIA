"""
Script de validação e teste da nova arquitetura.
Verifica se todos os componentes estão integrados corretamente.
"""
import sys
from pathlib import Path

# Adiciona fontes ao path
sys.path.insert(0, str(Path(__file__).parent / "fontes"))

print("=" * 60)
print("VALIDAÇÃO DA ARQUITETURA DE AGENTES COLABORATIVOS")
print("=" * 60)

# ========== TESTE 1: Imports ==========
print("\n[1/6] Testando imports...")
try:
    from utils.constantes import ModoJogo
    from ambientes import GeradorMapaValido, Mapa, ValidadorMapa
    from agentes.memoria_partilhada import MemoriaPartilhada
    from agentes.base.agente_base import AgenteBase, EstadoAgente
    from agentes.agentes_busca.agente_busca import AgenteBusca, AgenteArvoreBusca
    from agentes.agentes_nao_busca.agente_nao_busca import (
        AgenteAleatorio, AgenteExploracao, AgenteKNN
    )
    from agentes.agentes_hibridos.agente_hibrido import (
        AgenteHibrido, AgenteAdaptativo, AgenteCombinado
    )
    from metricas import MetricasGrupo, GestorMetricas
    print("✓ Todos os imports funcionaram!")
except Exception as e:
    print(f"✗ Erro em imports: {e}")
    sys.exit(1)

# ========== TESTE 2: Geração de Mapa ==========
print("\n[2/6] Testando geração de mapa...")
try:
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa, valido, msg = gerador.gerar()
    if valido and mapa is not None:
        print(f"✓ Mapa gerado com sucesso: {msg}")
    else:
        print(f"✗ Falha ao gerar mapa: {msg}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Erro ao gerar mapa: {e}")
    sys.exit(1)

# ========== TESTE 3: Memória Partilhada ==========
print("\n[3/6] Testando memória partilhada...")
try:
    memoria = MemoriaPartilhada()
    # Testa registros
    memoria.registrar_explorada((1, 1), "L", grupo_id=0)
    memoria.registrar_tesouro((2, 2), grupo_id=0)
    memoria.registrar_bomba((3, 3), grupo_id=0)
    
    # Testa consultas
    assert memoria.celula_foi_explorada((1, 1), grupo_id=0)
    assert len(memoria.obter_tesouros(grupo_id=0)) > 0
    assert len(memoria.obter_bombas(grupo_id=0)) > 0
    
    print("✓ Memória partilhada funcionando corretamente!")
except Exception as e:
    print(f"✗ Erro em memória partilhada: {e}")
    sys.exit(1)

# ========== TESTE 4: Agentes ==========
print("\n[4/6] Testando agentes...")
try:
    memoria = MemoriaPartilhada()
    
    # Testa diferentes tipos de agentes
    agentes_teste = [
        ("BFS", AgenteBusca("A1", mapa, memoria, grupo_id=0)),
        ("Aleatório", AgenteAleatorio("A2", mapa, memoria, grupo_id=0)),
        ("Exploração", AgenteExploracao("A3", mapa, memoria, grupo_id=0)),
        ("KNN", AgenteKNN("A4", mapa, memoria, grupo_id=0)),
        ("Híbrido", AgenteHibrido("A5", mapa, memoria, grupo_id=0)),
        ("Adaptativo", AgenteAdaptativo("A6", mapa, memoria, grupo_id=0)),
        ("Combinado", AgenteCombinado("A7", mapa, memoria, grupo_id=0)),
    ]
    
    for nome, agente in agentes_teste:
        # Executa um turno
        agente.executar_turno()
        metricas = agente.obter_metricas()
        
        # Verifica se métricas foram criadas
        assert "passos" in metricas
        assert "eficiencia" in metricas
        assert agente.estado in [EstadoAgente.ATIVO, EstadoAgente.MORTO, EstadoAgente.COMPLETO]
        
        print(f"  ✓ {nome}: passaram no teste")
    
    print("✓ Todos os agentes funcionando corretamente!")
except Exception as e:
    print(f"✗ Erro ao testar agentes: {e}")
    sys.exit(1)

# ========== TESTE 5: Métricas ==========
print("\n[5/6] Testando sistema de métricas...")
try:
    gestor = GestorMetricas()
    grupo = gestor.criar_grupo(0, ModoJogo.A_TESOUROS, 10)
    
    # Adiciona agentes
    grupo.adicionar_agente("A1", "BFS")
    grupo.adicionar_agente("A2", "Aleatório")
    
    # Simula algumas ações
    grupo.registrar_passo_agente("A1")
    grupo.registrar_tesouro("A1")
    grupo.registrar_morte_agente("A2", 5)
    grupo.avanca_turno()
    
    # Verifica métricas
    assert grupo.obter_tesouros_coletados() == 1
    assert grupo.obter_agentes_mortos() == 1
    assert grupo.obter_agentes_vivos() == 1
    
    # Testa relatório
    relatorio = grupo.obter_relatorio_completo()
    assert "metricas_obrigatorias" in relatorio
    assert "metricas_adicionais" in relatorio
    
    print("✓ Sistema de métricas funcionando corretamente!")
except Exception as e:
    print(f"✗ Erro ao testar métricas: {e}")
    sys.exit(1)

# ========== TESTE 6: Integração Completa ==========
print("\n[6/6] Testando integração completa...")
try:
    # Simula pequena simulação
    memoria = MemoriaPartilhada()
    gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
    mapa_sim, _, _ = gerador.gerar()
    
    agentes_sim = [
        AgenteBusca("Ag1", mapa_sim, memoria, grupo_id=0),
        AgenteAleatorio("Ag2", mapa_sim, memoria, grupo_id=0),
    ]
    
    # Executa 5 turnos
    for turno in range(5):
        for agente in agentes_sim:
            if agente.estado == EstadoAgente.ATIVO:
                agente.executar_turno()
    
    # Verifica estado
    vivos = sum(1 for a in agentes_sim if a.estado == EstadoAgente.ATIVO)
    mortos = sum(1 for a in agentes_sim if a.estado == EstadoAgente.MORTO)
    
    print(f"  Turnos executados: 5")
    print(f"  Agentes vivos: {vivos}")
    print(f"  Agentes mortos: {mortos}")
    print("✓ Integração completa funcionando corretamente!")
except Exception as e:
    print(f"✗ Erro na integração: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ TODAS AS VALIDAÇÕES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\nA arquitetura está pronta para uso!")
