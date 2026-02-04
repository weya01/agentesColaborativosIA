# 🤖 Sistema de Simulação Multi-Agentes - Rodadas Progressivas

## ✨ Visão Geral

Sistema de simulação de agentes inteligentes com **9 rodadas progressivas** onde:
- Começam com **2 agentes** por grupo
- Terminam com **10 agentes** por grupo
- Dificuldade aumenta com mais bombas no mapa (50% → 80%)
- **3 abordagens** executando **simultaneamente**
- Grupos **isolados** mas competindo na mesma arena

---

## 🚀 Início Rápido

### 1️⃣ Instalar dependências
```bash
pip install PySide6
```

### 2️⃣ Executar a aplicação
```bash
cd fontes
python main.py
```

### 3️⃣ Na interface:
1. Selecione as abordagens (A, B, C ou combinações)
2. Escolha a velocidade (0ms a 1000ms por turno)
3. Clique "▶ INICIAR SIMULAÇÃO"
4. Observe os agentes explorando o mapa!

---

## 📊 O Que Acontece

### Progressão de Rodadas
```
Rodada  Agentes  Bombas   Status
──────────────────────────────────
  1        2      50.00%   Explorando...
  2        3      53.75%   Escalando ⬆️
  3        4      57.50%   
  4        5      61.25%   
  5        6      65.00%   
  6        7      68.75%   
  7        8      72.50%   
  8        9      76.25%   
  9       10      80.00%   Completado ✅
```

### 3 Abordagens
- 🟢 **A (Tesouros)**: Coletar tesouros + atingir bandeira
- 🔵 **B (Sobrevivência)**: Explorar 80% do mapa
- 🟠 **C (Bandeira)**: Apenas atingir a bandeira

### Simultaneidade
Todos os grupos progridem juntos nos mesmos turnos:
- Cada grupo tem seu próprio ambiente lógico
- Visualização compartilhada no mapa (cores diferentes)
- Métricas independentes

---

## 📋 Interface

### Painel Esquerdo - Controles
- ✅ Seleção de abordagens (A, B, C)
- ⚡ Controle de velocidade
- ▶️ Botões: Iniciar, Pausar, Resetar
- 📖 Informações e legenda

### Painel Central - Simulação
- 🗺️ Mapa em tempo real com agentes
- 📍 Status de rodada (Rodada X/9)
- ⏱️ Contador de turnos
- 🎨 Cores diferentes para cada grupo

### Painel Direito - Métricas
- 📊 Seletor para visualizar abordagem
- 📈 Abas com dados de cada grupo:
  - Objetivo
  - % Explorado
  - Mortalidade
  - Eficiência
  - Tabela de agentes (ID, Tipo, Status, Passos, Tesouros)

---

## 🔬 Testes Disponíveis

### Teste Rápido (< 2 seg)
```bash
python validacao_rapida.py
```

### Teste de Rodadas
```bash
python teste_rodadas.py
```

### Teste de Comportamento dos Agentes
```bash
python teste_comportamento_agentes.py
```

### Teste Completo da Interface
```bash
python rodar_interface.py
```

---

## 📁 Estrutura de Arquivos

```
fontes/
├── main.py                           # Ponto de entrada
├── ui/
│   ├── janela_principal_clean.py     # Interface principal
│   ├── janela_principal_rodadas.py   # Sistema de rodadas (NOVO)
│   └── grid_mapa.py                  # Visualização do mapa
├── simulacao/
│   ├── gerenciador_corridas.py       # Gerencia grupos
│   ├── abordagens.py                 # Definições das 3 abordagens
│   └── motor.py                      # Motor de simulação
├── agentes/
│   ├── base/
│   │   └── agente_base.py            # Classe base de agentes
│   ├── agentes_busca/
│   │   └── agente_busca.py           # Implementação de busca
│   ├── gerador_por_abordagem.py      # Factory de agentes
│   └── memoria_partilhada.py         # Memória do grupo
├── ambientes/
│   ├── gerador_de_mapa.py            # Geração de mapas
│   └── ambiente.py                   # Lógica do ambiente
├── metricas.py                       # Cálculo de métricas
├── teste_rodadas.py                  # Testes (NOVO)
├── teste_comportamento_agentes.py    # Testes (NOVO)
├── teste_interface_rodadas.py        # Testes (NOVO)
├── validacao_rapida.py               # Validação rápida (NOVO)
├── rodar_interface.py                # Executar interface (NOVO)
└── SISTEMA_REFINADO.md              # Documentação (NOVO)
```

---

## 🎯 Funcionalidades Principais

✅ **Sistema de Rodadas**: 9 rodadas com escalamento automático
✅ **Grupos Isolados**: Cada grupo tem ambiente lógico próprio
✅ **Execução Simultânea**: Todos progridem juntos no tempo
✅ **Cores Dinâmicas**: Até 10 grupos com cores diferentes
✅ **Métricas em Tempo Real**: Atualização de dados a cada turno
✅ **3 Abordagens**: Diferentes objetivos para análise comparativa
✅ **Interface Intuitiva**: Seletor único, sem botões redundantes
✅ **Limite de Turnos**: 200 turnos máximo por rodada

---

## 🔧 Configuração

### Modificar limite de turnos
Arquivo: `ui/janela_principal_rodadas.py`
```python
MAX_TURNOS_POR_RODADA = 200  # Mude para mais/menos
```

### Modificar número de rodadas
Arquivo: `ui/janela_principal_rodadas.py`
```python
if self.rodada_atual < 9:  # Mude o número
```

### Modificar cores dos grupos
Arquivo: `ui/janela_principal_rodadas.py`
```python
self.cores_grupos = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", ...  # Adicione/modifique cores
]
```

---

## 💡 Dicas de Uso

1. **Começar com velocidade Normal**: Permite ver agentes se movimentando
2. **Visualizar uma abordagem por vez**: Mais fácil de acompanhar
3. **Pausar e retomar**: Use ⏸ para analisar um turno específico
4. **Resetar para novas simulações**: Limpa tudo e começa do zero

---

## 📊 Interpretando as Métricas

- **% Explorado**: Percentual de células visitadas
- **Mortalidade**: Percentual de agentes que morreram
- **Eficiência**: Benefício obtido / custo em passos
- **Passos**: Quantidade de movimentos do agente
- **Tesouros**: Itens coletados (abordagem A)
- **Status**: VIVO = ativo, MORTO = acionou bomba

---

## 🐛 Troubleshooting

### "Module not found" erro
```bash
pip install PySide6
```

### Interface não abre
```bash
python validacao_rapida.py
```

### Agentes não se movem
Aumente a duração (reduz velocidade em ms)

---

## 📚 Documentação Adicional

- `SISTEMA_REFINADO.md`: Documentação técnica completa
- Código comentado em português

---

## ✅ Status do Sistema

🟢 **FUNCIONAL E VALIDADO**
- Todas as 5 validações rápidas passam
- Testes de comportamento bem-sucedidos
- Sistema pronto para produção

---

## 📝 Versão

**v2.0 - Sistema de Rodadas Progressivas**
- Data: Janeiro 2026
- Status: ✅ Completo

---

**Aproveite a simulação! 🚀**
