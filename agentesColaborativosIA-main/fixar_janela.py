#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix janela_principal.py by keeping only first 8 lines"""

arquivo = r"C:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes\ui\janela_principal.py"

linhas_corretas = [
    '"""',
    'Janela principal - Versão nova multi-grupo.',
    'Redireciona para janela_principal_multi_grupo.',
    '"""',
    '',
    'from .janela_principal_multi_grupo import JanelaPrincipalMultiGrupo as JanelaPrincipal',
    '',
    "__all__ = ['JanelaPrincipal']",
]

try:
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas_corretas))
    print("✅ Arquivo janela_principal.py limpo com sucesso!")
    print(f"   Tamanho: {len(linhas_corretas)} linhas")
except Exception as e:
    print(f"❌ Erro: {e}")
