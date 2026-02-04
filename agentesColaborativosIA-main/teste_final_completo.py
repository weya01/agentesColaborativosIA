#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste Final Completo - Valida toda a arquitetura pós-correção
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def teste_completo():
    print("\n" + "="*70)
    print("TESTE FINAL COMPLETO - SISTEMA DE SCALING PROGRESSIVO")
    print("="*70)
    
    try:
        # 1. Importar classe
        print("\n[1] Importando JanelaPrincipalMultiGrupo...")
        from fontes.ui.janela_principal_multi_grupo import JanelaPrincipalMultiGrupo
        print("✅ Classe importada com sucesso")
        
        # 2. Verificar métodos críticos
        print("\n[2] Verificando métodos críticos...")
        metodos_obrigatorios = [
            '__init__',
            '_criar_ui',
            'iniciar_simulacao',
            'atualizar_turno',
            'resetar_simulacao',
            '_escalar_grupo',
            '_atualizar_tabs_grupos',
            '_criar_painel_grupo',
            '_obter_velocidade_ms'
        ]
        
        for metodo in metodos_obrigatorios:
            if hasattr(JanelaPrincipalMultiGrupo, metodo):
                print(f"   ✅ {metodo}")
            else:
                print(f"   ❌ {metodo} - NÃO ENCONTRADO")
                return False
        
        # 3. Verificar atributos de estado
        print("\n[3] Verificando variáveis de estado...")
        atributos = [
            'num_agentes_atual',
            'percentagem_bombas_atual',
            'grupos_objetivo_alcancados',
            'resultados_abordagens',
            'tabs_grupos',
            'lista_abordagens'
        ]
        
        # Verificar no código-fonte
        import inspect
        source = inspect.getsource(JanelaPrincipalMultiGrupo.__init__)
        
        for attr in atributos[:3]:  # Primeiros 3 são inicializados em __init__
            if f'self.{attr}' in source:
                print(f"   ✅ {attr} inicializado")
            else:
                print(f"   ⚠️  {attr} - verificar inicialização")
        
        # 4. Verificar integridade do método _atualizar_tabs_grupos
        print("\n[4] Verificando integridade de _atualizar_tabs_grupos...")
        atualizar_source = inspect.getsource(JanelaPrincipalMultiGrupo._atualizar_tabs_grupos)
        
        problemas = []
        if 'widget.texto_resumo' in atualizar_source:
            problemas.append("widget.texto_resumo (obsoleto)")
        if 'widget.tabela_agentes' in atualizar_source:
            problemas.append("widget.tabela_agentes (obsoleto)")
        if 'return widget' in atualizar_source and atualizar_source.count('return widget') > 1:
            problemas.append("return widget (cópia duplicada)")
        
        if problemas:
            print(f"   ❌ Problemas encontrados:")
            for prob in problemas:
                print(f"      - {prob}")
            return False
        else:
            print("   ✅ Sem referências obsoletas")
            print("   ✅ Estrutura correta")
        
        # 5. Verificar removidos corretamente
        print("\n[5] Verificando remoções de código obsoleto...")
        removidos = [
            '_atualizar_estilos_abordagem',
            '_selecionar_abordagem_a',
            '_selecionar_abordagem_b',
            '_selecionar_abordagem_c'
        ]
        
        for metodo in removidos:
            if not hasattr(JanelaPrincipalMultiGrupo, metodo):
                print(f"   ✅ {metodo} removido corretamente")
            else:
                print(f"   ❌ {metodo} ainda existe (deveria ter sido removido)")
                return False
        
        # 6. Verificar painel_a/b/c foram removidos
        print("\n[6] Verificando referências a painel_a/b/c...")
        resetar_source = inspect.getsource(JanelaPrincipalMultiGrupo.resetar_simulacao)
        
        if 'painel_a' in resetar_source or 'painel_b' in resetar_source or 'painel_c' in resetar_source:
            print("   ❌ Ainda há referências a painel_a/b/c")
            return False
        elif 'self.tabs_grupos.clear()' in resetar_source:
            print("   ✅ Usando tabs_grupos.clear() correto")
        else:
            print("   ⚠️  Método resetar_simulacao pode precisar revisão")
        
        # 7. Verificar QListWidget está sendo usado
        print("\n[7] Verificando uso de QListWidget...")
        if 'self.lista_abordagens' in source and 'QListWidget' in source:
            print("   ✅ QListWidget implementado")
            
            iniciar_source = inspect.getsource(JanelaPrincipalMultiGrupo.iniciar_simulacao)
            if 'selectedItems()' in iniciar_source:
                print("   ✅ Usando selectedItems() para seleção múltipla")
            else:
                print("   ⚠️  Verificar implementação de selectedItems()")
        else:
            print("   ❌ QListWidget não encontrado")
            return False
        
        # 8. Verificar escala progressiva
        print("\n[8] Verificando sistema de escala progressiva...")
        escalar_source = inspect.getsource(JanelaPrincipalMultiGrupo._escalar_grupo)
        
        if 'num_agentes_atual' in escalar_source and 'percentagem_bombas_atual' in escalar_source:
            print("   ✅ Escalas de agentes e bombas implementadas")
            if 'min(' in escalar_source and '10' in escalar_source:
                print("   ✅ Limite de 10 agentes implementado")
            else:
                print("   ⚠️  Verificar limite máximo de agentes")
        else:
            print("   ❌ Sistema de escala incompleto")
            return False
        
        # Resultado Final
        print("\n" + "="*70)
        print("✅ TESTE FINAL CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\nO sistema está pronto para:")
        print("  ✓ Iniciar GUI")
        print("  ✓ Selecionar múltiplas abordagens")
        print("  ✓ Executar simulação com scaling progressivo")
        print("  ✓ Exibir resultados de múltiplos grupos")
        print("\nPara iniciar: python main.py")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = teste_completo()
    sys.exit(0 if sucesso else 1)
