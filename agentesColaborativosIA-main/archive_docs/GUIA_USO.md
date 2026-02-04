# 🤖 Guia de Uso - Sistema Multi-Agentes Colaborativo

## 📋 Visão Geral

Sistema de simulação de agentes inteligentes com **3 abordagens isoladas** para diferentes objetivos.

---

## 🎯 As 3 Abordagens

### 🟢 **Abordagem A: Coleta de Tesouros**
- **Objetivo**: Coletar **≥50% dos tesouros descobertos**
- **Tipo de Agentes**: 
  - BFS (Busca em Largura)
  - KNN (K-Nearest Neighbors)
- **Mapa**: 
  - Bombas: 25%
  - Tesouros: 35%
  - Livres: 40%
- **Vitória**: Coleta tesouros e sobrevive

### 🔵 **Abordagem B: Sobrevivência Máxima**
- **Objetivo**: Explorar **>80% do mapa E manter ≥1 agente vivo**
- **Tipo de Agentes**: 
  - Aleatório Seguro (evita bombas conhecidas)
- **Mapa**: 
  - Bombas: 2%
  - Tesouros: 10%
  - Livres: 88%
- **Vitória**: Máxima exploração com sobrevivência
- **Agentes**: 5 agentes

### 🟠 **Abordagem C: Encontrar Bandeira**
- **Objetivo**: Encontrar e alcançar a **bandeira**
- **Tipo de Agentes**: 
  - 60% Aleatório Seguro
  - 30% KNN
  - 10% Híbrido
- **Mapa**: 
  - Bombas: 10%
  - Tesouros: 0%
  - Bandeira: 1
  - Livres: 89%
- **Vitória**: Descobrir e alcançar bandeira

---

## 🖱️ Como Usar a Interface

### 1️⃣ **Selecione UMA Abordagem**
```
Clique em um dos botões de abordagem:
✓ Apenas UM pode estar selecionado por vez
✓ Mudar de abordagem LIMPA O MAPA automaticamente
✓ Nenhum elemento de simulações anteriores permanece
```

### 2️⃣ **Ajuste Velocidade** (Opcional)
```
Muito Rápido  → 0ms por turno (visualização rápida)
Rápido        → 100ms por turno
Normal        → 200ms por turno (RECOMENDADO)
Lento         → 500ms por turno
Muito Lento   → 1000ms por turno (análise detalhada)
```

### 3️⃣ **Clique em "Iniciar Simulação"**
```
A simulação vai:
✓ Gerar um NOVO mapa aleatório
✓ Criar os agentes apropriados para a abordagem
✓ Executar os turnos automaticamente
✓ Mostrar progresso em tempo real
```

### 4️⃣ **Monitore as Métricas**
```
Para cada turno você verá:
- Células exploradas
- Agentes vivos/mortos
- Tesouros coletados (Abordagem A)
- Percentual exploração (Abordagem B)
- Bandeira encontrada (Abordagem C)
```

### 5️⃣ **Controles Durante Simulação**
```
⏸ Pausar      → Pausa a simulação
🔄 Resetar    → Limpa e volta ao início
📊 Comparar   → Mostra resultados finais
```

---

## 📊 Entendendo os Resultados

### ✅ Sucesso (Objetivo Alcançado)
```
Abordagem A: Coleta ≥50% dos tesouros descobertos
Abordagem B: >80% exploração + ≥1 agente vivo
Abordagem C: Bandeira encontrada
```

### ❌ Falha (Objetivo Não Alcançado)
```
Agentes podem morrer em bombas
Exploração pode ser incompleta
Tesouros podem não ser encontrados
```

---

## 🔄 Comportamento dos Agentes

### 📍 **Memória Partilhada do Grupo**
- Todos os agentes do mesmo grupo compartilham:
  - Células exploradas
  - Bombas conhecidas
  - Tesouros descobertos
  
✓ **Agentes NÃO revisitam células já exploradas** (se houver alternativas)

### 🧠 **Estratégia de Movimento**
```
1. Prioridade: Células NUNCA exploradas e sabidamente SEGURAS
2. Prioridade: Células NUNCA exploradas
3. Prioridade: Células seguras já vistas
4. Último recurso: Qualquer célula válida
```

### ⚠️ **Segurança**
```
- Agentes NUNCA entram em bombas conhecidas
- Exploram células desconhecidas calculando risco
- Compartilham descoberta de bombas em tempo real
```

---

## 💡 Dicas de Uso

### ✨ Para melhor compreensão:
1. **Comece com Abordagem B** (Sobrevivência)
   - Mais fácil de entender
   - Muitos agentes (5)
   - Objetivo claro (exploração)

2. **Use velocidade "Normal"** (200ms)
   - Tempo suficiente para ver movimento
   - Não é muito lento

3. **Observe o padrão de movimento**
   - Veja como agentes evitam células visitadas
   - Entenda estratégia de exploração

### 🔬 Para análise profunda:
1. **Use "Muito Lento"** (1000ms)
2. **Execute várias vezes** a mesma abordagem
   - Mapas diferentes cada vez
   - Compare resultados

---

## 🐛 Troubleshooting

### "Erro: DEVE SER FEITA APENAS UMA ABORDAGEM POR VEZ"
```
❌ Você selecionou mais de uma abordagem
✓ Clique em APENAS UM botão de abordagem
✓ Os outros vão ficar desativados automaticamente
```

### "Mapa não limpou"
```
✓ Mapa é limpado automaticamente ao trocar abordagem
✓ Clique em "Resetar" para limpar manualmente
✓ Inicie nova simulação para novo mapa aleatório
```

### "Agentes não se movem"
```
✓ Pode estar em pausa - clique "Pausar" novamente
✓ Simulação terminou - verifique métrica de "Objetivo alcançado"
✓ Aumente velocidade se está muito lento
```

---

## 📈 Exemplo de Execução

### Abordagem B (Sobrevivência):
```
Turno 1:   1/100 exploradas (1%) | 5/5 vivos
Turno 10:  23/100 exploradas (23%) | 4/5 vivos
Turno 20:  40/100 exploradas (40%) | 3/5 vivos
...
Turno 50:  81/100 exploradas (81%) | 2/5 vivos ✓ OBJETIVO ALCANÇADO

📊 Resultado:
   - Exploração: 81% (>80% ✓)
   - Agentes vivos: 2 (≥1 ✓)
   - Sucesso: SIM
```

---

## 🎓 Aprenda Mais

- **Algoritmos de Agentes**: Ver código em `fontes/agentes/`
- **Memória Partilhada**: Ver `fontes/agentes/memoria_partilhada.py`
- **Gerador de Mapas**: Ver `fontes/ambientes/gerador_de_mapa.py`
- **Motor de Simulação**: Ver `fontes/simulacao/motor.py`

---

## 📞 Suporte

Sistema desenvolvido para análise de algoritmos de inteligência artificial em ambientes colaborativos.

**Versão**: 1.0  
**Data**: Janeiro 2026  
**Linguagem**: Python 3.11+  
**GUI**: PySide6
