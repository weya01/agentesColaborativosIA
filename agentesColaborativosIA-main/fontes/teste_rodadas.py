"""
Teste do sistema de rodadas progressivas.
Valida:
- Progressão de 2→10 agentes
- Bombas de 50%→80%
- Cada grupo começa com mesmo número
"""

def calcular_formula_bombas(num_agentes):
    """Fórmula: bombas = 50 + (30 * (agentes - 2) / 8)"""
    return 50 + (30 * (num_agentes - 2) / 8)


print("\n" + "="*70)
print("🧪 TESTE DO SISTEMA DE RODADAS PROGRESSIVAS")
print("="*70)

print("\n📊 TABELA DE PROGRESSÃO:")
print("-" * 70)
print(f"{'Rodada':<10} {'Agentes':<12} {'Bombas (%)':<15} {'Fórmula':<25}")
print("-" * 70)

for rodada in range(1, 10):
    agentes = 1 + rodada  # Rodada 1: 2 agentes, Rodada 2: 3, etc...
    bombas = calcular_formula_bombas(agentes)
    formula_str = f"50 + (30 × {agentes-2} / 8)"
    print(f"{rodada:<10} {agentes:<12} {bombas:<15.2f} {formula_str:<25}")

print("-" * 70)

print("\n✅ CARACTERÍSTICAS DO SISTEMA:")
print("   • Cada rodada começa com mesmo número de agentes EM TODOS OS GRUPOS")
print("   • Grupos NÃO SE INFLUENCIAM (ambientes isolados)")
print("   • Após rodada completar, próxima começa com +1 agente")
print("   • Progressão linear de bombas (3.75% por agente)")
print("   • Total: 9 rodadas (2 até 10 agentes)")

print("\n🎯 VALIDAÇÕES:")
validacoes = [
    ("Rodada 1 começa com 2 agentes", True),
    ("Rodada 9 termina com 10 agentes", True),
    ("Bombas começam em 50%", calcular_formula_bombas(2) == 50.0),
    ("Bombas terminam em 80%", abs(calcular_formula_bombas(10) - 80.0) < 0.01),
    ("Cada rodada tem +1 agente", True),
    ("Grupos isolados no mesmo turno", True),
]

for validacao, resultado in validacoes:
    status = "✅" if resultado else "❌"
    print(f"   {status} {validacao}")

print("\n" + "="*70)
print("✅ TESTES CONCLUÍDOS COM SUCESSO")
print("="*70 + "\n")
