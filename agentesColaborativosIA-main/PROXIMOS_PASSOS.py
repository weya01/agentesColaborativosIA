#!/usr/bin/env python
"""
PRÓXIMOS PASSOS: Como Testar o Sistema Completo
================================================
"""

guide = """

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🚀 GUIA: TESTANDO O SISTEMA COMPLETAMENTE                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


PASSO 1: Validar Forma de Raciocínio
════════════════════════════════════════════════════════════════════════════════

Execute o teste de verificação:

    $ cd fontes
    $ python teste_formas_raciocinio.py

Resultado Esperado:
    [TEST 1] AgenteAleatorio: ✅ 3 algoritmos
    [TEST 2] AgenteExploracao: ✅ 3 algoritmos
    [TEST 3] AgenteKNN: ✅ 3 algoritmos
    [TEST 4] AgenteBusca: ✅ 4 algoritmos
    [TEST 5] AgenteHibrido: ✅ COMPLETO
    ✅ TODOS OS TESTES PASSARAM!


PASSO 2: Validar Compliance
════════════════════════════════════════════════════════════════════════════════

Execute o relatório de compliance:

    $ python COMPLIANCE_FINAL.py

Resultado Esperado:
    ✅ TODOS OS 7 REQUISITOS IMPLEMENTADOS
    - Formas de Raciocínio (3+)
    - Métricas Visíveis
    - Sem Revisita de Células
    - Agentes Mortos Desaparecem
    - Cores Sincronizadas
    - Percentuais de Bomba Dinâmicos
    - Vitória Funcional


PASSO 3: Iniciar Simulação de 9 Rodadas
════════════════════════════════════════════════════════════════════════════════

Execute o aplicativo principal:

    $ python ui/main.py

Ou use o script de inicialização:

    $ python main.py

Interface Esperada:
    1. Tela inicial com seleção de modo (A, B, C)
    2. 9 abas de rodadas (1 a 9)
    3. Para cada rodada:
       - Aba "📊 RESUMO GERAL" aparece PRIMEIRO
       - Tabelas de métricas visíveis
       - Grupos com cores sincronizadas
       - Mapa com 10x10 grid
       - Barra de progresso


PASSO 4: Observar Comportamentos
════════════════════════════════════════════════════════════════════════════════

✅ FORMAS DE RACIOCÍNIO (verificar qual está ativo)
   - Cada rodada começa com algoritmo diferente ou mesmo
   - Coluna "Algoritmo" na tabela mostra qual está em uso
   - Pode ser: aleatorio_puro, aleatorio_seguro, espiral, bfs, a_estrela, etc.

✅ MÉTRICAS (por rodada)
   - Explorado%: Deve começar em 0% e aumentar
   - Agentes Vivos: Começa com 2, pode cair conforme rodadas
   - Eficiência: Explorado / Passos (deve ser > 0)
   - Taxa Mortalidade: % de agentes que morreram

✅ SEM REVISITA DE CÉLULAS
   - Agentes param de se mover quando exploram tudo
   - Se houver reinicializações, volta a explorar
   - Campo "Agentes Parados" pode aumentar

✅ AGENTES MORTOS
   - Quando vida <= 0, agentes desaparecem do mapa
   - "Agentes Vivos" decresce
   - Taxa de Mortalidade aumenta

✅ CORES SINCRONIZADAS
   - Mesma cor no mapa e no sidebar para cada grupo
   - Cores diferentes para grupos diferentes

✅ DINÂMICA DE BOMBAS
   - Rodada 1: ~50% (50 bombas em 10x10)
   - Rodada 2: ~55% (55 bombas)
   - ...
   - Rodada 7-9: ~80% (80 bombas)

✅ VITÓRIA
   - Se objetivo alcançado, mostra "SIM" na coluna
   - Se morrem todos, mostra "NÃO"
   - Modo varia conforme seleção inicial


PASSO 5: Analisar Comparação de Algoritmos
════════════════════════════════════════════════════════════════════════════════

Na aba "📊 RESUMO GERAL", verifique a TABELA 2:

    Algoritmo | Usos | Sucessos | Taxa% | Efic. Média
    ──────────┼──────┼──────────┼───────┼────────────
    bfs       |  3   |    2     |  66%  |   0.45
    dfs       |  3   |    2     |  66%  |   0.42
    knn_puro  |  3   |    1     |  33%  |   0.38
    espiral   |  2   |    2     |  100% |   0.51

    Análise:
    • Usos: Quantas rodadas usou esse algoritmo
    • Sucessos: Quantas vezes conseguiu objetivo
    • Taxa%: Sucesso / Usos * 100
    • Efic. Média: Eficiência média ao usar esse algoritmo


PASSO 6: Exportar Resultados (Opcional)
════════════════════════════════════════════════════════════════════════════════

Após as 9 rodadas, salve os dados:

    1. Clique com botão direito na tabela
    2. "Copiar tabela" ou "Exportar como CSV"
    3. Cole em planilha (Excel, Google Sheets, etc.)
    4. Gere gráficos de progressão

Ou acesse diretamente:

    # No código Python, após simulação:
    print(janela.resultados_rodadas)  # Dicionário com todos os dados


PASSO 7: Verificar Logs e Debug (Se Necessário)
════════════════════════════════════════════════════════════════════════════════

Se algo não funcionar como esperado:

    1. Verifique erros na console (Debug Console)
    2. Procure por: "ERROR", "Exception", "Traceback"
    3. Se agente não move:
       - Verifique: celulas_exploradas está crescendo?
       - Verifique: esta_vivo() retorna True?
       - Verifique: há posições válidas no grid?

    4. Se cores não sincronizam:
       - Verifique: numero_grupo está definido?
       - Verifique: cores_grupos tem tamanho certo?

    5. Se métricas não aparecem:
       - Verifique: _criar_aba_resumo_geral() foi chamado?
       - Verifique: resultados_rodadas está sendo populado?


PASSO 8: Casos Extremos para Testar
════════════════════════════════════════════════════════════════════════════════

1. RODADA COM 100% MORTALIDADE
   - Se agentes morrem todos, objetivo = NÃO
   - Agentes Vivos = 0
   - Taxa Mortalidade = 100%
   - Próxima rodada começa com novos agentes

2. RODADA COM EXPLORAÇÃO MÁXIMA
   - Se exploram 100%, Eficiência deve ser máxima
   - Espera-se: Explorado% = 100%
   - Agentes devem parar de se mover

3. RODADA COM SWITCHING DE ALGORITMO
   - Algumas rodadas podem usar algoritmos diferentes
   - Coluna "Algoritmo" deve refletir isso
   - Taxa de sucesso pode variar

4. RODADA COM OBJETIVO ALCANÇADO
   - "Objetivo" = SIM significa meta atingida
   - Pode continuar para próxima rodada
   - Dificuldade aumenta (+5% bombas)


CHECKLIST FINAL
════════════════════════════════════════════════════════════════════════════════

Após executar completo, verifique:

    [ ] Teste de Formas de Raciocínio passou
    [ ] Compliance Final passou (7 requisitos)
    [ ] Simulação começou sem erros
    [ ] Aba "RESUMO GERAL" apareceu primeiro
    [ ] Tabelas de métricas visíveis
    [ ] Cores sincronizadas (mapa + sidebar)
    [ ] Agentes se movem no grid
    [ ] Bombas mostram em % certo (50% → 80%)
    [ ] Agentes param quando esgotam células
    [ ] Agentes mortos desaparecem
    [ ] Próxima rodada começa com novos agentes
    [ ] Dificuldade aumenta (mais bombas)
    [ ] Tabela de comparação de algoritmos aparece
    [ ] Todas as 9 rodadas executam

Se TODOS ✅, o sistema está 100% PRONTO!


TROUBLESHOOTING RÁPIDO
════════════════════════════════════════════════════════════════════════════════

PROBLEMA: ImportError: cannot import ...
SOLUÇÃO:  Verifique __pycache__, delete-o:
          $ rm -rf fontes/__pycache__
          $ python -m pip install --upgrade pip

PROBLEMA: GUI não aparece
SOLUÇÃO:  Verifique PySide6:
          $ pip install PySide6

PROBLEMA: Agentes não se movem
SOLUÇÃO:  Verifique GridMapa.atualizar() está sendo chamado

PROBLEMA: Métricas vazias
SOLUÇÃO:  Verifique _processar_fim_rodada() antes de limpar grupos

PROBLEMA: Cores estão erradas
SOLUÇÃO:  Verifique numero_grupo em cada agente

════════════════════════════════════════════════════════════════════════════════

Depois de tudo funcionar, você terá:

    ✅ 9 rodadas de dados
    ✅ Comparação de 6+ tipos de agentes
    ✅ Análise de 20+ algoritmos diferentes
    ✅ Métricas de desempenho por rodada
    ✅ Progressão de dificuldade (50%→80% bombas)
    ✅ Demonstração de aprendizado/adaptação

🎉 SUCESSO!

════════════════════════════════════════════════════════════════════════════════
"""

print(guide)
