"""
Modelos de Aprendizagem de Máquina para Decisão de Movimento.

Implementa 3 técnicas: Árvore de Decisão, KNN e Naive Bayes.
"""
from enum import Enum
import random
from typing import Tuple, List


class TecnicaML(Enum):
    """Técnicas de ML disponíveis"""
    ARVORE_DECISAO = "arvore_decisao"
    KNN = "knn"
    NAIVE_BAYES = "naive_bayes"
    ALEATORIO = "aleatorio"


class ModeloDecisao:
    """Interface base para modelos de decisão"""
    
    def decidir_movimento(self, percepcao: dict, historico: dict) -> Tuple[int, int]:
        """Retorna próximo movimento (dx, dy)"""
        raise NotImplementedError


class ArvoreDecisao(ModeloDecisao):
    """
    Modelo de Árvore de Decisão para exploração.
    
    Regras:
    1. Se célula vizinha é tesouro: ir para tesouro
    2. Se célula vizinha é livre e não explorada: ir
    3. Se célula vizinha é bomba conhecida: evitar
    4. Senão: explorar seguramente
    """
    
    def decidir_movimento(self, percepcao: dict, historico: dict) -> Tuple[int, int]:
        """Usa árvore de decisão para escolher movimento"""
        vizinhos = percepcao.get('vizinhos', {})
        exploradas = historico.get('exploradas', set())
        
        # Nó 1: Há tesouros?
        tesouros = [pos for pos, tipo in vizinhos.items() if tipo == 'T']
        if tesouros:
            return random.choice(tesouros)
        
        # Nó 2: Há células livres não exploradas?
        livres_novos = [pos for pos, tipo in vizinhos.items() 
                       if tipo == 'L' and pos not in exploradas]
        if livres_novos:
            return random.choice(livres_novos)
        
        # Nó 3: Há células livres já exploradas (mas seguras)?
        livres_seguros = [pos for pos, tipo in vizinhos.items() if tipo == 'L']
        if livres_seguros:
            return random.choice(livres_seguros)
        
        # Nó 4: Senão, não mover (exploração travada)
        return (0, 0)


class ModeloKNN(ModeloDecisao):
    """
    Modelo KNN (K-Nearest Neighbors) para exploração.
    
    Classifica próximo movimento baseado em similaridade
    com movimentos bem-sucedidos anteriores.
    """
    
    def __init__(self, k: int = 3):
        self.k = k
        self.historico_movimentos = []  # [(vizinhos, movimento_feito, sucesso), ...]
    
    def registrar_movimento(self, vizinhos: dict, movimento: Tuple, sucesso: bool):
        """Registra movimento bem-sucedido ou falhado"""
        self.historico_movimentos.append((vizinhos, movimento, sucesso))
    
    def decidir_movimento(self, percepcao: dict, historico: dict) -> Tuple[int, int]:
        """Usa KNN para escolher movimento similar aos bem-sucedidos"""
        vizinhos = percepcao.get('vizinhos', {})
        exploradas = historico.get('exploradas', set())
        
        # Se não tem histórico, usa heurística simples
        if not self.historico_movimentos:
            livres = [pos for pos, tipo in vizinhos.items() if tipo == 'L']
            return random.choice(livres) if livres else (0, 0)
        
        # Encontra K vizinhos similares com sucesso
        sucessos = [(mov, sim) for viz, mov, suc in self.historico_movimentos 
                   if suc for sim in [self._similaridade(vizinhos, viz)]]
        
        if sucessos:
            sucessos.sort(key=lambda x: x[1], reverse=True)
            movimento_similar = sucessos[0][0]
            return movimento_similar
        
        # Fallback: livres não explorados
        livres_novos = [pos for pos, tipo in vizinhos.items() 
                       if tipo == 'L' and pos not in exploradas]
        return random.choice(livres_novos) if livres_novos else (0, 0)
    
    def _similaridade(self, viz1: dict, viz2: dict) -> float:
        """Calcula similaridade entre duas perceções"""
        if not viz1 or not viz2:
            return 0.0
        
        # Compara tipos de células vizinhas
        tipo1 = [tipo for tipo in viz1.values()]
        tipo2 = [tipo for tipo in viz2.values()]
        
        # Simples: % de células com mesmo tipo
        iguais = sum(1 for t1, t2 in zip(tipo1, tipo2) if t1 == t2)
        return iguais / len(tipo1) if tipo1 else 0.0


class NaiveBayes(ModeloDecisao):
    """
    Modelo Naive Bayes para exploração.
    
    Calcula probabilidade de sucesso para cada tipo de movimento
    baseado em histórico de ações passadas.
    """
    
    def __init__(self):
        # {tipo_movimento: {'sucessos': n, 'tentativas': n}}
        self.probabilidades = {
            'L': {'sucessos': 0, 'tentativas': 0},
            'T': {'sucessos': 0, 'tentativas': 0},
            'B': {'sucessos': 0, 'tentativas': 0},
            'desconhecida': {'sucessos': 0, 'tentativas': 0}
        }
    
    def registrar_resultado(self, tipo_celula: str, sucesso: bool):
        """Registra resultado de movimento para uma celula"""
        if tipo_celula not in self.probabilidades:
            tipo_celula = 'desconhecida'
        
        self.probabilidades[tipo_celula]['tentativas'] += 1
        if sucesso:
            self.probabilidades[tipo_celula]['sucessos'] += 1
    
    def obter_probabilidade(self, tipo_celula: str) -> float:
        """Calcula P(sucesso | tipo_celula)"""
        if tipo_celula not in self.probabilidades:
            tipo_celula = 'desconhecida'
        
        stats = self.probabilidades[tipo_celula]
        if stats['tentativas'] == 0:
            return 0.5  # Probabilidade neutra
        
        return stats['sucessos'] / stats['tentativas']
    
    def decidir_movimento(self, percepcao: dict, historico: dict) -> Tuple[int, int]:
        """Usa Naive Bayes para escolher movimento mais provável de sucesso"""
        vizinhos = percepcao.get('vizinhos', {})
        
        # Calcula probabilidade para cada vizinho
        probabilidades = {}
        for pos, tipo in vizinhos.items():
            prob = self.obter_probabilidade(tipo)
            probabilidades[pos] = prob
        
        if not probabilidades:
            return (0, 0)
        
        # Escolhe posição com maior probabilidade
        melhor_pos = max(probabilidades, key=probabilidades.get)
        return melhor_pos


class GestorModelos:
    """Gerencia múltiplos modelos de ML para um agente"""
    
    def __init__(self, agente_id: str, tecnicas: List[TecnicaML] = None):
        self.agente_id = agente_id
        self.tecnicas = tecnicas or [TecnicaML.ARVORE_DECISAO, TecnicaML.KNN, TecnicaML.NAIVE_BAYES]
        
        self.modelos = {
            TecnicaML.ARVORE_DECISAO: ArvoreDecisao(),
            TecnicaML.KNN: ModeloKNN(),
            TecnicaML.NAIVE_BAYES: NaiveBayes(),
        }
        
        self.tecnica_atual = self.tecnicas[0]
        self.historico_decisoes = []
    
    def decidir_movimento(self, percepcao: dict, historico: dict) -> Tuple[int, int]:
        """Usa tecnica atual para decidir movimento"""
        modelo = self.modelos.get(self.tecnica_atual)
        if modelo:
            return modelo.decidir_movimento(percepcao, historico)
        return (0, 0)
    
    def trocar_tecnica(self, tecnica: TecnicaML):
        """Alterna técnica de decisão durante execução"""
        if tecnica in self.modelos:
            self.tecnica_atual = tecnica
    
    def obter_tecnica_atual(self) -> str:
        """Retorna nome da técnica atual"""
        return self.tecnica_atual.value

