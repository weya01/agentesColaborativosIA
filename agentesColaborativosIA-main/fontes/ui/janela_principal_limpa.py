"""
Janela principal da aplicação - versão multi-grupo.

Compatibilidade com versão anterior.
"""

# Redireciona para versão nova
from .janela_principal_multi_grupo import JanelaPrincipalMultiGrupo

# Alias para compatibilidade
JanelaPrincipal = JanelaPrincipalMultiGrupo

__all__ = ['JanelaPrincipal', 'JanelaPrincipalMultiGrupo']
