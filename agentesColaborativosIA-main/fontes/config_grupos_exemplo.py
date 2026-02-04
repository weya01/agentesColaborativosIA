"""
Configurações de exemplo para grupos de agentes.
Demonstra como criar grupos homogêneos e híbridos.
"""

# Exemplo 1: Grupos homogêneos (mesmo tipo de algoritmo)
GRUPOS_HOMOGENEOS = [
    {
        'tipo': 'homogeneo',
        'agente': 'BFS',
        'tamanho': 3,
        'nome': 'Grupo BFS'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'Aleatório',
        'tamanho': 3,
        'nome': 'Grupo Aleatório'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'Exploração',
        'tamanho': 2,
        'nome': 'Grupo Exploração'
    },
]

# Exemplo 2: Grupos híbridos (mesclagem de 2 tipos)
GRUPOS_HIBRIDOS = [
    {
        'tipo': 'hibrido',
        'agentes': ['BFS', 'KNN'],
        'tamanho': 4,
        'nome': 'Grupo BFS+KNN'
    },
    {
        'tipo': 'hibrido',
        'agentes': ['Exploração', 'Aleatório'],
        'tamanho': 3,
        'nome': 'Grupo Exploração+Aleatório'
    },
]

# Exemplo 3: Mix (alguns homogêneos, alguns híbridos)
GRUPOS_MIX = [
    {
        'tipo': 'homogeneo',
        'agente': 'BFS',
        'tamanho': 3,
        'nome': 'Grupo BFS Puro'
    },
    {
        'tipo': 'hibrido',
        'agentes': ['BFS', 'Aleatório'],
        'tamanho': 3,
        'nome': 'Grupo BFS+Aleatório'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'Exploração',
        'tamanho': 2,
        'nome': 'Grupo Exploração Puro'
    },
]

# Exemplo 4: Comparação completa (todos os tipos)
GRUPOS_COMPLETOS = [
    {
        'tipo': 'homogeneo',
        'agente': 'BFS',
        'tamanho': 2,
        'nome': 'BFS'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'DFS',
        'tamanho': 2,
        'nome': 'Árvore de Busca'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'Aleatório',
        'tamanho': 2,
        'nome': 'Aleatório'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'Exploração',
        'tamanho': 2,
        'nome': 'Exploração'
    },
    {
        'tipo': 'homogeneo',
        'agente': 'KNN',
        'tamanho': 2,
        'nome': 'KNN'
    },
    {
        'tipo': 'hibrido',
        'agentes': ['BFS', 'KNN'],
        'tamanho': 2,
        'nome': 'Híbrido BFS+KNN'
    },
    {
        'tipo': 'hibrido',
        'agentes': ['Exploração', 'Aleatório'],
        'tamanho': 2,
        'nome': 'Híbrido Exploração+Aleatório'
    },
]
