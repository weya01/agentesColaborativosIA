"""
Memória Partilhada para grupos de agentes.

Cada grupo de agentes tem sua própria memória partilhada.
Permite que agentes do mesmo grupo compartilhem conhecimento sobre:
- Bombas encontradas
- Tesouros descobertos
- Células exploradas
- Células seguras
- Agentes mortos
"""


class MemoriaPartilhada:
    """
    Gerencia memória partilhada para grupos de agentes.
    Cada grupo tem sua própria memória isolada.
    """

    def __init__(self):
        """Inicializa estrutura de memória para múltiplos grupos"""
        self.grupos = {}  # {grupo_id: dados_grupo}

    def _garantir_grupo_existe(self, grupo_id):
        """Cria estrutura de grupo se não existir"""
        if grupo_id not in self.grupos:
            self.grupos[grupo_id] = {
                "visitados": {},           # {(x, y): tipo_celula}
                "bombas": set(),           # Posições com bombas
                "tesouros": set(),         # Posições com tesouros
                "bandeira": None,          # Posição da bandeira
                "celulas_exploradas": set(),  # Todas as células exploradas
                "celulas_seguras": set(),  # Células sem bomba confirmadas
                "celulas_percebidas": set(),  # Células próximas mas não visitadas
                "agentes_vivos": set(),    # Nomes dos agentes vivos
                "agentes_mortos": set(),   # Nomes dos agentes que morreram
                "tesouros_coletados": 0,   # Contador de tesouros coletados
                "posicoes_tesouro_coletado": set(),  # Posições de tesouro já coletado
                "historico": []            # Histórico de eventos
            }

    # =====================================================================
    # REGISTROS DE EXPLORAÇÃO
    # =====================================================================

    def registrar_explorada(self, posicao, tipo_celula, grupo_id):
        """
        Registra uma célula como explorada pelo agente.
        
        Args:
            posicao: Tupla (x, y)
            tipo_celula: "B" (bomba), "T" (tesouro), "F" (bandeira), "L" (livre)
            grupo_id: ID do grupo
        """
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["visitados"][posicao] = tipo_celula
        grupo["celulas_exploradas"].add(posicao)
        grupo["historico"].append(("explorada", posicao, tipo_celula))

    def registrar_bomba(self, posicao, grupo_id):
        """Registra descoberta de bomba"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["bombas"].add(posicao)
        grupo["historico"].append(("bomba", posicao))

    def registrar_tesouro(self, posicao, grupo_id):
        """Registra descoberta de tesouro"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["tesouros"].add(posicao)
        grupo["historico"].append(("tesouro", posicao))

    def registrar_bandeira(self, posicao, grupo_id):
        """Registra descoberta de bandeira"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["bandeira"] = posicao
        grupo["historico"].append(("bandeira", posicao))

    def registrar_segura(self, posicao, grupo_id):
        """Registra célula como segura (sem bomba)"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["celulas_seguras"].add(posicao)

    def registrar_percebido(self, posicao, grupo_id):
        """Registra célula percebida mas não visitada"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["celulas_percebidas"].add(posicao)

    # =====================================================================
    # REGISTROS DE AGENTES
    # =====================================================================

    def registrar_agente_vivo(self, nome_agente, grupo_id):
        """Registra agente como vivo no grupo"""
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        grupo["agentes_vivos"].add(nome_agente)

    def registrar_agente_morto(self, nome_agente, grupo_id):
        """
        Registra que um agente morreu.
        Todos os agentes do grupo são notificados via memória.
        """
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        grupo["agentes_vivos"].discard(nome_agente)
        grupo["agentes_mortos"].add(nome_agente)
        grupo["historico"].append(("agente_morto", nome_agente))

    def registrar_tesouro_coletado(self, nome_agente, grupo_id, posicao):
        """
        Registra que tesouro foi coletado por agente.
        Verifica se já foi coletado para evitar contagem dupla.
        
        Args:
            nome_agente: Nome do agente que coletou
            grupo_id: ID do grupo
            posicao: Posição (x, y) do tesouro coletado
        
        Returns:
            True se foi contado, False se já havia sido coletado
        """
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        # Verifica se já foi coletado antes
        if posicao in grupo["posicoes_tesouro_coletado"]:
            return False  # Já foi coletado
        
        # Registra nova coleta
        grupo["posicoes_tesouro_coletado"].add(posicao)
        grupo["tesouros_coletados"] += 1
        grupo["historico"].append(("tesouro_coletado", nome_agente, posicao))
        return True

    # =====================================================================
    # CONSULTAS DE INFORMAÇÃO
    # =====================================================================

    def obter_bombas(self, grupo_id):
        """Retorna set de todas as bombas conhecidas do grupo"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["bombas"].copy()

    def obter_tesouros(self, grupo_id):
        """Retorna set de todos os tesouros conhecidos do grupo"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["tesouros"].copy()

    def obter_bandeira(self, grupo_id):
        """Retorna posição da bandeira se encontrada, None caso contrário"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["bandeira"]

    def obter_exploradas(self, grupo_id):
        """Retorna set de todas as células exploradas"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["celulas_exploradas"].copy()

    def obter_seguras(self, grupo_id):
        """Retorna set de todas as células seguras"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["celulas_seguras"].copy()

    def obter_percebidas(self, grupo_id):
        """Retorna set de células percebidas"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["celulas_percebidas"].copy()

    def obter_agentes_vivos(self, grupo_id):
        """Retorna set de nomes de agentes vivos"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["agentes_vivos"].copy()

    def obter_agentes_mortos(self, grupo_id):
        """Retorna set de nomes de agentes mortos"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["agentes_mortos"].copy()

    def obter_tesouros_coletados(self, grupo_id):
        """Retorna número de tesouros coletados"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["tesouros_coletados"]

    def consultar_celula(self, posicao, grupo_id):
        """
        Consulta informação sobre uma célula.
        Retorna o tipo de célula se já foi visitada, None caso contrário.
        """
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["visitados"].get(posicao)

    def celula_e_segura(self, posicao, grupo_id):
        """Verifica se célula é conhecida como segura"""
        self._garantir_grupo_existe(grupo_id)
        return posicao in self.grupos[grupo_id]["celulas_seguras"]

    def celula_tem_bomba(self, posicao, grupo_id):
        """Verifica se célula é conhecida como tendo bomba"""
        self._garantir_grupo_existe(grupo_id)
        return posicao in self.grupos[grupo_id]["bombas"]

    def celula_foi_explorada(self, posicao, grupo_id):
        """Verifica se célula foi explorada"""
        self._garantir_grupo_existe(grupo_id)
        return posicao in self.grupos[grupo_id]["celulas_exploradas"]

    # =====================================================================
    # ESTATÍSTICAS DO GRUPO
    # =====================================================================

    def obter_mapa_cognitivo(self, grupo_id):
        """
        Retorna mapa cognitivo do grupo.
        Mostra o que o grupo conhece sobre o ambiente.
        """
        self._garantir_grupo_existe(grupo_id)
        grupo = self.grupos[grupo_id]
        
        return {
            "total_explorado": len(grupo["celulas_exploradas"]),
            "total_bombas": len(grupo["bombas"]),
            "total_tesouros_encontrados": len(grupo["tesouros"]),
            "total_tesouros_coletados": grupo["tesouros_coletados"],
            "agentes_vivos": len(grupo["agentes_vivos"]),
            "agentes_mortos": len(grupo["agentes_mortos"]),
            "bandeira_encontrada": grupo["bandeira"] is not None,
            "bandeira_posicao": grupo["bandeira"]
        }

    def obter_historico(self, grupo_id):
        """Retorna histórico de eventos do grupo"""
        self._garantir_grupo_existe(grupo_id)
        return self.grupos[grupo_id]["historico"].copy()

    def limpar_grupo(self, grupo_id):
        """Limpa toda a memória de um grupo"""
        if grupo_id in self.grupos:
            del self.grupos[grupo_id]

    def limpar_tudo(self):
        """Limpa toda a memória"""
        self.grupos.clear()

    # =====================================================================
    # MÉTODOS PARA COMPATIBILIDADE COM CÓDIGO ANTIGO
    # =====================================================================

    def atualizar(self, pos, estado):
        """Compatibilidade com interface antiga"""
        self.registrar_explorada(pos, estado, 0)

    def consultar(self, pos):
        """Compatibilidade com interface antiga"""
        return self.consultar_celula(pos, 0)
