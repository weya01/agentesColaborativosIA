#!/usr/bin/env python
# -*- coding: utf-8 -*-

import py_compile
import sys

arquivos_testar = [
    'ui/janela_principal_multi_grupo.py'
]

erros = False
for arquivo in arquivos_testar:
    try:
        py_compile.compile(arquivo, doraise=True)
        print(f"✅ {arquivo} - OK")
    except py_compile.PyCompileError as e:
        print(f"❌ {arquivo} - ERRO: {e}")
        erros = True

if not erros:
    print("\n✅ Todos os arquivos compilaram com sucesso!")
    sys.exit(0)
else:
    print("\n❌ Há erros de sintaxe nos arquivos")
    sys.exit(1)
