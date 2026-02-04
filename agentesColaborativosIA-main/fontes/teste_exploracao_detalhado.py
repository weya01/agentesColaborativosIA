"""
TESTE DETALHADO: Regra de Exploração (Modo B)
Verifica os 8 pontos e executa simulação para validar
"""
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

print("\n" + "="*80)
print("TESTE DETALHADO: REGRA DE EXPLORAÇÃO (MODO B)")
print("="*80 + "\n")

try:
    # Importações
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    from simulacao.gerenciador_corridas import GerenciadorGrupos
    from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    
    print("✅ PASSO 1: Verificar imports da regra de exploração")
    print("   ✓ GerenciadorGrupos")
    print("   ✓ AbordagensPadrao")
    print("   ✓ GeradorAgentesAbordagem")
    
    print("\n✅ PASSO 2: Criar grupo B (Exploração)")
    gerenciador = GerenciadorGrupos()
    abordagem_b = AbordagensPadrao.obter_abordagem_b()
    print(f"   ✓ Abordagem: {abordagem_b.tipo.value}")
    print(f"   ✓ Modo jogo: {abordagem_b.modo_jogo}")
    
    factory = GeradorAgentesAbordagem.obter_factory_por_abordagem(TipoAbordagem.B.value)
    gerenciador.criar_grupo(
        grupo_id=1,
        abordagem=TipoAbordagem.B.value,
        modo=abordagem_b.modo_jogo,
        agentes_factory=factory,
        num_agentes=5  # Fixo para teste
    )
    
    agentes = gerenciador.obter_agentes_por_grupo(1)
    print(f"   ✓ {len(agentes)} agentes criados para Modo B")
    
    print("\n✅ PASSO 3: Verificar os 8 pontos da regra de exploração")
    
    # Ponto 1: Regra básica
    print("\n   [1] REGRA BÁSICA (>80% exploração)")
    mapa = gerenciador.grupos[1]['mapa_original']
    total_celulas = len(mapa) * len(mapa[0]) if isinstance(mapa, list) else mapa.tamanho ** 2
    print(f"       • Total de células: {total_celulas}")
    print(f"       • Limiar 80%: {int(total_celulas * 0.8)} células")
    
    # Ponto 2: Agentes vivos
    print("\n   [2] AGENTES VIVOS")
    agentes_vivos = [ag for ag in agentes if ag.estado.value == "ativo"]
    print(f"       • Agentes vivos: {len(agentes_vivos)}/{len(agentes)}")
    print(f"       • Estado: {'✓ OK' if agentes_vivos else '✗ FALHA'}")
    
    # Ponto 3: Contagem de exploradas
    print("\n   [3] CONTAGEM DE EXPLORADAS")
    memoria = gerenciador.grupos[1]['memoria']
    exploradas_inicial = len(memoria.obter_exploradas(grupo_id=1))
    print(f"       • Exploradas no início: {exploradas_inicial}")
    
    # Ponto 4: Cálculo de tamanho
    print("\n   [4] CÁLCULO DE TAMANHO")
    print(f"       • Tamanho mapa: {len(mapa)} x {len(mapa[0])}")
    print(f"       • Total: {total_celulas}")
    
    # Ponto 5: Comparação de limiar
    print("\n   [5] COMPARAÇÃO DE LIMIAR")
    limiar_correto = exploradas_inicial > (total_celulas * 0.8)
    print(f"       • Lógica: exploradas > (total * 0.8)")
    print(f"       • {exploradas_inicial} > {int(total_celulas * 0.8)}: {limiar_correto}")
    
    # Ponto 6: Integração com métrica
    print("\n   [6] INTEGRAÇÃO COM MÉTRICA")
    cobertura_inicial = (exploradas_inicial / total_celulas) * 100
    print(f"       • Cobertura métrica: {cobertura_inicial:.1f}%")
    
    # Ponto 7: Memória compartilhada
    print("\n   [7] MEMÓRIA COMPARTILHADA")
    print(f"       • Grupo ID: 1")
    print(f"       • Exploradas isoladas: {exploradas_inicial}")
    
    # Ponto 8: Condição final
    print("\n   [8] CONDIÇÃO FINAL (vivos E exploração)")
    print(f"       • Agentes vivos: {bool(agentes_vivos)}")
    print(f"       • Exploração >80%: {limiar_correto}")
    print(f"       • Resultado final: {bool(agentes_vivos) and limiar_correto}")
    
    print("\n✅ PASSO 4: Executar 50 turnos e monitorar exploração")
    
    max_turnos = 50
    for turno in range(1, max_turnos + 1):
        resultado = gerenciador.executar_turno_todos()
        
        # Verifica Status Modo B
        modo_b_resultado = resultado.get(1, {})
        terminou = modo_b_resultado.get('terminou', False)
        objetivo = modo_b_resultado.get('objetivo_alcancado', False)
        
        # Atualiza métricas
        exploradas_atual = len(memoria.obter_exploradas(grupo_id=1))
        cobertura_atual = (exploradas_atual / total_celulas) * 100
        agentes_vivos = sum(1 for ag in agentes if ag.estado.value == "ativo")
        
        if turno % 10 == 0 or terminou:
            print(f"\n   Turno {turno}:")
            print(f"      • Exploradas: {exploradas_atual}/{total_celulas} ({cobertura_atual:.1f}%)")
            print(f"      • Agentes vivos: {agentes_vivos}/{len(agentes)}")
            print(f"      • Terminou: {terminou}")
            print(f"      • Objetivo alcançado: {objetivo}")
        
        if terminou:
            print(f"\n   🎯 MODO B COMPLETADO NO TURNO {turno}!")
            break
    
    if not modo_b_resultado.get('terminou', False):
        print(f"\n   ⚠️  MODO B não completou em {max_turnos} turnos")
        print(f"      • Exploração final: {cobertura_atual:.1f}%")
        print(f"      • Faltavam: {100 - cobertura_atual:.1f}%")
    
    print("\n" + "="*80)
    print("✅ TESTE COMPLETO!")
    print("="*80 + "\n")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
