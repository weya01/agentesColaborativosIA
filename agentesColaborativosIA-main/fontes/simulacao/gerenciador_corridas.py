"""
Gerenciador de Grupos Isolados.

Implementa simulação multi-grupo com isolamento lógico:
- A, B, C correm SIMULTANEAMENTE
- Cada grupo tem seu próprio mapa lógico (ambiente isolado)
- Visualização no MESMO mapa visual (agentes de cores diferentes)
- Agentes não se veem ou interferem mutuamente
- Resultados comparáveis entre grupos
"""
from enum import Enum
from simulacao.motor import MotorSimulacao
from ambientes.gerador_de_mapa import GeradorDeMapa
from agentes.memoria_partilhada import MemoriaPartilhada
from copy import deepcopy


class Abordagem(Enum):
    """Abordagens do problema"""
    A = "A"
    B = "B"
    C = "C"


class ResultadoCorrida:
    """Armazena resultados de uma corrida"""
    
    def __init__(self, abordagem, modo, turno_final, objetivo_alcancado, agentes_metricas):
        self.abordagem = abordagem
        self.modo = modo
        self.turno_final = turno_final
        self.objetivo_alcancado = objetivo_alcancado
        self.agentes_metricas = agentes_metricas
        self.timestamp = None


class MapaIsolado:
    """Wrapper que fornece vista isolada do mapa para cada grupo"""
    
    def __init__(self, mapa_original, grupo_id):
        """
        Args:
            mapa_original: Mapa base (lista 2D ou objeto com atributos)
            grupo_id: ID do grupo (determina a cor visual)
        """
        self.mapa_original = mapa_original
        self.grupo_id = grupo_id
        
        # Se é uma lista (2D), extrai tamanho
        if isinstance(mapa_original, list):
            self.tamanho = len(mapa_original)
        else:
            # Se é um objeto, usa atributo tamanho
            self.tamanho = mapa_original.tamanho
    
    def ver(self, pos):
        """Retorna conteúdo da célula (mesmo para todos os grupos)"""
        if isinstance(self.mapa_original, list):
            # Acessa lista 2D
            linha, coluna = pos
            if 0 <= linha < len(self.mapa_original) and 0 <= coluna < len(self.mapa_original[0]):
                return self.mapa_original[linha][coluna]
            return None
        else:
            # Usa método do objeto
            return self.mapa_original.ver(pos)
    
    def vizinhos(self, pos):
        """Retorna vizinhos da célula"""
        if isinstance(self.mapa_original, list):
            # Calcula vizinhos manualmente para lista
            linha, coluna = pos
            vizinhos_pos = []
            for dl, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nl, nc = linha + dl, coluna + dc
                if 0 <= nl < self.tamanho and 0 <= nc < self.tamanho:
                    vizinhos_pos.append((nl, nc))
            return vizinhos_pos
        else:
            # Usa método do objeto
            return self.mapa_original.vizinhos(pos)
    
    def esta_dentro(self, pos):
        """Verifica se posição está dentro do mapa"""
        if isinstance(self.mapa_original, list):
            linha, coluna = pos
            return 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho
        else:
            # Usa método do objeto
            return self.mapa_original.esta_dentro(pos)
    
    def coletar_tesouro(self, pos):
        """Coleta tesouro de forma isolada (por grupo)"""
        if isinstance(self.mapa_original, list):
            # Para listas, apenas retorna True (sucesso)
            return True
        else:
            # Apenas marca como coletado, não altera mapa original
            return self.mapa_original.coletar_tesouro(pos)
    
    def acionar_bomba(self, pos):
        """Aciona bomba de forma isolada (por grupo)"""
        if isinstance(self.mapa_original, list):
            # Para listas, apenas retorna True (sucesso)
            return True
        else:
            # Apenas marca como acionada, não altera mapa original
            return self.mapa_original.acionar_bomba(pos)


class GerenciadorGrupos:
    """Gerencia múltiplos grupos executando simultaneamente com isolamento lógico"""
    
    def __init__(self):
        """Inicializa gerenciador de grupos"""
        self.grupos = {}  # {grupo_id: {'abordagem', 'modo', 'mapa', 'agentes', 'memoria', 'motor'}}
        self.resultados = {}  # {grupo_id: ResultadoCorrida}
        self.turno_atual = 0
        self.simulacao_ativa = True
        
    
    def criar_grupo(self, grupo_id, abordagem, modo, agentes_factory, num_agentes=None, percentagem_bombas=None, numero_grupo=None):
        """
        Cria um novo grupo isolado.
        
        Args:
            grupo_id: ID único do grupo (0, 1, 2 para A, B, C)
            abordagem: Abordagem ('A', 'B', 'C')
            modo: Modo de jogo (ModoJogo enum)
            agentes_factory: Função que cria agentes: f(mapa, memoria, num) -> lista_agentes
            num_agentes: Número de agentes (se None, aleatório entre 2-10)
            percentagem_bombas: Percentagem de bombas (50-80)
            numero_grupo: Número sequencial do grupo para cor (1, 2, 3, ...)
            
        Returns:
            Dict com configuração do grupo
        """
        import random
        
        # Gera número aleatório se não especificado
        if num_agentes is None:
            num_agentes = random.randint(2, 10)
        
        # Cria mapa isolado para este grupo COM PERCENTAGEM DE BOMBAS
        gerador = GeradorDeMapa(tamanho=10, modo=modo, percentagem_bombas=percentagem_bombas)
        mapa_base = gerador.gerar()
        mapa_isolado = MapaIsolado(mapa_base, grupo_id)
        
        # Cria memória isolada para este grupo
        memoria = MemoriaPartilhada()
        
        # Cria agentes isolados para este grupo
        agentes = agentes_factory(mapa_isolado, memoria, num_agentes)
        
        # Define grupo_id em cada agente
        for agente in agentes:
            agente.grupo_id = grupo_id
            # Se numero_grupo foi fornecido, adiciona também
            if numero_grupo is not None:
                agente.numero_grupo = numero_grupo
        
        # Cria motor isolado para este grupo
        motor = MotorSimulacao(
            mapa=mapa_isolado,
            agentes=agentes,
            memoria=memoria,
            modo=abordagem,
            max_turnos=500,
            grupo_id=grupo_id
        )
        
        # Armazena grupo
        self.grupos[grupo_id] = {
            'abordagem': abordagem,
            'modo': modo,
            'mapa_original': mapa_base,  # Para visualização
            'mapa_isolado': mapa_isolado,  # Para lógica
            'agentes': agentes,
            'memoria': memoria,
            'motor': motor,
            'num_agentes': num_agentes,
            'terminou': False
        }
        
        return self.grupos[grupo_id]
    
    def executar_turno_todos(self):
        """
        Executa um turno para TODOS os grupos simultaneamente.
        
        Returns:
            Dict {grupo_id: {'terminou', 'objetivo_alcancado'}}
        """
        self.turno_atual += 1
        resultado_turno = {}
        
        for grupo_id, grupo_info in self.grupos.items():
            if grupo_info['terminou']:
                resultado_turno[grupo_id] = {
                    'terminou': True,
                    'objetivo_alcancado': grupo_info['motor'].objetivo_alcancado
                }
                continue
            
            # Executa um turno para este grupo
            grupo_info['motor'].executar_um_turno()
            
            # Verifica se objetivo foi alcançado
            objetivo = grupo_info['motor'].verificar_objetivo_rapido()
            
            # Verifica se terminou
            terminou = grupo_info['motor']._fim()
            
            grupo_info['terminou'] = terminou
            
            resultado_turno[grupo_id] = {
                'terminou': terminou,
                'objetivo_alcancado': objetivo
            }
        
        # Verifica se TODOS os grupos terminaram
        if all(g['terminou'] for g in self.grupos.values()):
            self.simulacao_ativa = False
        
        return resultado_turno
    
    def obter_agentes_por_grupo(self, grupo_id):
        """Retorna lista de agentes de um grupo específico"""
        if grupo_id not in self.grupos:
            return []
        return self.grupos[grupo_id]['agentes']
    
    def obter_todos_agentes(self):
        """Retorna dicionário com todos os agentes agrupados por ID"""
        todos_agentes = {}
        for grupo_id, grupo_info in self.grupos.items():
            for agente in grupo_info['agentes']:
                agente.grupo_id = grupo_id  # Garante que grupo_id está definido
                todos_agentes[agente.id] = agente
        return todos_agentes
    
    def obter_memorias_isoladas(self):
        """Retorna dicionário {grupo_id: memoria}"""
        return {grupo_id: grupo_info['memoria'] 
                for grupo_id, grupo_info in self.grupos.items()}
    
    def terminar_grupos(self):
        """
        Termina todos os grupos e coleta resultados finais.
        
        Returns:
            Dict {grupo_id: ResultadoCorrida}
        """
        for grupo_id, grupo_info in self.grupos.items():
            motor = grupo_info['motor']
            agentes = grupo_info['agentes']
            
            # Coleta métricas finais
            agentes_metricas = {}
            for agente in agentes:
                agentes_metricas[agente.id] = agente.obter_metricas()
            
            # Cria resultado
            resultado = ResultadoCorrida(
                abordagem=grupo_info['abordagem'],
                modo=grupo_info['modo'],
                turno_final=motor.turno_atual,
                objetivo_alcancado=motor.objetivo_alcancado,
                agentes_metricas=agentes_metricas
            )
            
            self.resultados[grupo_id] = resultado
        
        self.simulacao_ativa = False
        return self.resultados
    
    def obter_resultado_grupo(self, grupo_id):
        """Obtém resultado de um grupo específico"""
        return self.resultados.get(grupo_id)
    
    def comparar_grupos(self):
        """
        Compara resultados de todos os grupos.
        
        Returns:
            Dict com comparação
        """
        if not self.resultados:
            return {}
        
        comparacao = {
            'grupos': {},
            'melhor_objetivo': None,
            'melhor_tempo': None,
            'melhor_eficiencia': None
        }
        
        melhores = {
            'objetivo': (None, False),  # (grupo_id, alcancado)
            'tempo': (None, float('inf')),  # (grupo_id, turnos)
            'eficiencia': (None, -1)  # (grupo_id, eficiencia)
        }
        
        for grupo_id, resultado in self.resultados.items():
            info = {
                'abordagem': resultado.abordagem,
                'objetivo_alcancado': resultado.objetivo_alcancado,
                'turno_final': resultado.turno_final,
                'num_agentes': len(resultado.agentes_metricas),
                'agentes': resultado.agentes_metricas
            }
            
            comparacao['grupos'][grupo_id] = info
            
            # Atualiza melhores
            if resultado.objetivo_alcancado and not melhores['objetivo'][1]:
                melhores['objetivo'] = (grupo_id, True)
            
            if resultado.turno_final < melhores['tempo'][1]:
                melhores['tempo'] = (grupo_id, resultado.turno_final)
            
            # Calcula eficiência média dos agentes
            eficiencias = []
            for metricas in resultado.agentes_metricas.values():
                eficiencias.append(metricas.get('eficiencia', 0))
            
            eficiencia_media = sum(eficiencias) / len(eficiencias) if eficiencias else 0
            if eficiencia_media > melhores['eficiencia'][1]:
                melhores['eficiencia'] = (grupo_id, eficiencia_media)
        
        # Registra melhores
        if melhores['objetivo'][0] is not None:
            comparacao['melhor_objetivo'] = melhores['objetivo'][0]
        if melhores['tempo'][0] is not None:
            comparacao['melhor_tempo'] = melhores['tempo'][0]
        if melhores['eficiencia'][0] is not None:
            comparacao['melhor_eficiencia'] = melhores['eficiencia'][0]
        
        return comparacao
    
    def resetar(self):
        """Reseta gerenciador para novo ciclo de simulação"""
        self.grupos = {}
        self.resultados = {}
        self.turno_atual = 0
        self.simulacao_ativa = False

