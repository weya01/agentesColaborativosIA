# 🚀 Quick Reference - Múltiplos Grupos por Abordagem

## Estrutura Rápida

### State Management
```python
# Métricas hierárquicas
self.gestores_metricas = {
    abordagem_id: {grupo_id: GestorMetricas()}
}

# Resultados por grupo
self.resultados_abordagens = {
    abordagem_id: {grupo_id: {"estrategia": "...", "num_agentes": 5, ...}}
}

# Painéis de cada grupo
self.tabs_grupos = {grupo_id: widget}
```

### Novos Métodos

| Método | Localização | Propósito |
|--------|------------|----------|
| `_definir_estrategias_grupo()` | JanelaPrincipalMultiGrupo | Define 3-4 estratégias por abordagem |
| `_criar_painel_grupo()` | JanelaPrincipalMultiGrupo | Cria painel para um grupo |
| `_atualizar_tabs_grupos()` | JanelaPrincipalMultiGrupo | Atualiza abas dinamicamente |
| `criar_grupo_bfs()` | GeradorAgentesAbordagem | Cria grupo BFS puro |
| `criar_grupo_knn()` | GeradorAgentesAbordagem | Cria grupo KNN puro |
| `criar_grupo_hibrido()` | GeradorAgentesAbordagem | Cria grupo híbrido (2BFS+1KNN) |

### Fluxo de Execução

```
Utilizador marca checkboxes
    ↓
Clica "Iniciar"
    ↓
iniciar_simulacao() detecta abordagens
    ↓
Para cada abordagem:
  - _definir_estrategias_grupo()
  - criar_grupo() para cada estratégia
  - Armazenar em gestores_metricas e resultados_abordagens
    ↓
_atualizar_tabs_grupos() cria abas dinâmicas
    ↓
Timer executa atualizar_turno()
    ↓
_atualizar_metricas_grupo() atualiza apenas visualizados
```

## Cheat Sheet

### Acessar métricas de um grupo
```python
abordagem_id = 0
grupo_id = 0
gestor = self.gestores_metricas[abordagem_id][grupo_id]
grupo_metricas = gestor.obter_grupo(grupo_id)
```

### Adicionar nova estratégia
```python
def _definir_estrategias_grupo(self, abordagem_id):
    if abordagem_id == 0:  # Abordagem A
        estrategias = [
            ("Minha Nova Estratégia", GeradorAgentesAbordagem.meu_novo_metodo),
            # ... outras
        ]
```

### Criar novo método de estratégia
```python
@staticmethod
def criar_meu_grupo(mapa, memoria, num_agentes=None):
    """Documentação"""
    if num_agentes is None:
        num_agentes = 5
    agentes = []
    for i in range(num_agentes):
        agente = MeuAgente(
            nome=f"Meu{i+1}",
            mapa=mapa,
            memoria_grupo=memoria,
            grupo_id=0
        )
        agentes.append(agente)
    return agentes
```

## Debugging

### Ver grupos criados
```python
for grupo_id in self.gerenciador.grupos.keys():
    print(f"Grupo {grupo_id}")
```

### Ver métricas de um grupo
```python
print(self.gestores_metricas[0][0].obter_grupo(0).obter_cobertura_mapa())
```

### Ver qual abordagem está sendo visualizada
```python
print(self.combo_visualizar.currentIndex())  # Retorna 0, 1 ou 2
```

### Forçar atualização de abas
```python
self._atualizar_tabs_grupos()
```

## Testes

### Executar testes
```bash
cd c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main

# Validar estratégias existem
python test_strategies_simple.py

# Testar criação múltiplos grupos
python test_multi_groups_full.py

# Testar fluxo completo
python test_full_workflow.py
```

### Adicionar novo teste
```python
# test_meu_teste.py
from simulacao.gerenciador_corridas import GerenciadorGrupos
from agentes.gerador_por_abordagem import GeradorAgentesAbordagem

gerenciador = GerenciadorGrupos()
gerenciador.criar_grupo(
    grupo_id=0,
    abordagem="A",
    modo=...,
    agentes_factory=GeradorAgentesAbordagem.criar_grupo_bfs,
    num_agentes=None
)
```

## Estrutura do Banco de Dados em Execução

Depois de iniciar simulação com Abordagens A e B:

```
gerenciador.grupos:
  0: {agentes: [...], mapa_original: ..., memoria: ...}  # Grupo A1
  1: {agentes: [...], mapa_original: ..., memoria: ...}  # Grupo A2
  2: {agentes: [...], mapa_original: ..., memoria: ...}  # Grupo A3
  3: {agentes: [...], mapa_original: ..., memoria: ...}  # Grupo B1
  4: {agentes: [...], mapa_original: ..., memoria: ...}  # Grupo B2

gestores_metricas:
  0:  # Abordagem A
    0: GestorMetricas()  # Grupo A1
    1: GestorMetricas()  # Grupo A2
    2: GestorMetricas()  # Grupo A3
  1:  # Abordagem B
    3: GestorMetricas()  # Grupo B1
    4: GestorMetricas()  # Grupo B2

resultados_abordagens:
  0:  # Abordagem A
    0: {estrategia: "3x BFS", num_agentes: 5, ...}
    1: {estrategia: "3x KNN", num_agentes: 5, ...}
    2: {estrategia: "2x BFS + 1x KNN", num_agentes: 3, ...}
  1:  # Abordagem B
    3: {estrategia: "5x Aleatório", num_agentes: 5, ...}
    4: {estrategia: "7x Aleatório", num_agentes: 7, ...}
```

## Variáveis Importantes

| Variável | Tipo | Significado |
|----------|------|------------|
| `self.abordagem_selecionada` | int (0-2) | Qual abordagem está sendo visualizada |
| `self.combo_visualizar.currentIndex()` | int | Índice selecionado no dropdown |
| `self.turno_atual` | int | Número de turno atual |
| `self.simulacao_ativa` | bool | Simulação em execução? |
| `self.tabs_grupos` | dict | {grupo_id: widget} |

## Callbacks Importantes

```python
# Quando combo muda
self.combo_visualizar.currentIndexChanged.connect(self._atualizar_visualizacao_abordagem)

# Quando timer dispara (a cada 200ms por padrão)
self.timer.timeout.connect(self.atualizar_turno)

# Quando botão clicado
self.btn_iniciar.clicked.connect(self.iniciar_simulacao)
```

## Logs Importantes

```
"✅ Grupo X: N agentes criados"
"📊 Visualizando Abordagem X"
"✅ Abas atualizadas para Abordagem X"
"▶ Simulação ativa"
"✓ Simulação completa!"
```

---

**Para questões técnicas, ver IMPLEMENTACAO_MULTIPLOS_GRUPOS.md**
**Para usar a interface, ver GUIA_USO_MULTIPLOS_GRUPOS.md**
