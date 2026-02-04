# Sistema de Múltiplos Grupos por Abordagem - Implementação

## Resumo das Mudanças

O sistema foi refatorado para suportar **múltiplos grupos com diferentes algoritmos dentro de cada abordagem** (A, B ou C), permitindo comparação de performance entre estratégias diferentes.

### Arquitetura

#### Estrutura de Dados Hierárquica

```
{
  abordagem_id (0, 1, 2):
    - grupo_id_1: 
        - estrategia: "Nome da Estratégia"
        - num_agentes: 5
        - tipos: ["AgenteBusca", "AgenteKNN", ...]
        - objetivo_alcancado: False
        - turno_conclusao: None
    - grupo_id_2: { ... }
    - grupo_id_3: { ... }
}
```

#### Métricas Hierárquicas

```
gestores_metricas:
  {
    abordagem_id:
      {
        grupo_id: GestorMetricas()
      }
  }
```

---

## Mudanças Implementadas

### 1. **GeradorAgentesAbordagem** (`gerador_por_abordagem.py`)

Adicionados 5 novos métodos para criar grupos com estratégias diferentes:

- `criar_grupo_bfs()` - Apenas agentes BFS puros
- `criar_grupo_knn()` - Apenas agentes KNN puros
- `criar_grupo_hibrido()` - Mistura: 2x BFS + 1x KNN
- `criar_grupo_hibrido_inverso()` - Mistura: 1x BFS + 2x KNN
- `criar_hibrido_balanceado()` - Mistura: 50% Aleatório + 50% KNN

### 2. **JanelaPrincipalMultiGrupo** (`janela_principal_multi_grupo.py`)

#### Mudança na Seleção de Abordagens
- ❌ **Antes**: Botões exclusivos (apenas 1 abordagem por vez)
- ✅ **Agora**: Checkboxes que permitem múltiplas abordagens

#### Nova Visualização de Métricas
- Dropdown `combo_visualizar` para selecionar qual abordagem visualizar
- Abas dinâmicas que mostram **apenas** os grupos da abordagem selecionada
- Cada grupo tem sua própria aba com métricas e agentes

#### Novos Métodos

```python
def _definir_estrategias_grupo(self, abordagem_id):
    """Define 3-4 estratégias de grupos para cada abordagem"""
    # Retorna lista de (estrategia_nome, factory) tuples

def _criar_painel_grupo(self, grupo_id, abordagem_id, estrategia_nome):
    """Cria painel de métricas para um grupo específico"""

def _atualizar_tabs_grupos(self):
    """Atualiza abas para mostrar grupos da abordagem selecionada"""

def _atualizar_metricas_grupo(self, grupo_id):
    """Atualiza métricas de um grupo (refatorado para trabalhar com hierarquia)"""
```

#### Estratégias por Abordagem

**Abordagem A (Tesouros):**
1. Grupo 1: 3x BFS
2. Grupo 2: 3x KNN
3. Grupo 3: 2x BFS + 1x KNN
4. Grupo 4: 1x BFS + 2x KNN

**Abordagem B (Sobrevivência):**
1. Grupo 1: 5x Aleatório Seguro (padrão)
2. Grupo 2: 7x Aleatório Seguro (agressivo)
3. Grupo 3: 3x Aleatório Seguro (conservador)

**Abordagem C (Bandeira):**
1. Grupo 1: 60% Aleatório, 30% KNN, 10% Híbrido
2. Grupo 2: 100% KNN (focado)
3. Grupo 3: 50% Aleatório, 50% KNN

---

## Fluxo de Execução

### Inicialização

1. Utilizador marca/desmarca checkboxes de abordagens
2. Clica "Iniciar Simulação"
3. Sistema determina abordagens selecionadas
4. Para cada abordagem, cria múltiplos grupos com estratégias diferentes
5. Cria visualização dinâmica (abas para cada grupo)
6. Inicia timer que executa turnos para **todos os grupos simultaneamente**

### Durante Simulação

1. Cada turno executa todos os grupos de todas as abordagens selecionadas
2. Métricas são atualizadas apenas para o grupo sendo visualizado
3. Combo dropdown permite mudar de abordagem (muda quais grupos aparecem)
4. Cada grupo tem sua própria aba com resumo e tabela de agentes

### Comparação de Resultados

Ao terminar, o sistema pode comparar desempenho dos grupos para determinar:
- Qual estratégia foi melhor por abordagem
- Tempo para completar objetivo
- Eficiência de exploração
- Taxa de mortalidade de agentes

---

## Benefícios da Nova Arquitetura

1. **Comparação de Algoritmos**: Testar múltiplas combinações em paralelo
2. **Análise Estatística**: Comparar performance entre estratégias
3. **Escalabilidade**: Fácil adicionar/remover estratégias
4. **Isolamento**: Cada grupo tem ambiente completamente isolado
5. **Visualização Clara**: Ver apenas o que se quer comparar

---

## Testes Realizados

✅ **test_strategies_simple.py** - Verifica se todos os métodos de estratégia existem
✅ **test_multi_groups_full.py** - Testa criação de múltiplos grupos e execução de turnos

### Resultado do Teste Completo:
- 3 abordagens selecionadas
- 7 grupos criados no total (3 em A, 2 em B, 2 em C)
- 38 agentes no total
- 3 turnos executados com sucesso
- Todos os grupos ativos e respondendo

---

## Próximas Melhorias (Opcionais)

- [ ] Implementar `_determinar_melhor_grupo()` para destacar melhor performance
- [ ] Adicionar gráficos de comparação de performance
- [ ] Salvar resultados em arquivo para análise posterior
- [ ] Exportar estatísticas detalhadas por grupo
