#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para diagnosticar o problema de inicialização
"""
import sys
sys.path.insert(0, '.')

print("=" * 70)
print("TESTE DE INICIALIZAÇÃO - Simulação Multi-Agentes")
print("=" * 70)

try:
    print("\n1️⃣  Importando abordagens...")
    from simulacao.abordagens import AbordagensPadrao, TipoAbordagem
    abordagem_a = AbordagensPadrao.obter_abordagem_a()
    print(f"   ✅ Abordagem A criada: {abordagem_a.tipo.value} - {abordagem_a.modo_jogo}")
except Exception as e:
    print(f"   ❌ Erro em abordagens: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n2️⃣  Importando gerador de agentes...")
    from agentes.gerador_por_abordagem import GeradorAgentesAbordagem
    factory = GeradorAgentesAbordagem.obter_factory_por_abordagem('A')
    print(f"   ✅ Factory obtida: {factory}")
except Exception as e:
    print(f"   ❌ Erro em gerador: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n3️⃣  Criando gerenciador de grupos...")
    from simulacao.gerenciador_corridas import GerenciadorGrupos
    gerenciador = GerenciadorGrupos()
    print(f"   ✅ Gerenciador criado")
except Exception as e:
    print(f"   ❌ Erro em gerenciador: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("\n4️⃣  Criando grupo 0 (Abordagem A)...")
    gerenciador.criar_grupo(
        grupo_id=0,
        abordagem='A',
        modo=abordagem_a.modo_jogo,
        agentes_factory=factory,
        num_agentes=3  # Teste com 3 agentes
    )
    print(f"   ✅ Grupo criado")
except Exception as e:
    print(f"   ❌ Erro ao criar grupo: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ TESTE CONCLUÍDO COM SUCESSO")
print("=" * 70)
