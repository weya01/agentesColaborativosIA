"""
Teste de alternância entre abordagens (sem crashes)
Simula o que acontece quando o utilizador alterna A->B->C->A...
"""
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PySide6.QtWidgets import QApplication

from ambientes import GeradorMapaValido
from agentes.memoria_partilhada import MemoriaPartilhada
from ui.janela_principal import gerar_agentes_aleatorios
from ui.grid_mapa import GridMapa
from utils.constantes import ModoJogo

def testar_alternancia():
    """Testa alternância rápida entre abordagens (simula cliques do utilizador)"""
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    print("\n" + "="*60)
    print("TESTE DE ALTERNÂNCIA ENTRE ABORDAGENS")
    print("="*60)
    
    abordagens = [
        (ModoJogo.A_TESOUROS, "A - Tesouros"),
        (ModoJogo.B_SOBREVIVENCIA, "B - Sobrevivência"),
        (ModoJogo.C_BANDEIRA, "C - Bandeira"),
    ]
    
    grid_mapa = None
    memoria = None
    agentes = []
    
    # Simula 3 ciclos de alternância (9 mudanças total)
    for ciclo in range(3):
        print(f"\nCiclo {ciclo + 1}:")
        for modo, nome in abordagens:
            try:
                print(f"  Alternando para {nome}...", end=" ")
                
                # Gera mapa
                gerador = GeradorMapaValido(10, modo)
                mapa, relatorio = gerador.gerar_com_relatorio()
                
                if not relatorio.get('sucesso'):
                    print(f"❌ Mapa não gerou")
                    return False
                
                # Remove GridMapa anterior (isto causava crashes!)
                if grid_mapa is not None:
                    try:
                        grid_mapa.deleteLater()
                        grid_mapa = None
                    except Exception as e:
                        print(f"⚠️  Erro ao deletar GridMapa anterior: {e}")
                        grid_mapa = None
                
                # Cria nova memória e agentes
                memoria = MemoriaPartilhada()
                agentes = gerar_agentes_aleatorios(mapa, memoria)
                
                # Cria GridMapa
                try:
                    grid_mapa = GridMapa(mapa, memoria)
                except Exception as e:
                    print(f"❌ Erro ao criar GridMapa: {e}")
                    return False
                
                # Atualiza renderização
                try:
                    grid_mapa.atualizar(agentes)
                except Exception as e:
                    print(f"❌ Erro ao atualizar: {e}")
                    return False
                
                print(f"✅ OK")
                
            except Exception as e:
                print(f"❌ ERRO: {e}")
                import traceback
                traceback.print_exc()
                return False
    
    print(f"\n{'='*60}")
    print(f"Resultado: ✅ 9 alternâncias SEM CRASHES!")
    print(f"{'='*60}\n")
    
    return True

if __name__ == "__main__":
    ok = testar_alternancia()
    sys.exit(0 if ok else 1)
