"""
Script de verificação de estrutura do projeto.
Valida que todos os ficheiros necessários existem e sem duplicados.
"""
import os
from pathlib import Path

def verificar_estrutura():
    """Verifica estrutura completa do projeto"""
    
    root = Path(__file__).parent / "fontes"
    raiz = Path(__file__).parent
    
    print("=" * 60)
    print("VERIFICAÇÃO DE ESTRUTURA DO PROJETO")
    print("=" * 60)
    
    # Estrutura esperada
    estrutura_esperada = {
        "agentes": {
            "base": ["__init__.py", "agente_base.py"],
            "agentes_busca": ["__init__.py", "agente_busca.py"],
            "agentes_nao_busca": ["__init__.py", "agente_nao_busca.py"],
            "agentes_hibridos": ["__init__.py", "agente_hibrido.py"],
            "files": ["__init__.py", "memoria_partilhada.py"]
        },
        "ambientes": {
            "files": ["__init__.py", "gerador_de_mapa.py", "validador.py", "manutencao_mapa.py"]
        },
        "metricas": {
            "files": ["__init__.py", "metricas.py", "gestor_metricas.py"]
        },
        "simulacao": {
            "files": ["__init__.py", "motor.py", "modos_de_jogo.py"]
        },
        "ui": {
            "files": ["__init__.py", "cores.py", "grid_mapa.py", "janela_principal.py", "painel_interacao.py"]
        },
        "utils": {
            "files": ["__init__.py", "constantes.py"]
        }
    }
    
    # Verifica cada pasta
    erros = []
    sucesso = []
    
    for pasta, conteudo in estrutura_esperada.items():
        pasta_path = root / pasta
        
        if not pasta_path.exists():
            erros.append(f"✗ Pasta {pasta}/ não existe")
            continue
        
        # Verifica subpastas
        for subpasta, arquivos in conteudo.items():
            if subpasta == "files":
                # Verifica ficheiros diretos
                for arquivo in arquivos:
                    arquivo_path = pasta_path / arquivo
                    if arquivo_path.exists():
                        sucesso.append(f"✓ {pasta}/{arquivo}")
                    else:
                        erros.append(f"✗ {pasta}/{arquivo} não existe")
            else:
                # Verifica subpasta
                subpasta_path = pasta_path / subpasta
                if not subpasta_path.exists():
                    erros.append(f"✗ {pasta}/{subpasta}/ não existe")
                    continue
                
                for arquivo in arquivos:
                    arquivo_path = subpasta_path / arquivo
                    if arquivo_path.exists():
                        sucesso.append(f"✓ {pasta}/{subpasta}/{arquivo}")
                    else:
                        erros.append(f"✗ {pasta}/{subpasta}/{arquivo} não existe")
    
    # Verifica ficheiros principais
    ficheiros_main = [
        ("fontes/main.py", root / "main.py"),
        ("validar_arquitetura.py", raiz / "validar_arquitetura.py")
    ]
    for nome, f_path in ficheiros_main:
        if f_path.exists():
            sucesso.append(f"✓ {nome}")
        else:
            erros.append(f"✗ {nome} não existe")
    
    # Exibe resultados
    print("\n✓ FICHEIROS CORRETOS:")
    for s in sucesso:
        print(f"  {s}")
    
    if erros:
        print("\n✗ ERROS ENCONTRADOS:")
        for e in erros:
            print(f"  {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ ESTRUTURA COMPLETA E CORRETA!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    sucesso = verificar_estrutura()
    exit(0 if sucesso else 1)
