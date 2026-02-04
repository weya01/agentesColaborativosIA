"""
Diagnóstico do gerador de mapa - verificar se está a colocar bombas em (0,0)
"""
from fontes.ambientes.gerador_de_mapa import GeradorDeMapa

# Testa a geração de 20 mapas
gen = GeradorDeMapa()

print("=" * 60)
print("DIAGNÓSTICO DO GERADOR DE MAPA")
print("=" * 60)

bombas_em_zero_zero = 0
mapas_testados = 20

for i in range(mapas_testados):
    mapa = gen.gerar_mapa_exploracao(prob_bomba=0.05)
    
    # Verifica se (0,0) é bomba
    celula_inicial = mapa[0][0]
    print(f"\nMapa {i+1}: (0,0) = '{celula_inicial}'", end="")
    
    if celula_inicial == "B":
        print(" ❌ BOMBA!")
        bombas_em_zero_zero += 1
    else:
        print(" ✓ Seguro")
    
    # Também calcula estatísticas
    bombs = sum(row.count("B") for row in mapa)
    treasures = sum(row.count("T") for row in mapa)
    empty = sum(row.count(" ") for row in mapa)
    total = bombs + treasures + empty
    
    print(f"   Conteúdo: {bombs} bombas, {treasures} tesouros, {empty} vazios (total {total})")

print("\n" + "=" * 60)
print(f"RESULTADO: {bombas_em_zero_zero}/{mapas_testados} mapas têm bomba em (0,0)")
print(f"Taxa: {bombas_em_zero_zero/mapas_testados*100:.1f}%")
print("=" * 60)
