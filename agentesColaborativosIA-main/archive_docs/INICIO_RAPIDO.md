# 🚀 GUIA DE INÍCIO RÁPIDO - Sistema Pronto para Uso

## ⚡ Começar em 30 Segundos

### 1️⃣ Abrir Terminal
```
Windows: Pressione Win+R, digite "cmd" e Enter
```

### 2️⃣ Navegar para Pasta
```bash
cd "c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes"
```

### 3️⃣ Iniciar Aplicação
```bash
python main.py
```

### 4️⃣ Interface Gráfica Aparecerá
- ✅ QListWidget mostrando: Abordagem A, Abordagem B, Abordagem C
- ✅ Painel de controles à esquerda
- ✅ Visualização do grid à direita

---

## 🎮 Como Usar

### Selecionar Abordagens
```
1. Clique em "Abordagem A"
2. Segure Ctrl + Clique em "Abordagem B" 
3. (Opcional) Segure Ctrl + Clique em "Abordagem C"
```

### Ajustar Velocidade
```
- Selector "Velocidade" à esquerda
- 0ms = rápido, 1000ms = lento
```

### Iniciar Simulação
```
- Clique em "Iniciar Simulação"
- Observe o scaling progressivo
- Agentes aumentam: 2 → 3 → 4 → ... → 10
- Bombas aumentam: 50% → 53.75% → 57.5% → ... → 80%
```

### Pausar/Parar
```
- Clique em "Pausar" para pausar
- Clique em "Resetar" para resetar
```

---

## ✅ Checklist de Validação

Antes de iniciar, verifique:
- [x] Python 3.8+ instalado (`python --version`)
- [x] PyQt6 instalado (`pip install PyQt6`)
- [x] Arquivo `main.py` em `fontes/`
- [x] Pasta `ui/` existe com `janela_principal_multi_grupo.py`
- [x] Pasta `simulacao/` existe com módulos

---

## 🔍 Verificação Rápida

### Validar Sintaxe (Antes de Iniciar)
```bash
python -c "from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo; print('✅ OK')"
```

### Esperado: `✅ OK`

---

## 📊 O Que Esperar

### Primeiro Turno
- 2 agentes em cada grupo
- 50% de bombas
- Grupos: Abordagem A (3 grupos), Abordagem B (3 grupos), Abordagem C (3 grupos)

### Durante Simulação
- Agentes se movem no grid
- Evitam bombas
- Procuram objetivo (bandeira ou tesouro)

### Quando Grupo Termina Objetivo
- ✅ Ativo no log
- 🚀 Próxima geração inicia
- 📈 +1 agente
- 💣 +3.75% bombas

### Ciclo Completo
- Começa: 2 agentes, 50% bombas
- Termina: 10 agentes, 80% bombas
- Duração: Varia com velocidade

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Erro: "No module named 'simulacao'"
```
Certifique-se de estar em: c:\...\fontes\
python main.py
```

### GUI não abre
```
- Verifique se Python está corretamente instalado
- Tente: python --version
- Deve ser 3.8 ou superior
```

### QListWidget não mostra items
```
- Reinicie a aplicação
- Se persistir, execute: python validacao_atualizacao.py
```

---

## 📚 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| `CONCLUSAO_FINAL.md` | Status final do projeto |
| `CORRECOES_FINAIS.md` | Detalhes técnicos das correções |
| `RESUMO_SESSAO_COMPLETO.md` | Histórico completo de mudanças |
| `GUIA_USO_FINAL.md` | Guia de uso detalhado |
| `README.md` | Visão geral do projeto |

---

## 💬 Suporte Rápido

### Perguntas Comuns

**P: Como selecionar múltiplas abordagens?**  
R: Use Ctrl+Click na QListWidget

**P: Qual é o máximo de agentes?**  
R: 10 agentes (atinge ao 8º turno)

**P: Abordagem C tem tesouros?**  
R: Não, apenas objetivo de bandeira

**P: Posso pausar a simulação?**  
R: Sim, clique em "Pausar" durante execução

**P: Como reseto tudo?**  
R: Clique em "Resetar" para voltar ao início

---

## 🎓 Exemplos de Uso

### Exemplo 1: Comparar Abordagens
```
1. Selecione APENAS Abordagem A
2. Clique "Iniciar Simulação"
3. Observe resultados de A
4. Clique "Resetar"
5. Repita para B e C
```

### Exemplo 2: Análise Comparativa
```
1. Selecione A, B e C (Ctrl+Click)
2. Clique "Iniciar Simulação"
3. Compare abas de Abordagem 0 (Comparação)
4. Veja métricas de todas
```

### Exemplo 3: Teste de Velocidade
```
1. Selector Velocidade = 0ms (máximo)
2. Selecione uma abordagem
3. Observe scaling em alta velocidade
```

---

## 🎯 Próximos Passos

1. **Executar**: `python main.py`
2. **Explorar**: Teste diferentes combinações de abordagens
3. **Analisar**: Verifique abas de métricas e comparação
4. **Documentar**: Registre seus achados

---

## 📞 Contato / Suporte

Se encontrar problemas:
1. Verifique se Python 3.8+ está instalado
2. Certifique-se de estar no diretório `fontes/`
3. Execute `python validacao_atualizacao.py` para validar código
4. Consulte documentação em `*.md` arquivos

---

**Status**: 🟢 Sistema Pronto para Uso
**Última Atualização**: Sessão Atual
**Tempo até Uso**: ~30 segundos

Boa sorte! 🚀
