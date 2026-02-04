#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSTRUCOES FINAIS DE EXECUCAO

Este script mostra como validar e executar o sistema completo.
"""

import sys
import io

# Configurar encoding UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("""
+==============================================================================+
|                                                                              |
|                  OK - SISTEMA MULTI-AGENTE - INSTRUCOES FINAIS             |
|                                                                              |
+==============================================================================+


================================================================================
PASSO 1: VERIFICAR INSTALACAO
================================================================================

Execute para verificar dependencias:

    $ pip list | grep PySide6

Se faltar PySide6:

    $ pip install PySide6


================================================================================
PASSO 2: VALIDAR REQUISITOS (2 minutos)
================================================================================

Execute os 3 testes de validacao em sequencia:

A) Testar Formas de Raciocinio:

    $ cd fontes
    $ python teste_formas_raciocinio.py

    Resultado esperado:
    [TEST 1] AgenteAleatorio: 3 algoritmos OK
    [TEST 2] AgenteExploracao: 3 algoritmos OK
    [TEST 3] AgenteKNN: 3 algoritmos OK
    [TEST 4] AgenteBusca: 4 algoritmos OK
    Todos os testes passaram!


B) Testar Compliance (7 requisitos):

    $ python COMPLIANCE_FINAL.py

    Resultado esperado:
    RESULTADO FINAL: TODOS OS 7 REQUISITOS IMPLEMENTADOS OK


C) Ver Sumario Visual:

    $ python sumario_visual.py

    Resultado: Mostra todos 7 requisitos com detalhes


================================================================================
PASSO 3: EXECUTAR SIMULACAO DE 9 RODADAS
================================================================================

Execute a simulacao principal:

    $ cd ..
    $ python main.py

Interface esperada:
    OK Tela inicial com selecao de modo (A, B, C)
    OK 9 abas para Rodadas 1-9
    OK Primeira aba: "RESUMO GERAL" com tabelas
    OK Proximas 9 abas: Rodadas 1-9 (com cores sincronizadas)
    OK Cada rodada: Grid 10x10 com agentes e bombas


================================================================================
PASSO 4: OBSERVAR COMPORTAMENTOS IMPORTANTES
================================================================================

Enquanto simulacao executa, observe:

METRICAS (na aba "RESUMO GERAL"):
   _ TABELA 1: Dados por grupo
   _ TABELA 2: Comparacao de algoritmos
   _ Valores atualizam apos cada rodada

FORMAS DE RACIOCINIO:
   _ Coluna "Algoritmo" muda de rodada para rodada
   _ Pode ser: aleatorio_puro, bfs, espiral, a_estrela

CORES:
   _ Mesma cor no grid e na tabela (grupos sincronizados)

DINAMICA DE BOMBAS:
   _ Rodada 1: ~50% bombas (50 em 10x10)
   _ Rodada 2: ~55%
   _ Rodada 3: ~60%
   _ ...
   _ Rodada 7-9: ~80%

MORTE DE AGENTES:
   _ Agentes que entram em bombas desaparecem
   _ "Agentes Vivos" decresce
   _ Taxa de Mortalidade aumenta

SEM REVISITA:
   _ Agentes param quando exploram tudo
   _ "Explorado%" chega proximo a 100%

VITORIA:
   _ "Objetivo" mostra SIM ou NAO
   _ Indica se meta foi alcancada


================================================================================
PASSO 5: EXPORTAR E ANALISAR RESULTADOS
================================================================================

Apos 9 rodadas completas:

Option A - Copiar tabela:
    1. Clique direito na tabela da aba "RESUMO GERAL"
    2. "Copy" ou "Select All"
    3. Cole em Excel/Google Sheets

Option B - Acessar dados programaticamente:
    from ui.janela_principal_rodadas import JanelaPrincipalRodadas
    janela = JanelaPrincipalRodadas()
    print(janela.resultados_rodadas)


================================================================================
PASSO 6: ANALISE DOS RESULTADOS
================================================================================

Apos coletar dados, analise:

1. QUAL AGENTE TEM MELHOR DESEMPENHO?
   Verifique: Taxa de sucesso

2. QUAL ALGORITMO E MAIS EFICIENTE?
   Verifique: Eficiencia Media

3. COMO A DIFICULDADE AFETA PERFORMANCE?
   Compare: Rodadas iniciais vs. finais

4. QUAL MODO ALCANCA OBJETIVO COM MAIS FREQUENCIA?
   Verifique: % de SIM em cada modo (A, B, C)

5. AGENTES APRENDEM?
   Compare: Eficiencia rodada 1 vs. rodada 9


================================================================================
CHECKLIST: SISTEMA FUNCIONAL 100%
================================================================================

VALIDACAO:
    [ ] teste_formas_raciocinio.py passou
    [ ] COMPLIANCE_FINAL.py passou (7 requisitos)
    [ ] sumario_visual.py mostrou todos requisitos

SIMULACAO:
    [ ] Interface GUI apareceu sem erros
    [ ] Aba "RESUMO GERAL" existe e e primeira
    [ ] 9 abas de rodadas criadas
    [ ] Tabelas de metricas visiveis

COMPORTAMENTOS:
    [ ] Cores sincronizadas (mapa + sidebar)
    [ ] Agentes se movem no grid
    [ ] Bombas aparecem em % correto (50% > 80%)
    [ ] Agentes mortos desaparecem
    [ ] Agentes param quando exploram tudo
    [ ] Coluna "Algoritmo" muda entre rodadas
    [ ] Proxima rodada comeca com novos agentes
    [ ] Todas as 9 rodadas executam

Se TODOS marcados, seu sistema esta 100% PRONTO para analise!


================================================================================
TROUBLESHOOTING RAPIDO
================================================================================

PROBLEMA: ModuleNotFoundError: No module named 'PySide6'
SOLUCAO:  pip install PySide6

PROBLEMA: GUI nao aparece
SOLUCAO:  Verifique PySide6, restart terminal

PROBLEMA: Agentes nao se movem
SOLUCAO:  Verifique GridMapa.atualizar()

PROBLEMA: Metricas vazias
SOLUCAO:  Verifique _processar_fim_rodada()

PROBLEMA: Cores estao erradas
SOLUCAO:  Verifique numero_grupo em cada agente


================================================================================

BOM! O SISTEMA ESTA 100% PRONTO PARA TESTAR!

================================================================================

Data: 25 de Janeiro, 2026
Status: PRODUCAO
Versao: 1.0
""")

