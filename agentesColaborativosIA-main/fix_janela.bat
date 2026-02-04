@echo off
REM Clean janela_principal.py file

setlocal enabledelayedexpansion

set "filepath=c:\Users\HP\Downloads\agentesColaborativosIA-main\agentesColaborativosIA-main\fontes\ui\janela_principal.py"

(
echo """
echo Janela principal - Versão nova multi-grupo.
echo Redireciona para janela_principal_multi_grupo.
echo """
echo.
echo from .janela_principal_multi_grupo import JanelaPrincipalMultiGrupo as JanelaPrincipal
echo.
echo __all__ = ['JanelaPrincipal']
) > "!filepath!"

echo Arquivo limpo: !filepath!
