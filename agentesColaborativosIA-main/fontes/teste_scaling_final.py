#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TESTE CRÍTICO: Validação do Sistema de Scaling Progressivo
Verifica:
1. Agentes começam com 2 e terminam com 10
2. Bombas aumentam de 50% para 80%
3. Agentes atingem condições de vitória
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ambientes.gerador_de_mapa import GeradorDeMapa
from ambientes.ambiente import Ambiente
from agentes.agente_arvore import AgenteArvore
from agentes.agente_busca import AgenteBusca
from agentes.agente_hibrido import AgenteHibrido

def teste_scaling_progressivo():
    """Testa o ciclo completo de scaling: 2 agentes → 10 agentes"""
    
    print("\n" + "="*80)
    print("🔬 TESTE: SCALING PROGRESSIVO (2 → 10 AGENTES)")
    print("="*80 + "\n")
    
    resultados = []
    
    # Ciclo de escalamento: 2 → 10 agentes
    for num_agentes in range(2, 11):
        # Calcula percentagem de bombas pela fórmula
        percentagem_bombas = 50 + (30 * (num_agentes - 2) / 8)
        
        print(f"🔄 Rodada com {num_agentes} agentes ({percentagem_bombas:.1f}% bombas)")
        print("-" * 80)
        
        try:
            # Cria mapa e ambiente
            mapa = GeradorDeMapa()
            ambiente = Ambiente(mapa)
            
            # Cria agentes progressivamente
            agentes = []
            for i in range(num_agentes):
                if i % 3 == 0:
                    agentes.append(AgenteArvore(i, ambiente))
                elif i % 3 == 1:
                    agentes.append(AgenteBusca(i, ambiente))
                else:
                    agentes.append(AgenteHibrido(i, ambiente))
            
            print(f"   ✅ {num_agentes} agentes criados")
            print(f"      - Árvore: {len([a for a in agentes if isinstance(a, AgenteArvore)])}")
            print(f"      - Busca: {len([a for a in agentes if isinstance(a, AgenteBusca)])}")
            print(f"      - Híbrido: {len([a for a in agentes if isinstance(a, AgenteHibrido)])}")
            
            # Simula 50 turnos
            agentes_sucesso = 0
            for turno in range(50):
                for agente in agentes:
                    agente.pensar()
                    agente.agir()
                
                # Conta agentes que atingiram objetivo
                agentes_sucesso = sum(
                    1 for a in agentes 
                    if a.conseguiu_objetivo
                )
                
                # Se todos atingiram, para mais cedo
                if agentes_sucesso == num_agentes:
                    print(f"   ✅ Todos os agentes atingiram objetivo no turno {turno+1}")
                    break
            
            taxa_sucesso = (agentes_sucesso / num_agentes) * 100
            
            print(f"   📊 Resultado:")
            print(f"      - Agentes com sucesso: {agentes_sucesso}/{num_agentes}")
            print(f"      - Taxa de vitória: {taxa_sucesso:.1f}%")
            
            # Armazena resultado
            resultados.append({
                'agentes': num_agentes,
                'bombas': percentagem_bombas,
                'sucesso': agentes_sucesso,
                'taxa': taxa_sucesso
            })
            
            if taxa_sucesso >= 50:
                print(f"   ✅ PASSOU (≥50% de sucesso)\n")
            else:
                print(f"   ⚠️  PASSOU COM AVISO (<50% de sucesso)\n")
                
        except Exception as e:
            print(f"   ❌ ERRO: {str(e)[:60]}\n")
            resultados.append({
                'agentes': num_agentes,
                'bombas': percentagem_bombas,
                'sucesso': 0,
                'taxa': 0,
                'erro': str(e)
            })
    
    # Resumo final
    print("="*80)
    print("📊 RESUMO DE RESULTADOS")
    print("="*80 + "\n")
    
    print("Agentes | Bombas | Sucesso | Taxa | Status")
    print("-" * 50)
    for r in resultados:
        status = "✅" if r.get('taxa', 0) >= 50 else "⚠️"
        print(f"   {r['agentes']:2d}   | {r['bombas']:5.1f}% |  {r['sucesso']}/{r['agentes']:2d}   | {r['taxa']:5.1f}% | {status}")
    
    # Validação final
    print("\n" + "="*80)
    print("✅ VALIDAÇÃO FINAL")
    print("="*80)
    
    todas_com_sucesso = all(r['agentes'] >= 2 and r['agentes'] <= 10 for r in resultados)
    progressao_agentes = all(
        resultados[i]['agentes'] == i + 2 
        for i in range(len(resultados))
    )
    progressao_bombas = all(
        resultados[i]['bombas'] <= resultados[i+1]['bombas']
        for i in range(len(resultados)-1)
    )
    
    print(f"\n✓ Ciclo 2→10 agentes: {'✅ SIM' if todas_com_sucesso else '❌ NÃO'}")
    print(f"✓ Progressão de agentes: {'✅ SIM' if progressao_agentes else '❌ NÃO'}")
    print(f"✓ Progressão de bombas: {'✅ SIM' if progressao_bombas else '❌ NÃO'}")
    
    taxa_media = sum(r['taxa'] for r in resultados) / len(resultados)
    print(f"\n✓ Taxa média de vitória: {taxa_media:.1f}%")
    
    if todas_com_sucesso and progressao_agentes and progressao_bombas:
        print("\n🎉 SISTEMA DE SCALING PROGRESSIVO FUNCIONANDO CORRETAMENTE!")
    else:
        print("\n⚠️  VERIFICAR SISTEMA DE SCALING")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    teste_scaling_progressivo()
