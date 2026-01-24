AgentesColaborativos_Grupo_X/
│
├── README.md
├── requerimentos.txt
├── .gitignore
│
├── docs/
│   ├── relatorio.pdf
│   ├── apresentacao.pdf
│   └── referencias.md
│
├── data/
│   ├── mapas/
│   │   ├── mapa_base.json
│   │   └── mapa_teste/
│   └── logs/
│       └── execucao.log
│
├── src/
│   ├── main.py
│
│   ├── ambientes/
│   │   ├── __init__.py
│   │   ├── gerador_mapa.py
│   │   ├── validador.py
│   │   └── celula.py
│
│   ├── agentes/
│   │   ├── __init__.py
│   │   ├── agente_base.py
│   │   ├── agente_busca.py
│   │   ├── agente_ml.py
│   │   ├── agente_hibrido.py
│   │   └── memoria_partilhada.py
│
│   ├── simulacao/
│   │   ├── __init__.py
│   │   ├── motor.py
│   │   ├── modos_jogo.py
│   │   └── metricas.py
│
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── painel.py
│   │   └── renderizador.py
│
│   └── utils/
│       ├── ajudas.py
│       └── constantes.py
│
└── testes/
    ├── teste_mapa.py
    ├── teste_agente.py
    └── teste_simulacao.py
