# GUIA RÁPIDO - UTILIZAR O PROJETO

## ⚡ STATUS ATUAL: ✅ TUDO FUNCIONANDO!

**Todas as correções foram implementadas e testadas com sucesso.**
Veja `CORRECOES_FINAL.md` para detalhes técnicos.

## ⚡ Início Rápido

### Pré-requisitos
```bash
pip install PySide6
```

### Executar Aplicação
```bash
cd fontes
python main.py
```

> **Nota**: Nenhum erro esperado! Se encontrar algum, por favor reporte.

---

## 📖 Interface Gráfica

### Painel Esquerdo (Controles)

1. **Abordagem**
   - Selecione: A (Tesouros), B (Exploração) ou C (Bandeira)
   - Define o objetivo da simulação

2. **Tipo de Agente**
   - Desabilitado (ignorado)
   - Agentes são gerados ALEATORIAMENTE

3. **Número de Agentes**
   - Campo desabilitado (ignorado)
   - Sistema gera 2-10 agentes ALEATORIAMENTE

4. **Velocidade**
   - 100-2000 ms por turno
   - Padrão: 300 ms

5. **Botões**
   - ▶ Iniciar Simulação
   - ⏸ Pausar/Continuar
   - 🔄 Resetar
   - 💾 Exportar Métricas

### Painel Central (Mapa)

Visualização em tempo real:
- **Cinzento escuro** = Células exploradas
- **Vermelho** = Bombas conhecidas
- **Verde com número** = Agentes (ex: "1" = Agente A1)
- **Cinzento claro** = Células não exploradas

### Painel Direito (Métricas)

3 abas:
1. **Resumo**: Estatísticas globais da simulação
2. **Agentes**: Tabela com métricas de cada agente
3. **Detalhes**: Informações adicionais

---

## 🎮 Como Jogar

### Passo 1: Escolher Abordagem
```
Selecione uma das 3 abordagens:
- A: Encontrar >50% dos tesouros
- B: Explorar >80% do mapa
- C: Encontrar a bandeira
```

### Passo 2: Iniciar Simulação
```
Clique em "▶ Iniciar Simulação"

O sistema irá:
1. Gerar mapa válido
2. Criar 2-10 agentes aleatoriamente
3. Iniciar o relógio
```

### Passo 3: Acompanhar Progresso
```
Veja em tempo real:
- Agentes movem-se no mapa
- Células exploradas aparecem
- Métricas atualizam a cada turno
```

### Passo 4: Objetivo Alcançado
```
Quando o objetivo é atingido:
- Timer para
- Botão "Exportar Métricas" ativa
- Turno mostra "✓ OBJETIVO ALCANÇADO!"
```

---

## 🧪 Testar o Ciclo de IA

```bash
python teste_ia.py
```

Isto executa:
1. Geração de mapa
2. Validação de acessibilidade (flood fill)
3. Criação de agentes
4. Execução de 5 turnos
5. Coleta de métricas

Resultado esperado:
```
✅ TESTE CONCLUÍDO COM SUCESSO!
```

---

## 🔍 Entender o Ciclo de IA

Cada agente executa por turno:

```
1. PERCEÇÃO
   └─ Observa célula atual e vizinhos
   
2. ATUALIZAÇÃO DE MEMÓRIA
   └─ Registra: bombas, tesouros, células exploradas
   
3. DECISÃO
   └─ Escolhe próxima ação com base em algoritmo
   
4. AÇÃO
   └─ Move para célula ou coleta tesouro
```

**Código:**
```python
# Em agentes/base/agente_base.py
def executar_turno(self):
    percepcao = self._percepcao()              # 1. Perceber
    self._atualizar_memoria(percepcao)         # 2. Memorizar
    acao = self._decisao()                     # 3. Decidir
    if acao:
        self._executar_acao(acao)              # 4. Agir
```

---

## 📊 Interpretar Métricas

### Aba "Resumo"
- **Tesouros coletados**: Número de tesouros
- **Células exploradas**: Quantas células foram visitadas
- **Cobertura do mapa**: Percentagem explorada
- **Agentes vivos/mortos**: Estado dos agentes
- **Taxa mortalidade**: Percentagem de agentes mortos

### Aba "Agentes"
Tabela com:
- **ID**: Nome do agente (A1, A2, etc)
- **Tipo**: Algoritmo usado (BFS, Aleatório, KNN, etc)
- **Status**: VIVO ou MORTO
- **Passos**: Número de movimentos
- **Tesouros**: Coletados por este agente
- **Eficiência**: Passos/célula explorada

### Aba "Detalhes"
Informações adicionais sobre a execução.

---

## 🐛 Troubleshooting

### Problema: "Módulo não encontrado"
```
ModuleNotFoundError: No module named 'PySide6'
```
**Solução:**
```bash
pip install PySide6
```

### Problema: Mapa não aparece
```
O container mostra "Mapa será exibido aqui"
```
**Solução:**
Clique em "▶ Iniciar Simulação" para gerar mapa

### Problema: Agentes não se movem
```
Agentes ficam na mesma posição
```
**Verificar:**
- Velocidade não é muito alta
- Tempo suficiente passou
- Agentes não morreram todos

### Problema: Objetivo alcançado imediatamente
```
Objetivo aparece no turno 1
```
**Possível causa:**
- Mapa muito pequeno/com muitos tesouros
- Abordagem B/C com configuração especial
- Tente resetar e tentar novamente

---

## 📁 Estrutura de Ficheiros

```
fontes/
├── main.py ........................ Ponto de entrada
├── agentes/
│   ├── base/agente_base.py ........ Classe base (ciclo IA)
│   ├── agentes_busca/ ............. Agentes com busca
│   ├── agentes_nao_busca/ ......... Agentes sem busca
│   └── agentes_hibridos/ .......... Agentes híbridos
├── ambientes/
│   ├── gerador_de_mapa.py ......... Gera mapas
│   ├── validador_acessibilidade.py  Flood fill
│   └── manutencao_mapa.py ......... Valida mapas
├── simulacao/
│   └── motor.py ................... Controla simulação
├── metricas/
│   ├── metricas.py ................ Métricas de agente
│   └── gestor_metricas.py ......... Gestor de métricas
├── ui/
│   ├── janela_principal.py ........ UI principal
│   ├── grid_mapa.py ............... Renderizador de mapa
│   └── cores.py ................... Definição de cores
└── utils/
    └── constantes.py .............. Enums e constantes
```

---

## 💡 Dicas Avançadas

### Testar Abordagem Específica
```python
# Em teste_ia.py, mude:
modo=ModoJogo.A_TESOUROS  # A
modo=ModoJogo.B_SOBREVIVENCIA  # B
modo=ModoJogo.C_BANDEIRA  # C
```

### Ajustar Probabilidades de Mapa
```python
# Em ambientes/gerador_de_mapa.py
def _mapa_tesouros(self):
    return self._gerar_mapa(
        prob_bomba=0.25,      # Reduz para menos bombas
        prob_tesouro=0.35,    # Aumenta para mais tesouros
        com_bandeira=False
    )
```

### Aumentar Max Turnos
```python
# Em ui/janela_principal.py iniciar_simulacao()
self.motor = MotorSimulacao(
    ...
    max_turnos=1000,  # Aumenta de 500 para 1000
    ...
)
```

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se PySide6 está instalado
2. Verifique PATH de Python
3. Tente executar `teste_ia.py` primeiro
4. Verifique console para mensagens de erro

---

## ✅ Checklist Antes da Defesa

- [ ] Aplicação inicia sem erros
- [ ] Selector de Abordagem funciona
- [ ] Mapa renderiza corretamente
- [ ] Agentes se movem
- [ ] Métricas atualizam
- [ ] Objetivo é detectado corretamente
- [ ] Pode pausar/retomar simulação
- [ ] Pode resetar e começar nova

**Se tudo acima passa, PRONTO PARA DEFESA!** ✅

