"""
Projeto: Jogo do Moinho (variante 3x3, 3 pecas por jogador)
Autor: <Jose Ameixa n-18881 Diogo Vaz n-21132 Pedro Duarte n-21190>
- Vence quem alinhar 3 pecas na HORIZONTAL ou VERTICAL (diagonais NAO contam).
- O centro ('b2') liga tambem, em diagonal, a todos os cantos.
- Fase 1 (colocacao): ate existirem 3 X e 3 O no tabuleiro.
- Fase 2 (movimento): move-se 1 peca por jogada para uma posicao adjacente livre.
- "Passar" so e permitido quando NAO existem movimentos possiveis.
TADs e funcoes publicas:
- TAD posicao: cria_posicao, cria_copia_posicao, obter_pos_c, obter_pos_l,
  eh_posicao, posicoes_iguais, posicao_para_str, obter_posicoes_adjacentes
- TAD peca: cria_peca, cria_copia_peca, eh_peca, pecas_iguais,
  peca_para_str, peca_para_inteiro
- TAD tabuleiro: cria_tabuleiro, cria_copia_tabuleiro, obter_peca,
  obter_vetor, coloca_peca, remove_peca, move_peca, eh_tabuleiro,
  eh_posicao_livre, tabuleiros_iguais, tabuleiro_para_str,
  tuplo_para_tabuleiro, obter_ganhador, obter_posicoes_livres,
  obter_posicoes_jogador
- Jogo: obter_movimento_manual (I/O), obter_movimento_auto (AI), moinho (principal)
Mensagens obrigatorias:
- Erros:
  'cria_posicao: argumentos invalidos'
  'cria_peca: argumento invalido'
  'obter_movimento_manual: escolha invalida'
  'moinho: argumentos invalidos'
- Arranque:
  'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade <nivel>.'
- Turno do computador:
  'Turno do computador (<nivel>):'
- Notas de IA:
  - Na fase de movimento, usa-se Minimax com filtragem de ramos alpha-beta.
"""
from typing import Literal
from src.constantes import *
from src.posicao import *
from src.peca import *
from src.tabuleiro import *
from src.ai import *


# -------------------------------------------------------------------------------------------------
# (4) TAD movimento (construtores e predicados)
# -------------------------------------------------------------------------------------------------
def cria_mov_colocacao(posicao):
    """Cria um movimento de colocacao: (posicao,)."""
    return (posicao,)

def cria_mov_passar(posicao):
    """Cria um movimento de passagem: (posicao,posicao)."""
    return posicao, posicao

def cria_movimento(pos_origem, pos_destino):
    """Cria um movimento real: (pos_origem,pos_destino)."""
    return pos_origem, pos_destino

def eh_colocacao(movimento):
    """True se o movimento for (posicao,), i.e., colocacao."""
    return len(movimento) == 1

def eh_passar(movimento):
    """True se o movimento for (posicao,posicao), i.e., passar."""
    return len(movimento) == 2 and posicoes_iguais(movimento[0], movimento[1])

def eh_mov_real(movimento):
    """True se o movimento for (pos_origem,pos_destino) com pos_origem != pos_destino."""
    return len(movimento) == 2 and not posicoes_iguais(movimento[0], movimento[1])

# -------------------------------------------------------------------------------------------------
# Funcoes auxiliares (ordem de leitura)
# -------------------------------------------------------------------------------------------------
def _iterador_posicoes_leitura():
    """Iterador de posicoes na ordem de leitura: linhas 1..3; colunas a..c."""
    for l in ROWS:
        for c in COLS:
            yield cria_posicao(c, l)

def obter_posicoes_livres(tabuleiro):
    """Tuplo das posicoes livres (ordem de leitura)."""
    return tuple(pos for pos in _iterador_posicoes_leitura() if eh_posicao_livre(tabuleiro, pos))

def obter_posicoes_jogador(tabuleiro, jogador: str):
    """Tuplo das posicoes ocupadas por jogador (ordem de leitura)."""
    return tuple(pos for pos in _iterador_posicoes_leitura() if obter_peca(tabuleiro, pos) == jogador)

def _contar_pecas(tabuleiro) -> int:
    """Total de pecas no tabuleiro (X+O)."""
    return sum(1 for pos in _iterador_posicoes_leitura() if obter_peca(tabuleiro, pos) != ' ')

def _esta_na_fase_colocacao(tabuleiro) -> bool:
    """True se total de pecas < 6 (fase de colocacao)."""
    return _contar_pecas(tabuleiro) < 6

def _posicoes_adjacentes_livres(tabuleiro, posicao):
    """Tuplo das posicoes adjacentes livres (ordem de leitura)."""
    return tuple(p for p in obter_posicoes_adjacentes(posicao) if eh_posicao_livre(tabuleiro, p))

def _gerar_movimentos_validos(tabuleiro, jogador: str):
    """Gera todas as jogadas (origem, destino) validas por ordem de leitura.
    Se NAO existir movimento real, inclui (posicao,posicao) para a primeira peca do jogador (passar).
    """
    jogadas = []
    for pos in obter_posicoes_jogador(tabuleiro, jogador):
        for adj in _posicoes_adjacentes_livres(tabuleiro, pos):
            jogadas.append((pos, adj))
    if not jogadas:
        pos_jogs = obter_posicoes_jogador(tabuleiro, jogador)
        if pos_jogs:
            jogadas.append((pos_jogs[0], pos_jogs[0]))  # passar
    return tuple(jogadas)
# -----------------------------------------------------------------------------------------------
# (3) Regra de "passar"
# -----------------------------------------------------------------------------------------------
def _verifica_se_pode_passar(tabuleiro, jogador) -> bool:
    """'Passar' so e valido se NAO existir qualquer movimento real possivel para jogador."""
    return not any(not posicoes_iguais(a, b) for (a, b) in _gerar_movimentos_validos(tabuleiro, jogador))

def jogada_valida(tabuleiro, jogador, p_origem, p_destino):
    """Valida uma jogada de movimento para o jogador."""
    if not (eh_posicao(p_origem) and eh_posicao(p_destino)):
        return False
    tem_propria = (obter_peca(tabuleiro, p_origem) == jogador)
    if posicoes_iguais(p_origem, p_destino):
        return tem_propria and _verifica_se_pode_passar(tabuleiro, jogador)
    return tem_propria and p_destino in obter_posicoes_adjacentes(p_origem) and eh_posicao_livre(tabuleiro, p_destino)
# -------------------------------------------------------------------------------------------------
# I/O: obter_movimento_manual
# -------------------------------------------------------------------------------------------------
def obter_movimento_manual(tabuleiro, jogador: str):
    """Le e valida a escolha do jogador humano (colocacao ou movimento)."""
    import sys
    if _esta_na_fase_colocacao(tabuleiro):
        sys.stdout.write('Turno do jogador. Escolha uma posicao: ')
        sys.stdout.flush()
        entrada = sys.stdin.readline().strip()
        try:
            pos = str_para_posicao(entrada)
        except ValueError:
            raise ValueError(ERR_MANUAL)
        if eh_posicao_livre(tabuleiro, pos):
            return (pos,)
        raise ValueError(ERR_MANUAL)
    sys.stdout.write('Turno do jogador. Escolha um movimento: ')
    sys.stdout.flush()
    entrada = sys.stdin.readline().strip()
    try:
        p_origem, p_destino = str_para_movimento(entrada)
    except ValueError:
        raise ValueError(ERR_MANUAL)
    if jogada_valida(tabuleiro, jogador, p_origem, p_destino):
        return p_origem, p_destino
    raise ValueError(ERR_MANUAL)
# -------------------------------------------------------------------------------------------------
# AI: colocacao
# -------------------------------------------------------------------------------------------------
def _alistar_cantos():
    """Tuplo com posicoes de canto (ordem fixa)."""
    return (cria_posicao('a', '1'), cria_posicao('c', '1'),
            cria_posicao('a', '3'), cria_posicao('c', '3'))

def _alistar_laterais():
    """Tuplo com posicoes laterais (nao centro, nao cantos)."""
    return (cria_posicao('b', '1'), cria_posicao('a', '2'),
            cria_posicao('c', '2'), cria_posicao('b', '3'))

def _jogada_vencedora_colocacao(tabuleiro, jogador: str):
    """Devolve posicao livre que da vitoria imediata a jogador, se existir."""
    for pos in obter_posicoes_livres(tabuleiro):
        t2 = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t2, jogador, pos)
        if obter_ganhador(t2) == jogador:
            return pos
    return None

def _jogada_bloqueio_colocacao(tabuleiro, jogador: str):
    """Devolve posicao livre que bloqueia vitoria imediata do adversario, se existir."""
    o = outro_jogador(jogador)
    return _jogada_vencedora_colocacao(tabuleiro, o)

# -------- Heuristica adicional: 2-em-linha (segura) ----------------------------------------------
def _existe_2_em_linha(tabuleiro, jogador: str) -> bool:
    """Retorna True se existir uma linha com exatamente 2 'jogador' e 1 vazia (horizontal/vertical)."""
    o = outro_jogador(jogador)
    for (a, b, c) in WIN_LINES:
        linha = [tabuleiro[a[0]][a[1]], tabuleiro[b[0]][b[1]], tabuleiro[c[0]][c[1]]]
        if linha.count(jogador) == 2 and linha.count(' ') == 1 and linha.count(o) == 0:
            return True
    return False

def _posicao_2_em_linha_segura(tabuleiro, jogador: str):
    """Retorne a primeira posicao livre (ordem de leitura) que cria uma amea?a segura de 2 em linha.
    Seguro = apos a colocacao, o oponente nao tem uma colocacao vencedora imediata.
    Se nao houver nenhuma, retorne Nenhum.
    """
    o = outro_jogador(jogador)
    for pos in obter_posicoes_livres(tabuleiro):
        t2 = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t2, jogador, pos)
        if _existe_2_em_linha(t2, jogador):
            if _jogada_vencedora_colocacao(t2, o) is None:
                return pos
    return None

def _escolher_colocacao_ia(tabuleiro, jogador: str):
    """AI (colocacao): vitoria -> bloqueio -> centro -> 2-em-linha segura -> cantos -> laterais."""
    posicao = _jogada_vencedora_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)
    posicao = _jogada_bloqueio_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)

    # Centro
    b2 = cria_posicao('b', '2')
    if eh_posicao_livre(tabuleiro, b2):
        return (b2,)

    # Heuristica adicional: criar 2-em-linha segura
    posicao = _posicao_2_em_linha_segura(tabuleiro, jogador)
    if posicao:
        return (posicao,)

    # Cantos
    for pos_adjacente in _alistar_cantos():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    # Laterais
    for pos_adjacente in _alistar_laterais():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    livres = obter_posicoes_livres(tabuleiro)
    return (livres[0],) if livres else (cria_posicao('a', '1'),)

# -------------------------------------------------------------------------------------------------
# Funcoes de aplicacao e ciclo do jogo
# -------------------------------------------------------------------------------------------------
def _executar_movimento(tabuleiro, jogador: str, movimento: tuple):
    """Aplica a jogada ao tabuleiro (colocacao, movimento real ou passagem)."""
    if _esta_na_fase_colocacao(tabuleiro):
        coloca_peca(tabuleiro, jogador, movimento[0])
    else:
        if eh_passar(movimento):
            pass
        else:
            move_peca(tabuleiro, movimento[0], movimento[1])
    return tabuleiro

def moinho(jogador: str, nivel: str) -> str:
    """Corre um jogo (humano vs computador) e devolve a peca vencedora ('[X]'/'[O]').
    Raises:
        ValueError: 'moinho: argumentos invalidos' para argumentos invalidos.
    """
    if not (
        isinstance(jogador, str) and jogador in ('[X]', '[O]') and
        isinstance(nivel, str) and nivel in ('facil', 'normal', 'dificil')):
        raise ValueError(ERR_MOINHO)
    humano = 'X' if jogador == '[X]' else 'O'
    cpu = outro_jogador(humano)
    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {nivel}.')
    tabuleiro = cria_tabuleiro()
    print(tabuleiro_para_str(tabuleiro))
    turno = 'X'
    while obter_ganhador(tabuleiro) == ' ':
        if turno == humano:
            movimento = obter_movimento_manual(tabuleiro, humano)
            _executar_movimento(tabuleiro, humano, movimento)
            print(tabuleiro_para_str(tabuleiro))
        else:
            print(f'Turno do computador ({nivel}):')
            movimento = obter_movimento_auto(tabuleiro, cpu, nivel)
            _executar_movimento(tabuleiro, cpu, movimento)
            print(tabuleiro_para_str(tabuleiro))
        turno = outro_jogador(turno)
    return peca_para_str(obter_ganhador(tabuleiro))




# -------------------------------------------------------------------------------------------------
# Minimax (fase de movimento) com filtragem de ramos alpha-beta
# -------------------------------------------------------------------------------------------------
def _algoritmo_minimax(tabuleiro, jogador_atual: str, max_depth: int = 5):
    """Minimax com filtragem de ramos alpha-beta (fase de movimento).
    Contexto:
      - 'X' maximiza o valor; 'O' minimiza.
      - Avaliacao:
          +1 se 'X' tem vitoria;
          -1 se 'O' tem vitoria;
           0 caso contrario (empate/estado intermedio).
    Argumentos:
      tabuleiro     -- TAD tabuleiro em fase de movimento (nao na fase de colocacao);
      jogador_atual -- 'X' ou 'O' (jogador que escolhe no nivel corrente);
      max_depth     -- profundidade maxima de pesquisa (int >= 0);
    Retorna:
      (resultado, melhor_mov)
        resultado      -- int em {-1, 0, +1} (avaliacao do estado para 'X');
        melhor_mov -- (pos_origem, pos_destino) ou None se sem movimentos (ou se depth==0/estado terminal);
        Nota: movimentos (p,p) sinalizam "passar"; nao alteram o tabuleiro na simulacao.
    Notas:
      - A filtragem de ramos alpha-beta ignora ramos que nao podem influenciar a decisao final:
        se um ramo ja e pior do que uma opcao conhecida para  o adversario, e seguro descarta-lo antecipadamente.
      - A ordenacao coloca vitorias imediatas primeiro (melhora a filtragem).
    """
    def avaliacao(tabuleiro_temp: list) -> int:
        """Avaliacao do estado: +1 se 'X' ganhou, -1 se 'O' ganhou, 0 caso contrario."""
        g = obter_ganhador(tabuleiro_temp)
        if g == 'X':
            return 1
        if g == 'O':
            return -1
        return 0

    def outro(j: str) -> str:
        """Devolve o outro jogador: 'X' <-> 'O'."""
        return 'O' if j == 'X' else 'X'

    def ordenar_movimentos(tabuleiro_temp: list, jogador: str, movs: tuple):
        """Prioriza movimentos vencedores imediatos, mantendo determinismo.
        Estrategia:
          - Simula (origem->destino) quando nao for 'passar' (p,p);
          - Se der vitoria imediata para 'jogador', vai para 'ganhos';
          - Caso contrario, vai para 'restantes';
          - Devolve tuple(ganhos + restantes) (estavel e deterministico).
        """
        ganhos, restantes = [], []
        for (pos_origem, pos_destino) in movs:
            t_sim = cria_copia_tabuleiro(tabuleiro_temp)
            if not posicoes_iguais(pos_origem, pos_destino):  # 'passar' nao altera
                move_peca(t_sim, pos_origem, pos_destino)
            if obter_ganhador(t_sim) == jogador:
                ganhos.append((pos_origem, pos_destino))
            else:
                restantes.append((pos_origem, pos_destino))
        return tuple(ganhos + restantes)

    def mm(tabuleiro_temp, jogador: str, depth: int, alpha: int, beta: int):
        """Nucleo recursivo do Minimax com filtragem de ramos alpha-beta.
        Paramentros:
          tabuleiro_temp -- estado corrente (lista 3x3);
          jogador        -- 'X' (maximizador) ou 'O' (minimizador);
          depth          -- profundidade restante;
          alpha, beta    -- limites da filtragem (int).
        Retorna:
            (resultado, melhor_movimento) resultado -- int em {-1,0,+1} melhor_movimento -- (pos_origem, pos_destino) ou None
        Regras:
          - Estado terminal: retorna avaliacao e melhor_movimento=None;
          - Sem movimentos: retorna avaliacao e melhor_movimento=None;
          - Caso geral:
             * Se jogador == 'X': maximiza resultado;
             * Se jogador == 'O': minimiza resultado;
             * Aplica filtragem quando alpha >= beta (corte do ramo).
        """
        ganhador = obter_ganhador(tabuleiro_temp)
        if ganhador != ' ' or depth == 0:
            return avaliacao(tabuleiro_temp), None

        movs = _gerar_movimentos_validos(tabuleiro_temp, jogador)
        if not movs:
            return avaliacao(tabuleiro_temp), None

        movs = ordenar_movimentos(tabuleiro_temp, jogador, movs)

        if jogador == 'X':  # maximiza
            melhor_resultado, melhor_movimento = -10, None
            for (pos_origem, pos_destino) in movs:
                t_sim = cria_copia_tabuleiro(tabuleiro_temp)
                if not posicoes_iguais(pos_origem, pos_destino):  # 'passar' nao altera
                    move_peca(t_sim, pos_origem, pos_destino)
                resultado, _ = mm(t_sim, outro(jogador), depth - 1, alpha, beta)
                if resultado > melhor_resultado:
                    melhor_resultado, melhor_movimento = resultado, (pos_origem, pos_destino)
                if resultado > alpha:
                    alpha = resultado
                if alpha >= beta:  # filtragem de ramos (alpha-beta)
                    break
            return melhor_resultado, melhor_movimento

        else:  # minimiza ('O')
            melhor_resultado, melhor_movimento = 10, None
            for (pos_origem, pos_destino) in movs:
                t_sim = cria_copia_tabuleiro(tabuleiro_temp)
                if not posicoes_iguais(pos_origem, pos_destino):
                    move_peca(t_sim, pos_origem, pos_destino)
                resultado, _ = mm(t_sim, outro(jogador), depth - 1, alpha, beta)

                if resultado < melhor_resultado:
                    melhor_resultado, melhor_movimento = resultado, (pos_origem, pos_destino)
                if resultado < beta:
                    beta = resultado
                if alpha >= beta:  # filtragem de ramos (alpha-beta)
                    break
            return melhor_resultado, melhor_movimento

    return mm(tabuleiro, jogador_atual, max_depth, -10, 10)

# -------------------------------------------------------------------------------------------------
# AI: colocacao
# -------------------------------------------------------------------------------------------------
def _alistar_cantos():
    """Tuplo com posicoes de canto (ordem fixa)."""
    return (cria_posicao('a', '1'), cria_posicao('c', '1'),
            cria_posicao('a', '3'), cria_posicao('c', '3'))

def _alistar_laterais():
    """Tuplo com posicoes laterais (nao centro, nao cantos)."""
    return (cria_posicao('b', '1'), cria_posicao('a', '2'),
            cria_posicao('c', '2'), cria_posicao('b', '3'))

def _jogada_vencedora_colocacao(tabuleiro, jogador: str):
    """Devolve posicao livre que da vitoria imediata a jogador, se existir."""
    for pos in obter_posicoes_livres(tabuleiro):
        t2 = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t2, jogador, pos)
        if obter_ganhador(t2) == jogador:
            return pos
    return None

def _jogada_bloqueio_colocacao(tabuleiro, jogador: str):
    """Devolve posicao livre que bloqueia vitoria imediata do adversario, se existir."""
    o = outro_jogador(jogador)
    return _jogada_vencedora_colocacao(tabuleiro, o)

# -------- Heuristica adicional: 2-em-linha (segura) ----------------------------------------------
def _existe_2_em_linha(tabuleiro, jogador: str) -> bool:
    """Retorna True se existir uma linha com exatamente 2 'jogador' e 1 vazia (horizontal/vertical)."""
    o = outro_jogador(jogador)
    for (a, b, c) in WIN_LINES:
        linha = [tabuleiro[a[0]][a[1]], tabuleiro[b[0]][b[1]], tabuleiro[c[0]][c[1]]]
        if linha.count(jogador) == 2 and linha.count(' ') == 1 and linha.count(o) == 0:
            return True
    return False

def _posicao_2_em_linha_segura(tabuleiro, jogador: str):
    """Retorne a primeira posicao livre (ordem de leitura) que cria uma amea?a segura de 2 em linha.
    Seguro = apos a colocacao, o oponente nao tem uma colocacao vencedora imediata.
    Se nao houver nenhuma, retorne Nenhum.
    """
    o = outro_jogador(jogador)
    for pos in obter_posicoes_livres(tabuleiro):
        t2 = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t2, jogador, pos)
        if _existe_2_em_linha(t2, jogador):
            if _jogada_vencedora_colocacao(t2, o) is None:
                return pos
    return None

def _escolher_colocacao_ia(tabuleiro, jogador: str):
    """AI (colocacao): vitoria -> bloqueio -> centro -> 2-em-linha segura -> cantos -> laterais."""
    posicao = _jogada_vencedora_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)
    posicao = _jogada_bloqueio_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)

    # Centro
    b2 = cria_posicao('b', '2')
    if eh_posicao_livre(tabuleiro, b2):
        return (b2,)

    # Heuristica adicional: criar 2-em-linha segura
    posicao = _posicao_2_em_linha_segura(tabuleiro, jogador)
    if posicao:
        return (posicao,)

    # Cantos
    for pos_adjacente in _alistar_cantos():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    # Laterais
    for pos_adjacente in _alistar_laterais():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    livres = obter_posicoes_livres(tabuleiro)
    return (livres[0],) if livres else (cria_posicao('a', '1'),)
# -------------------------------------------------------------------------------------------------
# AI: movimento (facil/normal/dificil)
# -------------------------------------------------------------------------------------------------
def _escolher_primeiro_movimento(tabuleiro, jogador: str):
    """Nivel 'facil': primeiro movimento valido; se nenhum, (posicao,posicao)."""
    for pos in obter_posicoes_jogador(tabuleiro, jogador):
        for adj in obter_posicoes_adjacentes(pos):
            if eh_posicao_livre(tabuleiro, adj):
                return pos, adj
    pos_jogs = obter_posicoes_jogador(tabuleiro, jogador)
    return (pos_jogs[0], pos_jogs[0]) if pos_jogs else (cria_posicao('a', '1'), cria_posicao('a', '1'))

def _jogada_vencedora_movimento(tabuleiro, jogador: str):
    """Procura (origem,destino) que vence imediatamente."""
    for (pos_origem, pos_destino) in _gerar_movimentos_validos(tabuleiro, jogador):
        if posicoes_iguais(pos_origem, pos_destino):
            continue
        t2 = cria_copia_tabuleiro(tabuleiro)
        move_peca(t2, pos_origem, pos_destino)
        if obter_ganhador(t2) == jogador:
            return pos_origem, pos_destino
    return None

def obter_movimento_auto(tabuleiro, jogador: str, nivel: str):
    """Escolha automatica de jogada (colocacao ou movimento) para o nivel dado."""
    if _esta_na_fase_colocacao(tabuleiro):
        return _escolher_colocacao_ia(tabuleiro, jogador)
    if nivel == 'facil':
        return _escolher_primeiro_movimento(tabuleiro, jogador)
    if nivel == 'normal':
        mov = _jogada_vencedora_movimento(tabuleiro, jogador)
        return mov if mov else _escolher_primeiro_movimento(tabuleiro, jogador)
    if nivel == 'dificil':
        _, mov = _algoritmo_minimax(tabuleiro, jogador, max_depth=5)
        return mov if mov else _escolher_primeiro_movimento(tabuleiro, jogador)
    raise ValueError("obter_movimento_auto: nivel invalido")


def cria_tabuleiro():
    """Construtor do TAD tabuleiro (3x3) vazio."""
    return [[cria_peca(' ') for _ in COLS] for _ in ROWS]

def cria_copia_tabuleiro(tabuleiro):
    """Copia profunda (por linhas) do tabuleiro."""
    return [linha[:] for linha in tabuleiro]

def eh_posicao_livre(tabuleiro, posicao) -> bool:
    """Teste: True se a posicao no tabuleiro estiver livre."""
    return obter_peca(tabuleiro, posicao) == ' '

def tabuleiros_iguais(t1, tabuleiro_copia) -> bool:
    """Teste: True se t1 e tabuleiro_copia forem iguais (todas as casas)."""
    return all(t1[r][c] == tabuleiro_copia[r][c] for r in range(3) for c in range(3))

def tabuleiro_para_str(tabuleiro) -> str:
    """Transformador: devolve a representacao ASCII do tabuleiro no formato do enunciado."""
    def linha_str(i: int) -> str:
        return f"{ROWS[i]} " + "-".join(peca_para_str(tabuleiro[i][j]) for j in range(3))
    return "\n".join([HEADER, linha_str(0), CONN1, linha_str(1), CONN2, linha_str(2)])

def tuplo_para_tabuleiro(tp) -> list[list[str]]:
    """Construtor a partir de tuplo 3x3 de inteiros {-1,0,1}."""
    # --- Validacoes m?nimas ---
    if not (isinstance(tp, tuple) and len(tp) == 3 and all(isinstance(l, tuple) and len(l) == 3 for l in tp)):
        raise ValueError("tuplo_para_tabuleiro: argumento deve ser um tuplo 3x3")
    valores_validos = {1, 0, -1}
    for r in range(3):
        for c in range(3):
            if tp[r][c] not in valores_validos:
                raise ValueError("tuplo_para_tabuleiro: valores inv?lidos (usar 1, 0, -1)")

    tabuleiro = cria_tabuleiro()
    for r in range(3):
        for c in range(3):
            val = tp[r][c]
            if val == 1:
                jogador: Literal['X', 'O', ' '] = 'X'
            elif val == -1:
                jogador = 'O'
            else:
                jogador = ' '
            tabuleiro[r][c] = jogador
    return tabuleiro






def obter_vetor(tabuleiro, entrada: str) -> tuple[str, str, str]:
    """Seletor: devolve a linha ou a coluna do tabuleiro como tuplo de 3 pecas."""
    if entrada in COLS:
        c = COLS.index(entrada)
        return tuple(tabuleiro[r][c] for r in range(3))
    elif entrada in ROWS:
        r = ROWS.index(entrada)
        return tuple(tabuleiro[r][c] for c in range(3))
    else:
        raise ValueError("obter_vetor: seletor invalido (use 'a'..'c' ou '1'..'3')")

def _tem_vencedor(tabuleiro, jogador: str) -> bool:
    """Teste interno: True se jogador tiver uma linha completa (horizontal/vertical)."""
    for (a, b, c) in WIN_LINES:
        if tabuleiro[a[0]][a[1]] == jogador and tabuleiro[b[0]][b[1]] == jogador and tabuleiro[c[0]][c[1]] == jogador:
            return True
    return False

def obter_ganhador(tabuleiro) -> str:
    """Devolve 'X'/'O' ou ' ' se ainda nao ha vencedor."""
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '

