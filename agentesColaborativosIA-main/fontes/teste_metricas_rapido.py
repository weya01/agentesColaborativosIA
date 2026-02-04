#!/usr/bin/env python3
"""Teste rápido de métricas de grupos"""
import sys
sys.path.insert(0, '.')

from ambientes import GeradorMapaValido
from agentes.memoria_partilhada import MemoriaPartilhada
from utils.constantes import ModoJogo
from ui.janela_principal import gerar_agentes_aleatorios
from config_grupos_exemplo import GRUPOS_MIX

# Testa métricas
gerador = GeradorMapaValido(10, ModoJogo.A_TESOUROS)
mapa, _ = gerador.gerar_com_relatorio()
memoria = MemoriaPartilhada()

agentes, gestor = gerar_agentes_aleatorios(mapa, memoria, grupos_config=GRUPOS_MIX)
print(f'✅ {len(agentes)} agentes criados em {len(gestor.grupos)} grupos')

# Executa 5 turnos
for turno in range(5):
    for agente in agentes:
        agente.executar_turno()

print(f'✅ 5 turnos executados')

# Exibe métricas
comparacao = gestor.obter_comparacao_grupos()
print(f'✅ Métricas de {len(comparacao)} grupos:')
for nome, dados in comparacao.items():
    m = dados['metricas']
    passos = m.get('passos_total', 0)
    celulas = m.get('celulas_exploradas_total', 0)
    print(f'  {nome}: {passos} passos, {celulas} células')
