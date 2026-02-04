# SISTEMA REFINADO - RODADAS PROGRESSIVAS COM ISOLAMENTO DE GRUPOS

## 🎯 OBJETIVO ALCANÇADO

Sistema completamente refactorizado com as seguintes melhorias implementadas:

### 1. **Separação em Rodadas (em vez de "Turnos")**
- Cada rodada representa um escalamento de dificuldade
- Rodada 1 → 9 com progressão clara de agentes (2→10)
- Cada rodada tem limite de 200 turnos

### 2. **Sistema Progressivo de Escalamento**
- **Rodada 1**: 2 agentes, 50% bombas
- **Rodada 2**: 3 agentes, 53.75% bombas
- **Rodada 3**: 4 agentes, 57.50% bombas
- ...continuação linear...
- **Rodada 9**: 10 agentes, 80% bombas

Fórmula: `bombas(%) = 50 + (30 × (agentes - 2) / 8)`

### 3. **Grupos Isolados mas Simultâneos**
- Todos os grupos começam com **MESMO número de agentes** por rodada
- Grupos **NÃO SE INFLUENCIAM** (ambientes lógicos isolados)
- Grupos executam **SIMULTANEAMENTE** nos mesmos turnos
- Cores diferentes para identificação visual no mapa

### 4. **Interface Completamente Redesenhada**
✅ **Removido**: 3 botões de abordagem que não eram elegantes
✅ **Adicionado**: Seletor único de "Visualizar:" para trocar entre abordagens
✅ **Cleaner**: Layout mais profissional e intuitivo
✅ **Labels Claros**: Rodada, Agentes, Bombas, Turno em tempo real

### 5. **Comportamento dos Agentes Corrigido**
- Agentes se movem corretamente pelo mapa
- Exploram células novas com prioridade
- Evitam bombas conhecidas
- Coletam tesouros
- Sistema de métricas funcional

### 6. **Métricas Claras e Detalhadas**
Exibidas em tempo real para cada grupo:
- Objetivo da abordagem
- Turno atual
- Percentual explorado
- Taxa de mortalidade
- Eficiência de exploração
- Tabela com status de cada agente:
  - ID, Tipo, Status (VIVO/MORTO)
  - Passos dados, Tesouros coletados, Eficiência

---

## 📁 ARQUIVOS MODIFICADOS/CRIADOS

### Novos Arquivos:
```
fontes/ui/janela_principal_rodadas.py
├── Interface completa com sistema de rodadas
├── Gestão de múltiplos grupos simultâneos
├── Cores diferentes para cada grupo (até 10)
└── Sistema de métricas em tempo real

fontes/teste_rodadas.py
├── Validação da fórmula de escalamento
└── Tabela de progressão

fontes/teste_interface_rodadas.py
├── Validação de componentes
├── Teste de criação de grupos
└── Teste de execução de turnos

fontes/teste_comportamento_agentes.py
├── Teste detalhado de movimento de agentes
├── Validação de exploração
├── Teste com múltiplas abordagens
└── Estatísticas finais

fontes/rodar_interface.py
└── Script para executar a interface completa
```

### Arquivos Modificados:
```
fontes/ui/janela_principal_clean.py
└── Redireciona para janela_principal_rodadas em vez de janela_principal_multi_grupo
```

---

## 🚀 COMO USAR

### 1. Iniciar a Aplicação
```bash
cd fontes
python main.py
```

### 2. Na Interface
1. **Selecionar Abordagens**: Clique em A, B, e/ou C (Ctrl+Click para múltiplas)
   - 🟢 A: Tesouros (coletar tesouros + bandeira)
   - 🔵 B: Sobrevivência (explorar 80% do mapa)
   - 🟠 C: Bandeira (apenas atingir bandeira)

2. **Escolher Velocidade**: Dropdown de 0ms a 1000ms por turno

3. **Iniciar**: Clique em "▶ INICIAR SIMULAÇÃO"

4. **Visualizar**: Use o seletor "Visualizar:" para trocar entre abordagens

5. **Observar**:
   - Mapa sendo preenchido com agentes de cores diferentes
   - Métricas atualizando em tempo real
   - Rodadas progredindo automaticamente
   - Grupos escalando de dificuldade

---

## 📊 ESTRUTURA DE DADOS

### Estado da Simulação
```python
# Rastreamento de Rodadas
self.rodada_atual: int = 1  # Rodada atual (1-9)
self.turno_atual: int = 0   # Turno dentro da rodada
self.num_agentes_atual: int = 2  # Agentes por grupo
self.percentagem_bombas_atual: float = 50.0  # % de bombas no mapa

# Resultados por Rodada
self.resultados_rodadas = {
    1: {  # Rodada
        0: {  # Abordagem (0=A, 1=B, 2=C)
            "R1_A0_G1": {  # Grupo ID
                "estrategia": "Exploração BFS",
                "num_agentes": 2,
                "tipos": ["AgenteBusca", "AgenteBusca"],
                "grupo_numero": 1  # Para cores
            }
        }
    }
}

# Cores para Grupos
self.cores_grupos = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A",
    "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2",
    "#F8B88B", "#A9DFBF"  # Até 10 cores diferentes
]
```

### Tabelas de Métricas (em tempo real)
```
Grupo [Cor]
├── Objetivo: [descrição]
├── Turno: N
├── Explorado: X%
├── Mortalidade: Y%
├── Eficiência: Z
└── Tabela de Agentes:
    ID | Tipo | Status | Passos | Tesouros | Efic.
```

---

## ✅ VALIDAÇÃO COMPLETA

Todos os testes passam com sucesso:

✅ Sistema de rodadas validado (2→10 agentes)
✅ Fórmula de bombas verificada (50%→80%)
✅ Grupos isolados funcionando
✅ Múltiplas abordagens simultâneas
✅ Agentes se movem e exploram
✅ Métricas em tempo real
✅ Interface responsiva
✅ Sistema de cores para grupos
✅ Limite de turnos por rodada (200)
✅ Transição automática entre rodadas

---

## 🔧 CARACTERÍSTICAS TÉCNICAS

### Isolamento de Grupos
- Cada grupo tem seu próprio gerenciador de memória
- Ambientes lógicos completamente isolados
- Mesmo mapa visual, lógica separada
- Sem interferência entre grupos

### Escalamento Automático
- Ao completar rodada, próxima começa automaticamente
- +1 agente por rodada
- +3.75% bombas por agente (progressão linear)
- 9 rodadas totais

### Sistema de Métricas
- Atualizado a cada turno
- Gestor de métricas por grupo e abordagem
- Cálculo de:
  - Cobertura do mapa
  - Taxa de mortalidade
  - Eficiência de exploração
  - Status individual de agentes

### Interface
- Painel de controles à esquerda
- Mapa central com visualização em tempo real
- Painel de métricas à direita com abas por grupo
- Cores diferenciadas para até 10 grupos

---

## 📝 NOTAS IMPORTANTES

1. **Turnos vs Rodadas**: 
   - Um "Turno" é um passo no tempo
   - Uma "Rodada" é uma série de turnos com mesmo nível de dificuldade
   
2. **Limite de Turnos**: 200 por rodada (para evitar loops infinitos)

3. **Status de Agentes**:
   - VIVO: agente ainda explorando
   - MORTO: acionou bomba
   - COMPLETADO: atingiu objetivo (bandeira)

4. **Grupos Simultâneos**: Todos progridem juntos no tempo

5. **Cores**: Cada grupo tem cor única para fácil identificação no mapa

---

## 🎓 PRÓXIMAS MELHORIAS (Opcional)

- [ ] Gráficos de progresso por rodada
- [ ] Estatísticas comparativas entre abordagens
- [ ] Export de resultados
- [ ] Replay de simulações
- [ ] Ajuste fino de parâmetros
- [ ] Diferentes algoritmos de geração de mapa

---

**Status**: ✅ SISTEMA 100% FUNCIONAL E VALIDADO

**Pronto para**: Uso imediato em ensino/pesquisa de agentes inteligentes

**Última Atualização**: Hoje (Janeiro 2026)
