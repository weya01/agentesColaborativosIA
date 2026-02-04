#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de validação - Verifica se o código foi corrigido corretamente
"""

import sys
import os

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa e analisa o arquivo
try:
    print("=" * 70)
    print("TESTE DE VALIDAÇÃO - Janela Principal Multi Grupo")
    print("=" * 70)
    
    # Teste 1: Compilação
    print("\n[1/3] Testando compilação...")
    import py_compile
    py_compile.compile('ui/janela_principal_multi_grupo.py', doraise=True)
    print("✅ Arquivo compila sem erros de sintaxe")
    
    # Teste 2: Imports
    print("\n[2/3] Testando imports...")
    from ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
    print("✅ Classe JanelaPrincipalMultiGrupo importada com sucesso")
    
    # Teste 3: Análise de código
    print("\n[3/3] Analisando código...")
    
    import inspect
    
    # Verifica se o método _atualizar_tabs_grupos existe
    if hasattr(JanelaPrincipalMultiGrupo, '_atualizar_tabs_grupos'):
        print("✅ Método _atualizar_tabs_grupos existe")
    else:
        print("❌ Método _atualizar_tabs_grupos não encontrado")
        sys.exit(1)
    
    # Verifica o código do método
    source = inspect.getsource(JanelaPrincipalMultiGrupo._atualizar_tabs_grupos)
    
    # Verifica se há referências a variáveis não definidas
    if 'widget.texto_resumo' in source:
        print("❌ Ainda há referências a widget.texto_resumo no método")
        sys.exit(1)
    else:
        print("✅ Sem referências a widget.texto_resumo")
    
    if 'widget.tabela_agentes' in source:
        print("❌ Ainda há referências a widget.tabela_agentes no método")
        sys.exit(1)
    else:
        print("✅ Sem referências a widget.tabela_agentes")
    
    if 'return widget' in source:
        print("❌ Ainda há 'return widget' obsoleto no método")
        sys.exit(1)
    else:
        print("✅ Sem 'return widget' obsoleto")
    
    print("\n" + "=" * 70)
    print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
