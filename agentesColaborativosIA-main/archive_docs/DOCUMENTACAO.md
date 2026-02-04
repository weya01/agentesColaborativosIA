"""
Documentação da Arquitetura de Agentes Colaborativos
=====================================================

## Visão Geral

Este projeto implementa um sistema de agentes colaborativos heterogêneos para exploração 
de mapas em ambiente 10x10. A arquitetura segue o padrão de Inteligência Artificial 
com ciclo de IA completo: Percepção → Memória → Decisão → Ação.

## Estrutura do Projeto

### /fontes/agentes/
Sistema completo de agentes organizados hierarquicamente:

#### /base/
- **agente_base.py**: Classe abstrata que implementa o ciclo de IA para todos os agentes
  - Ciclo: percepção() → atualizar_memoria() → decisao() → executar_acao()
  - Estados: ATIVO, MORTO, COMPLETO
  - Métricas: passos, bombas, tesouros, células exploradas, eficiência

#### /agentes_busca/
Agentes que usam algoritmos de busca formal:
- **AgenteBusca**: 4 algoritmos (BFS, DFS, Gulosa, A*) com seleção dinâmica
- **AgenteArvoreBusca**: Busca em árvore com limite de profundidade

#### /agentes_nao_busca/
Agentes com estratégias não-formais:
- **AgenteAleatorio**: Movimento aleatório (2 variantes: puro, seguro)
- **AgenteExploracao**: Exploração dirigida (espiral, camadas, dirigida)
- **AgenteKNN**: K-Vizinhos Mais Próximos (3 variantes: puro, peso, ponderado)

#### /agentes_hibridos/
Agentes que combinam múltiplas estratégias:
- **AgenteHibrido**: Alterna entre BFS e exploração aleatória
- **AgenteAdaptativo**: Auto-melhoria com tracking de sucesso por algoritmo
- **AgenteCombinado**: Votação ponderada de 3 estratégias

#### memoria_partilhada.py
- Sistema de memória com isolamento por grupo
- Rastreia: bombas, tesouros, bandeira, células exploradas/seguras
- Histórico completo de eventos
- Métodos: registrar_*, obter_*, consultar_*, limpar_*

### /fontes/ambientes/
Gerenciamento de mapas:

#### gerador_de_mapa.py
- **GeradorDeMapa**: Cria mapas aleatórios para cada modo
  - Modo A (Tesouros): 25% bombas, 35% tesouros
  - Modo B (Sobrevivência): 55% bombas, 15% tesouros
  - Modo C (Bandeira): 45% bombas, bandeira aleatória
- **Mapa**: Interface de consulta (ver célula, vizinhos, distância)

#### validador.py
- **ValidadorMapa**: Valida mapas antes de usar
  - Verifica conectividade por flood-fill
  - Valida acessibilidade de objetivos
  - Gera relatório de integridade

#### manutencao_mapa.py
- **GeradorMapaValido**: Wrapper que gera mapas garantidamente válidos
  - Tenta até 50 vezes se necessário
  - Retorna relatório de validação

### /fontes/metricas/
Sistema de rastreamento de desempenho:

#### metricas.py
- **MetricasAgente**: Rastreia individual:
  - Passos, bombas, tesouros, células, eficiência
  - Histórico de movimentos e decisões
  - Algoritmos usados e frequência

- **MetricasGrupo**: Agrupa métricas:
  - 7 métricas obrigatórias (tesouros, células, tempo, agentes, bandeira, algoritmos)
  - 6 métricas adicionais (eficiência, mortalidade, cobertura, etc.)
  - Relatórios completos e resumos visuais

#### gestor_metricas.py
- **GestorMetricas**: Coordena múltiplos grupos
  - Comparação entre grupos
  - Ranking de agentes
  - Exportação em JSON

### /fontes/ui/
Interface gráfica com PySide6:

#### janela_principal.py
- Configuração de simulação (modo, tipo agente, velocidade)
- Display do mapa
- Painel de métricas com 3 abas (Resumo, Agentes, Detalhes)
- Controles (iniciar, pausar, resetar, exportar)

#### Outros arquivos
- grid_mapa.py: Renderização do mapa
- cores.py: Paleta de cores
- painel_interacao.py: Controles de interação

### /fontes/utils/
- constantes.py: ModoJogo enum e constantes

## Como Usar

### 1. Executar a Aplicação GUI

```bash
cd fontes
python main.py
```

Abre interface gráfica para:
1. Selecionar modo de jogo
2. Escolher tipo de agente
3. Configurar número de agentes (1-10)
4. Ajustar velocidade de simulação
5. Executar e visualizar em tempo real
6. Exportar métricas em JSON

### 2. Teste de Validação

```bash
python validar_arquitetura.py
```

Executa 6 testes:
1. Imports de todos os módulos
2. Geração de mapas
3. Memória partilhada
4. Agentes individuais
5. Sistema de métricas
6. Integração completa

### 3. Uso Programático

```python
from fontes.utils.constantes import ModoJogo
from fontes.ambientes import GeradorMapaValido
from fontes.agentes.memoria_partilhada import MemoriaPartilhada
from fontes.agentes.agentes_busca.agente_busca import AgenteBusca
from fontes.metricas import GestorMetricas

# Gera mapa válido
gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
mapa, relatorio = gerador.gerar_com_relatorio()

# Cria memória e agentes
memoria = MemoriaPartilhada()
agentes = [
    AgenteBusca("A1", mapa, memoria, grupo_id=0),
    AgenteBusca("A2", mapa, memoria, grupo_id=0),
]

# Cria métricas
gestor = GestorMetricas()
grupo = gestor.criar_grupo(0, ModoJogo.A_TESOUROS, 10)
for agente in agentes:
    grupo.adicionar_agente(agente.id, agente.__class__.__name__)

# Executa simulação
for turno in range(100):
    for agente in agentes:
        agente.executar_turno()
    grupo.avanca_turno()
    
    # Verifica objetivo
    if grupo.obter_tesouros_coletados() >= 10:
        grupo.registrar_objetivo_alcancado()
        break

# Obtém relatório
print(grupo.obter_resumo_visual())
```

## Ciclo de IA em Detalhe

Cada agente executa este ciclo a cada turno:

```
┌─────────────────────────────────────┐
│     EXECUTAR_TURNO (Principal)      │
└──────────────┬──────────────────────┘
               │
    ┌──────────v──────────┐
    │   1. PERCEPÇÃO      │
    │  _percepcao()       │
    │  Observa célula     │
    │  e vizinhos         │
    └──────────┬──────────┘
               │
    ┌──────────v──────────────────┐
    │  2. ATUALIZAR MEMÓRIA       │
    │  _atualizar_memoria()       │
    │  Registra na memória:       │
    │  - Explorada                │
    │  - Bomba/Tesouro/Bandeira   │
    │  - Célula segura            │
    │  - Vizinhos percebidos      │
    └──────────┬──────────────────┘
               │
    ┌──────────v────────────────────┐
    │  3. DECISÃO                    │
    │  _decidir_acao_interna()       │
    │  (Implementado por subclasses) │
    │  Retorna: "CIMA"/"BAIXO"/etc.  │
    └──────────┬────────────────────┘
               │
    ┌──────────v──────────────────┐
    │   4. AÇÃO                    │
    │  _executar_acao()            │
    │  - Move agente               │
    │  - Avalia célula             │
    │  - Pode morrer/completar     │
    └──────────┬──────────────────┘
               │
               └──────────────────────>
```

## Métricas Obrigatórias (7)

1. **Tesouros Coletados**: Total de tesouros coletados pelo grupo
2. **Células Exploradas**: Quantidade de células únicas visitadas
3. **Tempo Decorrido**: Número de turnos executados
4. **Agentes Vivos**: Quantos agentes ainda estão ativos
5. **Agentes Mortos**: Quantos agentes foram mortos em bombas
6. **Bandeira Encontrada**: Se objetivo C foi alcançado (sim/não)
7. **Algoritmos Usados**: Quais algoritmos foram usados e frequência

## Modos de Jogo

| Modo | Nome | Objetivo | Bombas | Tesouros |
|------|------|----------|--------|----------|
| A | Tesouros | Coletar 50% dos tesouros | 25% | 35% |
| B | Sobrevivência | Explorar 100% + sobreviver | 55% | 15% |
| C | Bandeira | Encontrar bandeira | 45% | 0% |

## Exemplos de Tipos de Agentes

- **BFS**: Algoritmo de busca em largura, encontra caminho mais curto
- **Aleatório Seguro**: Movimento aleatório evitando bombas conhecidas
- **Exploração Espiral**: Explora em padrão espiral a partir do centro
- **KNN**: Vai em direção aos tesouros mais próximos
- **Híbrido**: BFS para tesouros próximos, aleatório para exploração
- **Adaptativo**: Aprende qual algoritmo funciona melhor
- **Combinado**: Vota entre 3 estratégias para melhor ação

## Requisitos

- Python 3.8+
- PySide6 (para GUI)
- collections (standard library)
- pathlib (standard library)

Instalar dependências:
```bash
pip install PySide6
```

## Estrutura de Pastas Esperada

```
agentesColaborativosIA-main/
├── fontes/
│   ├── main.py
│   ├── validar_arquitetura.py
│   ├── agentes/
│   │   ├── __init__.py
│   │   ├── memoria_partilhada.py
│   │   ├── base/
│   │   ├── agentes_busca/
│   │   ├── agentes_nao_busca/
│   │   └── agentes_hibridos/
│   ├── ambientes/
│   │   ├── __init__.py
│   │   ├── gerador_de_mapa.py
│   │   ├── validador.py
│   │   └── manutencao_mapa.py
│   ├── metricas/
│   │   ├── __init__.py
│   │   ├── metricas.py
│   │   └── gestor_metricas.py
│   ├── ui/
│   │   ├── janela_principal.py
│   │   ├── grid_mapa.py
│   │   └── ...
│   └── utils/
│       └── constantes.py
└── README.md
```

## Notas de Implementação

- ✅ Ciclo de IA completo em cada agente
- ✅ Memória com isolamento por grupo
- ✅ 7 tipos de agentes com múltiplos algoritmos
- ✅ 7 métricas obrigatórias + adicionais
- ✅ Interface gráfica interativa
- ✅ Mapas gerados e validados
- ✅ Sistema de exportação de dados

## Autores e Versão

Versão: 2.0 (Refatorada)
Projeto Acadêmico: Agentes Colaborativos para Exploração de Mapas

"""
