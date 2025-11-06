from typing import Tuple, List, Optional
# -------------------------------------------------------------------------------------------------
# Constantes e mensagens
# -------------------------------------------------------------------------------------------------
cols = ('a', 'b', 'c')
rows = ('1', '2', '3')
err_pos = 'cria_posicao: argumentos invalidos'
err_piece = 'cria_peca: argumento invalido'
err_manual = 'obter_movimento_manual: escolha invalida'
err_moinho = 'moinho: argumentos invalidos'
# ASCII do tabuleiro
header = '   a   b   c'
conn1 = '   | \\ | / |'
conn2 = '   | / | \\ |'
# Linhas vencedoras (horizontais e verticais)
win_lines = (
    ((0,0), (0,1), (0,2)),
    ((1,0), (1,1), (1,2)),
    ((2,0), (2,1), (2,2)),
    ((0,0), (1,0), (2,0)),
    ((0,1), (1,1), (2,1)),
    ((0,2), (1,2), (2,2)),
)
inf = 10  # Constante para valores iniciais de alpha/beta no Minimax
# -------------------------------------------------------------------------------------------------
# Utilitarios de validacao
# -------------------------------------------------------------------------------------------------
def _validar_posicao(c: str, l: str) -> None:
    if not isinstance(c, str) or not isinstance(l, str):
        raise ValueError(err_pos)
    if c not in cols or l not in rows:
        raise ValueError(err_pos)

def _validar_peca(entrada: str) -> None:
    if not (isinstance(entrada, str) and len(entrada) == 1 and entrada in ('X', 'O', ' ')):
        raise ValueError(err_piece)

def _obter_adversario(jogador: str) -> str:
    return 'O' if jogador == 'X' else 'X'

# -------------------------------------------------------------------------------------------------
# TAD posicao
# -------------------------------------------------------------------------------------------------
def cria_posicao(c: str, l: str) -> Tuple[str, str]:
    _validar_posicao(c, l)
    return c, l

def cria_copia_posicao(posicao: Tuple[str, str]) -> Tuple[str, str]:
    return posicao[0], posicao[1]

def obter_pos_c(posicao: Tuple[str, str]) -> str:
    return posicao[0]

def obter_pos_l(posicao: Tuple[str, str]) -> str:
    return posicao[1]

def eh_posicao(arg) -> bool:
    return (
        isinstance(arg, tuple) and
        len(arg) == 2 and
        arg[0] in cols and
        arg[1] in rows
    )

def posicoes_iguais(p1, p2) -> bool:
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(posicao: Tuple[str, str]) -> str:
    return posicao[0] + posicao[1]

def str_para_posicao(entrada: str):
    if len(entrada) == 2 and entrada[0] in cols and entrada[1] in rows:
        return cria_posicao(entrada[0], entrada[1])
    raise ValueError(err_manual)

def str_para_movimento(entrada: str):
    if len(entrada) == 4 and entrada[0] in cols and entrada[1] in rows and entrada[2] in cols and entrada[3] in rows:
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(err_manual)

def cria_mov_colocacao(posicao):
    return (posicao,)

def eh_colocacao(movimento):
    return len(movimento) == 1

def cria_mov_passar(posicao):
    return posicao, posicao

def eh_passar(movimento):
    return len(movimento) == 2 and posicoes_iguais(movimento[0], movimento[1])

def cria_movimento(pos_origem, pos_destino):
    return pos_origem, pos_destino

def eh_mov_real(movimento):
    return len(movimento) == 2 and not posicoes_iguais(movimento[0], movimento[1])

_adj = {
    'a1': ('b1', 'a2', 'b2'),
    'b1': ('b2', 'a1', 'c1'),
    'c1': ('b1', 'c2', 'b2'),
    'a2': ('a1', 'a3', 'b2'),
    'b2': ('a2', 'b1', 'c2', 'b3', 'a1', 'c1', 'a3', 'c3'),
    'c2': ('c1', 'c3', 'b2'),
    'a3': ('a2', 'b3', 'b2'),
    'b3': ('b2', 'a3', 'c3'),
    'c3': ('c2', 'b3', 'b2')
}
def obter_posicoes_adjacentes(posicao: Tuple[str, str]) -> Tuple[Tuple[str, str], ...]:
    if not eh_posicao(posicao):
        raise ValueError('obter_posicoes_adjacentes: posicao invalida')
    key = posicao_para_str(posicao)
    return tuple(cria_posicao(p[0], p[1]) for p in _adj[key])

# -------------------------------------------------------------------------------------------------
# TAD peca
# -------------------------------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    _validar_peca(entrada)
    return entrada

def cria_copia_peca(jogador: str) -> str:
    return jogador

def eh_peca(arg) -> bool:
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(peca1: str, peca2: str) -> bool:
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2

def peca_para_str(jogador: str) -> str:
    return f'[{jogador}]'

def peca_para_inteiro(jogador: str) -> int:
    return 1 if jogador == 'X' else (-1 if jogador == 'O' else 0)

# -------------------------------------------------------------------------------------------------
# TAD tabuleiro
# -------------------------------------------------------------------------------------------------
def cria_tabuleiro() -> List[List[str]]:
    return [[cria_peca(' ') for _ in cols] for _ in rows]

def cria_copia_tabuleiro(tabuleiro: List[List[str]]) -> List[List[str]]:
    return [linha[:] for linha in tabuleiro]

def _idx_from_pos(posicao: Tuple[str, str]) -> Tuple[int, int]:
    return rows.index(obter_pos_l(posicao)), cols.index(obter_pos_c(posicao))

def obter_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> str:
    r, c = _idx_from_pos(posicao)
    return tabuleiro[r][c]

def obter_vetor(tabuleiro: List[List[str]], entrada: str) -> Tuple[str, str, str]:
    if entrada in cols:
        c = cols.index(entrada)
        return tabuleiro[0][c], tabuleiro[1][c], tabuleiro[2][c]
    elif entrada in rows:
        r = rows.index(entrada)
        return tabuleiro[r][0], tabuleiro[r][1], tabuleiro[r][2]
    else:
        raise ValueError("obter_vetor: seletor invalido (use 'a'..'c' ou '1'..'3')")

def coloca_peca(tabuleiro: List[List[str]], jogador: str, posicao: Tuple[str, str]) -> List[List[str]]:
    if not eh_peca(jogador) or jogador == ' ':
        raise ValueError("coloca_peca: peca invalida")
    if not eh_posicao(posicao):
        raise ValueError("coloca_peca: posicao invalida")
    if obter_peca(tabuleiro, posicao) != ' ':
        raise ValueError("coloca_peca: posicao ocupada")
    r, c = _idx_from_pos(posicao)
    tabuleiro[r][c] = jogador
    return tabuleiro

def remove_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> List[List[str]]:
    r, c = _idx_from_pos(posicao)
    tabuleiro[r][c] = ' '
    return tabuleiro

def move_peca(tabuleiro: List[List[str]], p_origem: Tuple[str, str], p_destino: Tuple[str, str]) -> List[List[str]]:
    if not (eh_posicao(p_origem) and eh_posicao(p_destino)):
        raise ValueError("move_peca: posicao invalida")
    if obter_peca(tabuleiro, p_origem) == ' ':
        raise ValueError("move_peca: origem vazia")
    if obter_peca(tabuleiro, p_destino) != ' ':
        raise ValueError("move_peca: destino ocupado")
    if p_destino not in obter_posicoes_adjacentes(p_origem):
        raise ValueError("move_peca: destino nao adjacente")
    jogador = obter_peca(tabuleiro, p_origem)
    remove_peca(tabuleiro, p_origem)
    coloca_peca(tabuleiro, jogador, p_destino)
    return tabuleiro

def _tem_vencedor(tabuleiro: List[List[str]], jogador: str) -> bool:
    for line in win_lines:
        if all(obter_peca(tabuleiro, cria_posicao(cols[c], rows[r])) == jogador for r, c in line):
            return True
    return False

def eh_tabuleiro(arg) -> bool:
    if not (isinstance(arg, list) and len(arg) == 3 and all(isinstance(row, list) and len(row) == 3 for row in arg)):
        return False
    pieces = [p for row in arg for p in row]
    if not all(eh_peca(p) for p in pieces):
        return False
    count_x = pieces.count('X')
    count_o = pieces.count('O')
    if count_x > 3 or count_o > 3:
        return False
    if abs(count_x - count_o) > 1:
        return False
    winner_x = _tem_vencedor(arg, 'X')
    winner_o = _tem_vencedor(arg, 'O')
    if winner_x and winner_o:
        return False
    return True

def eh_posicao_livre(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> bool:
    return obter_peca(tabuleiro, posicao) == ' '

def tabuleiros_iguais(t1: List[List[str]], t2: List[List[str]]) -> bool:
    return all(obter_peca(t1, pos) == obter_peca(t2, pos) for pos in _iterador_posicoes_leitura())

def tabuleiro_para_str(tabuleiro: List[List[str]]) -> str:
    def linha_str(i: int) -> str:
        return f"{rows[i]} " + "-".join(peca_para_str(obter_peca(tabuleiro, cria_posicao(c, rows[i]))) for c in cols)
    return "\n".join([header, linha_str(0), conn1, linha_str(1), conn2, linha_str(2)])

def tuplo_para_tabuleiro(tp: Tuple[Tuple[int, int, int], ...]) -> List[List[str]]:
    if not (isinstance(tp, tuple) and len(tp) == 3 and all(isinstance(l, tuple) and len(l) == 3 for l in tp)):
        raise ValueError("tuplo_para_tabuleiro: argumento deve ser um tuplo 3x3")
    valores_validos = {1, 0, -1}
    if any(tp[r][c] not in valores_validos for r in range(3) for c in range(3)):
        raise ValueError("tuplo_para_tabuleiro: valores invalidos (usar 1, 0, -1)")
    tabuleiro = cria_tabuleiro()
    for r in range(3):
        for c in range(3):
            val = tp[r][c]
            if val != 0:
                jogador = 'X' if val == 1 else 'O'
                coloca_peca(tabuleiro, jogador, cria_posicao(cols[c], rows[r]))
    return tabuleiro

def obter_ganhador(tabuleiro: List[List[str]]) -> str:
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '

# -------------------------------------------------------------------------------------------------
# Funcoes auxiliares (ordem de leitura)
# -------------------------------------------------------------------------------------------------
def _iterador_posicoes_leitura():
    for l in rows:
        for c in cols:
            yield cria_posicao(c, l)

def obter_posicoes_livres(tabuleiro: List[List[str]]) -> Tuple[Tuple[str, str], ...]:
    return tuple(pos for pos in _iterador_posicoes_leitura() if eh_posicao_livre(tabuleiro, pos))

def obter_posicoes_jogador(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    return tuple(pos for pos in _iterador_posicoes_leitura() if obter_peca(tabuleiro, pos) == jogador)

def _esta_na_fase_colocacao(tabuleiro: List[List[str]]) -> bool:
    return len(obter_posicoes_jogador(tabuleiro, 'X')) < 3 or len(obter_posicoes_jogador(tabuleiro, 'O')) < 3

def _obter_movimentos_validos(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]:
    movimentos = []
    pos_jogs = obter_posicoes_jogador(tabuleiro, jogador)
    tem_movimentos = False
    for pos in pos_jogs:
        for adj in obter_posicoes_adjacentes(pos):
            if eh_posicao_livre(tabuleiro, adj):
                movimentos.append(cria_movimento(pos, adj))
                tem_movimentos = True
    if not tem_movimentos and pos_jogs:
        movimentos.append(cria_mov_passar(pos_jogs[0]))
    return tuple(movimentos)

def _verifica_se_pode_passar(tabuleiro: List[List[str]], jogador: str) -> bool:
    for pos in obter_posicoes_jogador(tabuleiro, jogador):
        for adj in obter_posicoes_adjacentes(pos):
            if eh_posicao_livre(tabuleiro, adj):
                return False
    return True

def jogada_valida(tabuleiro: List[List[str]], jogador: str, p_origem: Tuple[str, str], p_destino: Tuple[str, str]) -> bool:
    if not (eh_posicao(p_origem) and eh_posicao(p_destino)):
        return False
    tem_propria = (obter_peca(tabuleiro, p_origem) == jogador)
    if posicoes_iguais(p_origem, p_destino):
        return tem_propria and _verifica_se_pode_passar(tabuleiro, jogador)
    return tem_propria and eh_posicao_livre(tabuleiro, p_destino) and p_destino in obter_posicoes_adjacentes(p_origem)

# -------------------------------------------------------------------------------------------------
# I/O: obter_movimento_manual
# -------------------------------------------------------------------------------------------------
def obter_movimento_manual(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    import sys
    if _esta_na_fase_colocacao(tabuleiro):
        print('Turno do jogador. Escolha uma posicao: ', end='')
        entrada = sys.stdin.readline().strip()
        pos = str_para_posicao(entrada)
        if eh_posicao_livre(tabuleiro, pos):
            return cria_mov_colocacao(pos)
        raise ValueError(err_manual)
    print('Turno do jogador. Escolha um movimento: ', end='')
    entrada = sys.stdin.readline().strip()
    p_origem, p_destino = str_para_movimento(entrada)
    if jogada_valida(tabuleiro, jogador, p_origem, p_destino):
        return cria_movimento(p_origem, p_destino) if not posicoes_iguais(p_origem, p_destino) else cria_mov_passar(p_origem)
    raise ValueError(err_manual)

# -------------------------------------------------------------------------------------------------
# AI: colocacao
# -------------------------------------------------------------------------------------------------
def _obter_posicoes_de_canto() -> Tuple[Tuple[str, str], ...]:
    return cria_posicao('a', '1'), cria_posicao('c', '1'), cria_posicao('a', '3'), cria_posicao('c', '3')

def _obter_posicoes_laterais() -> Tuple[Tuple[str, str], ...]:
    return cria_posicao('b', '1'), cria_posicao('a', '2'), cria_posicao('c', '2'), cria_posicao('b', '3')

def _posicao_vencedora_para_colocacao(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    for pos in obter_posicoes_livres(tabuleiro):
        t_copy = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t_copy, jogador, pos)
        if obter_ganhador(t_copy) == jogador:
            return pos
    return None

def _posicao_de_bloqueio_para_colocacao(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    return _posicao_vencedora_para_colocacao(tabuleiro, _obter_adversario(jogador))

def _ha_dois_em_linha(tabuleiro: List[List[str]], jogador: str) -> bool:
    o = _obter_adversario(jogador)
    for line in win_lines:
        pecas = [obter_peca(tabuleiro, cria_posicao(cols[c], rows[r])) for r, c in line]
        if pecas.count(jogador) == 2 and pecas.count(' ') == 1 and pecas.count(o) == 0:
            return True
    return False

def _posicao_dois_em_linha_segura(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    o = _obter_adversario(jogador)
    for pos in obter_posicoes_livres(tabuleiro):
        t_copy = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t_copy, jogador, pos)
        if _ha_dois_em_linha(t_copy, jogador) and _posicao_vencedora_para_colocacao(t_copy, o) is None:
            return pos
    return None

def _escolher_colocacao_ia(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    pos = _posicao_vencedora_para_colocacao(tabuleiro, jogador)
    if pos:
        return cria_mov_colocacao(pos)
    pos = _posicao_de_bloqueio_para_colocacao(tabuleiro, jogador)
    if pos:
        return cria_mov_colocacao(pos)
    b2 = cria_posicao('b', '2')
    if eh_posicao_livre(tabuleiro, b2):
        return cria_mov_colocacao(b2)
    pos = _posicao_dois_em_linha_segura(tabuleiro, jogador)
    if pos:
        return cria_mov_colocacao(pos)
    for pos in _obter_posicoes_de_canto():
        if eh_posicao_livre(tabuleiro, pos):
            return cria_mov_colocacao(pos)
    for pos in _obter_posicoes_laterais():
        if eh_posicao_livre(tabuleiro, pos):
            return cria_mov_colocacao(pos)
    livres = obter_posicoes_livres(tabuleiro)
    return cria_mov_colocacao(livres[0]) if livres else cria_mov_colocacao(cria_posicao('a', '1'))

# -------------------------------------------------------------------------------------------------
# AI: movimento (facil/normal/dificil)
# -------------------------------------------------------------------------------------------------
def _primeiro_movimento_disponivel(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    pos_jogs = obter_posicoes_jogador(tabuleiro, jogador)
    for pos in pos_jogs:
        for adj in obter_posicoes_adjacentes(pos):
            if eh_posicao_livre(tabuleiro, adj):
                return cria_movimento(pos, adj)
    return cria_mov_passar(pos_jogs[0]) if pos_jogs else cria_mov_passar(cria_posicao('a', '1'))

def _jogada_vencedora_movimento(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[Tuple[str, str], ...]]:
    for mov in _obter_movimentos_validos(tabuleiro, jogador):
        if eh_passar(mov):
            continue
        t_copy = cria_copia_tabuleiro(tabuleiro)
        move_peca(t_copy, mov[0], mov[1])
        if obter_ganhador(t_copy) == jogador:
            return mov
    return None

def obter_movimento_auto(tabuleiro: List[List[str]], jogador: str, nivel: str) -> Tuple[Tuple[str, str], ...]:
    if _esta_na_fase_colocacao(tabuleiro):
        return _escolher_colocacao_ia(tabuleiro, jogador)
    if nivel == 'facil':
        return _primeiro_movimento_disponivel(tabuleiro, jogador)
    if nivel == 'normal':
        mov = _jogada_vencedora_movimento(tabuleiro, jogador)
        return mov if mov else _primeiro_movimento_disponivel(tabuleiro, jogador)
    if nivel == 'dificil':
        _, mov = _algoritmo_minimax(tabuleiro, jogador)
        return mov if mov else _primeiro_movimento_disponivel(tabuleiro, jogador)
    raise ValueError("obter_movimento_auto: nivel invalido")

# -------------------------------------------------------------------------------------------------
# Minimax (fase de movimento) com filtragem de ramos alpha-beta
# -------------------------------------------------------------------------------------------------
def _avaliacao(tabuleiro: List[List[str]]) -> int:
    g = obter_ganhador(tabuleiro)
    return 1 if g == 'X' else (-1 if g == 'O' else 0)

def _ordenar_movimentos(tabuleiro: List[List[str]], jogador: str, movs: Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]) -> Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]:
    ganhos, restantes = [], []
    for mov in movs:
        t_sim = cria_copia_tabuleiro(tabuleiro)
        if eh_mov_real(mov):
            move_peca(t_sim, mov[0], mov[1])
        if obter_ganhador(t_sim) == jogador:
            ganhos.append(mov)
        else:
            restantes.append(mov)
    return tuple(ganhos + restantes)


def _minimax_generico(tabuleiro, jogador, depth, alpha, beta, movs, melhor_val_inicial, comparar, atualizar_limite):
    melhor_val, melhor_mov = melhor_val_inicial, None

    for mov in movs:
        t_sim = cria_copia_tabuleiro(tabuleiro)
        if eh_mov_real(mov):
            move_peca(t_sim, mov[0], mov[1])# TODO
        val, _ = _minimax_recursivo(t_sim, _obter_adversario(jogador), depth -1, alpha, beta)

        if comparar(val, melhor_val):
            melhor_val, melhor_mov = val, mov
        
        alpha, beta = atualizar_limite(alpha, beta, val)

        if alpha >= beta:
            break
    return melhor_val, melhor_mov



def _minimax_recursivo(tabuleiro: List[List[str]], jogador: str, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Tuple[Tuple[str, str], Tuple[str, str]]]]:
    if obter_ganhador(tabuleiro) != ' ' or depth == 0:
        return _avaliacao(tabuleiro), None
    movs = _obter_movimentos_validos(tabuleiro, jogador)
    if not movs:
        return _avaliacao(tabuleiro), None
    movs = _ordenar_movimentos(tabuleiro, jogador, movs)

    if jogador == 'X':  # maximiza
        return _minimax_generico(
            tabuleiro, jogador, depth, alpha, beta, movs, inf,  
            lambda val, melhor_val: val > melhor_val,
            lambda alpha, beta, val: (max(alpha, val), beta)
        )
    
    else:  # minimiza
        return _minimax_generico(
            tabuleiro, jogador, depth, alpha, beta, movs, inf,
            lambda val, melhor_val: val < melhor_val,
            lambda alpha, beta, val: (alpha, min(val, beta))
        )

def _algoritmo_minimax(tabuleiro: List[List[str]], jogador: str, max_depth: int = 5) -> Tuple[int, Optional[Tuple[Tuple[str, str], Tuple[str, str]]]]:
    return _minimax_recursivo(tabuleiro, jogador, max_depth, -inf, inf)

# -------------------------------------------------------------------------------------------------
# Funcoes de aplicacao e ciclo do jogo
# -------------------------------------------------------------------------------------------------
def _aplicar_movimento_no_tabuleiro(tabuleiro: List[List[str]], jogador: str, movimento: Tuple[Tuple[str, str], ...]) -> List[List[str]]:
    if eh_colocacao(movimento):
        coloca_peca(tabuleiro, jogador, movimento[0])
    elif eh_mov_real(movimento):
        move_peca(tabuleiro, movimento[0], movimento[1])
    return tabuleiro

def moinho(jogador_str: str, nivel: str) -> str:
    if not (jogador_str in ('[X]', '[O]') and nivel in ('facil', 'normal', 'dificil')):
        raise ValueError(err_moinho)
    humano = 'X' if jogador_str == '[X]' else 'O'
    cpu = _obter_adversario(humano)
    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {nivel}.')
    tabuleiro = cria_tabuleiro()
    print(tabuleiro_para_str(tabuleiro))
    turno = 'X'
    while obter_ganhador(tabuleiro) == ' ':
        if turno == humano:
            movimento = obter_movimento_manual(tabuleiro, humano)
            _aplicar_movimento_no_tabuleiro(tabuleiro, humano, movimento)
        else:
            print(f'Turno do computador ({nivel}):')
            movimento = obter_movimento_auto(tabuleiro, cpu, nivel)
            _aplicar_movimento_no_tabuleiro(tabuleiro, cpu, movimento)
        print(tabuleiro_para_str(tabuleiro))
        turno = _obter_adversario(turno)
    return peca_para_str(obter_ganhador(tabuleiro))