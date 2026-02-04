"""
TESTE FINAL COMPLETO
Simula uma sessão real: gerar abordagem, rodar turnos, alternar
"""
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6.QtWidgets import QApplication

from ambientes import GeradorMapaValido
from agentes.memoria_partilhada import MemoriaPartilhada
from ui.janela_principal import gerar_agentes_aleatorios
from ui.grid_mapa import GridMapa
from simulacao.motor import MotorSimulacao
from utils.constantes import ModoJogo

def testar_sessao_completa():
    """Testa uma sessão completa: gerar -> renderizar -> rodar turnos -> alternar"""
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    print("\n" + "="*70)
    print("TESTE FINAL COMPLETO - SESSÃO REALISTA")
    print("="*70)
    
    abordagens = [
        (ModoJogo.A_TESOUROS, "A - Tesouros (50% descobertos)"),
        (ModoJogo.B_SOBREVIVENCIA, "B - Sobrevivência (80% explorado)"),
        (ModoJogo.C_BANDEIRA, "C - Bandeira"),
    ]
    
    todos_ok = True
    
    for modo, nome_completo in abordagens:
        print(f"\n{'─'*70}")
        print(f"Testando: {nome_completo}")
        print(f"{'─'*70}")
        
        try:
            # 1. GERAR MAPA
            print("  1️⃣  Gerando mapa...", end=" ")
            gerador = GeradorMapaValido(10, modo)
            mapa, relatorio = gerador.gerar_com_relatorio()
            
            if not relatorio.get('sucesso'):
                print(f"❌ FALHA: {relatorio.get('mensagem')}")
                todos_ok = False
                continue
            
            print(f"✅ OK ({relatorio.get('percentual_acessivel', 0):.0f}% acessível)")
            
            # 2. CRIAR AGENTES
            print("  2️⃣  Gerando agentes...", end=" ")
            memoria = MemoriaPartilhada()
            agentes = gerar_agentes_aleatorios(mapa, memoria)
            print(f"✅ OK ({len(agentes)} agentes)")
            
            # 3. RENDERIZAR
            print("  3️⃣  Renderizando GridMapa...", end=" ")
            grid_mapa = GridMapa(mapa, memoria)
            grid_mapa.atualizar(agentes)
            print(f"✅ OK (100 células)")
            
            # 4. CRIAR MOTOR DE SIMULAÇÃO
            print("  4️⃣  Iniciando motor...", end=" ")
            motor = MotorSimulacao(
                mapa=mapa,
                agentes=agentes,
                memoria=memoria,
                modo=modo
            )
            print(f"✅ OK")
            
            # 5. RODAR 5 TURNOS
            print("  5️⃣  Executando 5 turnos...", end=" ")
            for turno in range(1, 6):
                try:
                    for agente in agentes:
                        agente.executar_turno()
                    
                    # Atualiza renderização
                    grid_mapa.atualizar(agentes)
                    
                    # Verifica objetivo
                    objetivo_alcancado = motor.verificar_objetivo_rapido()
                    if objetivo_alcancado:
                        print(f"✅ OK (Objetivo atingido no turno {turno})")
                        break
                        
                except Exception as e:
                    print(f"❌ Turno {turno}: {e}")
                    todos_ok = False
                    break
            else:
                print(f"✅ OK (5 turnos completados)")
            
            # 6. ESTATÍSTICAS
            exploradas = len(memoria.obter_exploradas(grupo_id=0))
            print(f"  6️⃣  Estatísticas: {exploradas} células exploradas")
            
            print(f"\n✅ {nome_completo}: COMPLETO COM SUCESSO")
            
        except Exception as e:
            import traceback
            print(f"❌ ERRO GERAL: {e}")
            traceback.print_exc()
            todos_ok = False
    
    print(f"\n{'='*70}")
    if todos_ok:
        print("✅ TESTE FINAL: TODAS AS ABORDAGENS OK!")
        print("   Mapa gerado ✅ | Agentes ✅ | Renderização ✅ | Simulação ✅")
    else:
        print("❌ TESTE FINAL: ALGUMAS FALHAS")
    print(f"{'='*70}\n")
    
    return todos_ok

if __name__ == "__main__":
    ok = testar_sessao_completa()
    sys.exit(0 if ok else 1)
