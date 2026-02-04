AgentesColaborativos_Grupo_X/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/                     # Documentação
│   ├── relatorio.pdf
│   ├── apresentacao.pdf
│   └── referencias.md
│
├── data/                     # Dados e mapas
│   ├── maps/
│   │   ├── base_map.json
│   │   └── test_maps/
│   └── logs/
│       └── exec_log.txt
│
├── src/
│   ├── main.py               # Ponto de entrada
│   │
│   ├── environment/          # PARTE 1
│   │   ├── __init__.py
│   │   ├── map_generator.py
│   │   ├── validator.py
│   │   └── cell.py
│   │
│   ├── agents/               # PARTE 2
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── random_agent.py
│   │   ├── knn_agent.py
│   │   ├── tree_agent.py
│   │   └── shared_memory.py
│   │
│   ├── simulation/           # PARTE 3
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── approaches.py     # A, B, C
│   │   └── metrics.py
│   │
│   ├── ui/                    # Interface
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   └── renderer.py
│   │
│   └── utils/
│       ├── helpers.py
│       └── constants.py
│
└── tests/
    ├── test_map.py
    ├── test_agents.py
    └── test_simulation.py
