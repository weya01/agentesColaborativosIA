"""
Teste de renderização GridMapa sem UI
Verifica se consegue atualizar sem crashes
"""
import sys
from ambientes import GeradorMapaValido
from agentes.memoria_partilhada import MemoriaPartilhada
from ui.janela_principal import gerar_agentes_aleatorios
from utils.constantes import ModoJogo

# Mock minimal do QApplication para não abrir janela
class MockQApplication:
    pass

def testar_renderizacao():
    """Testa renderização de GridMapa para todas as abordagens"""
    print("\n" + "="*60)
    print("TESTE DE RENDERIZAÇÃO GRIDMAPA")
    print("="*60)
    
    # Workaround: definir variável de ambiente para rendering headless
    import os
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    from ui.grid_mapa import GridMapa
    
    abordagens = [
        (ModoJogo.A_TESOUROS, "A - Tesouros"),
        (ModoJogo.B_SOBREVIVENCIA, "B - Sobrevivência"),
        (ModoJogo.C_BANDEIRA, "C - Bandeira")
    ]
    
    todos_ok = True
    
    for modo, nome in abordagens:
        try:
            print(f"\nTestando {nome}...")
            
            # Gera mapa
            gerador = GeradorMapaValido(10, modo)
            mapa, relatorio = gerador.gerar_com_relatorio()
            
            if not relatorio.get('sucesso'):
                print(f"  ❌ Mapa não gerou")
                todos_ok = False
                continue
            
            # Cria memória e agentes
            memoria = MemoriaPartilhada()
            agentes = gerar_agentes_aleatorios(mapa, memoria)
            
            # Cria GridMapa
            try:
                grid = GridMapa(mapa, memoria)
                print(f"  ✅ GridMapa criado")
            except Exception as e:
                print(f"  ❌ Erro ao criar GridMapa: {e}")
                todos_ok = False
                continue
            
            # Tenta atualizar renderização
            try:
                grid.atualizar(agentes)
                print(f"  ✅ Renderização atualizada")
            except Exception as e:
                print(f"  ❌ Erro ao atualizar renderização: {e}")
                todos_ok = False
                continue
            
            # Verifica células
            num_celulas = len(grid.celulas)
            print(f"  ✅ {num_celulas} células renderizadas")
            
            # Verifica agentes
            print(f"  ✅ {len(agentes)} agentes rendidos")
            
            print(f"  ✅ {nome}: TUDO OK!")
            
        except Exception as e:
            import traceback
            print(f"  ❌ ERRO geral: {e}")
            traceback.print_exc()
            todos_ok = False
    
    print(f"\n{'='*60}")
    print(f"Resultado: {'✅ TUDO OK!' if todos_ok else '❌ ALGUMAS FALHAS'}")
    print(f"{'='*60}\n")
    
    return todos_ok

if __name__ == "__main__":
    ok = testar_renderizacao()
    sys.exit(0 if ok else 1)
