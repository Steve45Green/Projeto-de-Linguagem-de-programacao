# -*- coding: ascii -*-
"""
Projeto: Jogo do Moinho (variante 3x3, 3 pecas por jogador)
Autor: <Jose Ameixa n-18881>
Descricao (ASCII):
 - Vence quem alinhar 3 pecas na HORIZONTAL ou VERTICAL (diagonais NAO contam).
 - Centro ('b2') tem ligacoes tambem diagonais aos quatro cantos.
 - Fase 1: Colocacao (ate ter 3 X e 3 O no tabuleiro).
 - Fase 2: Movimento (move-se 1 peca propria por jogada para adjacente livre).
 - "Passar" so e permitido quando NAO existem movimentos possiveis (todas as pecas do jogador estao bloqueadas).

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
- Jogo: obter_movimento_manual (I/O), obter_movimento_auto (IA), moinho (principal)

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
"""

# -----------------------------------------------------------------------------
# Constantes
# -----------------------------------------------------------------------------
COLS = ('a', 'b', 'c')
ROWS = ('1', '2', '3')

ERR_POS = 'cria_posicao: argumentos invalidos'
ERR_PIECE = 'cria_peca: argumento invalido'
ERR_MANUAL = 'obter_movimento_manual: escolha invalida'
ERR_MOINHO = 'moinho: argumentos invalidos'

# ---------------- Desenho do tabuleiro (ASCII) ----------------

HEADER = '   a   b   c'
CONN1  = '   | \\ | / |'
CONN2  = '   | / | \\ |'

# Linhas vencedoras (horizontais e verticais) em indices (linha,coluna)
WIN_LINES = (
    ((0,0), (0,1), (0,2)),
    ((1,0), (1,1), (1,2)),
    ((2,0), (2,1), (2,2)),
    ((0,0), (1,0), (2,0)),
    ((0,1), (1,1), (2,1)),
    ((0,2), (1,2), (2,2)),
)

# -----------------------------------------------------------------------------
# TAD posicao
# -----------------------------------------------------------------------------
def cria_posicao(c, l):
    """Construtor: recebe c em {'a','b','c'} e l em {'1','2','3'}."""
    if not isinstance(c, str) or not isinstance(l, str):
        raise ValueError(ERR_POS)
    if c not in COLS or l not in ROWS:
        raise ValueError(ERR_POS)
    return c, l

def cria_copia_posicao(p):
    """Devolve copia da posicao p."""
    return p[0], p[1]

def obter_pos_c(p):
    """Seletor: devolve a coluna da posicao p."""
    return p[0]

def obter_pos_l(p):
    """Seletor: devolve a linha da posicao p."""
    return p[1]

def _e_col(c): return isinstance(c, str) and len(c) == 1 and c in COLS
def _e_lin(l): return isinstance(l, str) and len(l) == 1 and l in ROWS
def _e_pos(c, l): return _e_col(c) and _e_lin(l)

def eh_posicao(arg):
    """Reconhecedor: True se arg e um TAD posicao valido."""
    return isinstance(arg, tuple) and len(arg) == 2 and _e_pos(arg[0], arg[1])

def posicoes_iguais(p1, p2):
    """Teste: True se p1 e p2 sao posicoes iguais."""
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(p):
    """Transformador: devolve 'cl' (ex.: 'a1') da posicao p."""
    return obter_pos_c(p) + obter_pos_l(p)

# Adjacencias (ordem de leitura do tabuleiro)
# Nota: alem das ligacoes ortogonais, o centro 'b2' liga-se tambem em diagonal aos
# quatro cantos, conforme especificacao do enunciado desta variante 3x3.
_ADJ = {
    'a1': ('b1', 'a2', 'b2'),
    'b1': ('b2', 'a1', 'c1'),
    'c1': ('b2', 'b1', 'c2'),
    'a2': ('a1', 'a3', 'b2'),
    'b2': ('b1', 'a2', 'c2', 'a1', 'c1', 'a3', 'c3', 'b3'),
    'c2': ('b2', 'c1', 'c3'),
    'a3': ('a2', 'b3', 'b2'),
    'b3': ('b2', 'a3', 'c3'),
    'c3': ('b3', 'c2', 'b2'),
}

def obter_posicoes_adjacentes(p):
    """Alto nivel: tuplo com as posicoes adjacentes a p (ordem de leitura)."""
    if not eh_posicao(p):
        raise ValueError('obter_posicoes_adjacentes: posicao invalida')
    key = posicao_para_str(p)
    # Mantem determinismo: filtra por ordem de leitura sem sets na saida
    viz = set(_ADJ[key])
    return tuple(pp for pp in _iter_pos_em_leitura() if posicao_para_str(pp) in viz)

# -----------------------------------------------------------------------------
# TAD peca
# -----------------------------------------------------------------------------
def cria_peca(s):
    """Construtor: 'X', 'O' ou ' ' (livre)."""
    if not (isinstance(s, str) and len(s) == 1 and s in ('X', 'O', ' ')):
        raise ValueError(ERR_PIECE)
    return s

def cria_copia_peca(j):
    """Devolve copia da peca j."""
    return j

def eh_peca(arg):
    """Reconhecedor: True se arg e 'X', 'O' ou ' '."""
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(j1, j2):
    """Teste: True se j1 e j2 sao pecas iguais."""
    return eh_peca(j1) and eh_peca(j2) and j1 == j2

def peca_para_str(j):
    """Transformador: devolve '[X]', '[O]' ou '[ ]'."""
    return '[' + j + ']'

def peca_para_inteiro(j):
    """Alto nivel: X->1, O->-1, ' '->0."""
    return 1 if j == 'X' else (-1 if j == 'O' else 0)

# -----------------------------------------------------------------------------
# TAD tabuleiro
# -----------------------------------------------------------------------------
def cria_tabuleiro():
    """Construtor: devolve tabuleiro 3x3 vazio (' ')."""
    return [[cria_peca(' ') for _ in COLS] for _ in ROWS]

def cria_copia_tabuleiro(t):
    """Devolve copia superficial do tabuleiro."""
    return [row[:] for row in t]

def _idx_from_pos(p):
    """Interna: converte posicao (c,l) em indices (r,c) 0..2."""
    c = COLS.index(obter_pos_c(p))
    r = ROWS.index(obter_pos_l(p))
    return r, c

def obter_peca(t, p):
    """Seletor: devolve peca na posicao p (' ' se livre)."""
    r, c = _idx_from_pos(p)
    return t[r][c]

def obter_vetor(t, s):
    """Seletor: tuplo com as pecas da linha (s em {'1','2','3'}) ou coluna (s em {'a','b','c'})."""
    if s in COLS:
        c = COLS.index(s)
        return tuple(t[r][c] for r in range(3))
    else:
        r = ROWS.index(s)
        return tuple(t[r][c] for c in range(3))

def coloca_peca(t, j, p):
    """Modificador: coloca peca j em p (destrutivo)."""
    r, c = _idx_from_pos(p)
    t[r][c] = j
    return t

def remove_peca(t, p):
    """Modificador: remove peca de p (coloca ' ')."""
    r, c = _idx_from_pos(p)
    t[r][c] = ' '
    return t

def move_peca(t, p_origem, p_destino):
    """Modificador: move peca de p_origem para p_destino."""
    j = obter_peca(t, p_origem)
    remove_peca(t, p_origem)
    coloca_peca(t, j, p_destino)
    return t

def _has_winner(t, j):
    """Interna: True se j tem 3 em linha horizontal ou vertical (usa WIN_LINES)."""
    for (a, b, c) in WIN_LINES:
        if t[a[0]][a[1]] == j and t[b[0]][b[1]] == j and t[c[0]][c[1]] == j:
            return True
    return False

def eh_tabuleiro(arg):
    """
    Reconhecedor do tabuleiro:
    - lista 3x3 de pecas validas
    - max 3 pecas por jogador
    - |#X - #O| <= 1
    - no maximo um vencedor em simultaneo
    """
    if not (isinstance(arg, list) and len(arg) == 3 and all(isinstance(row, list) and len(row) == 3 for row in arg)):
        return False
    flat = [arg[r][c] for r in range(3) for c in range(3)]
    if not all(eh_peca(x) for x in flat):
        return False
    nx = sum(1 for x in flat if x == 'X')
    no = sum(1 for x in flat if x == 'O')
    if nx > 3 or no > 3:
        return False
    if abs(nx - no) > 1:
        return False
    gx = _has_winner(arg, 'X')
    go = _has_winner(arg, 'O')
    if gx and go:
        return False
    return True

def eh_posicao_livre(t, p):
    """Reconhecedor: True se posicao p esta livre."""
    return obter_peca(t, p) == ' '

def tabuleiros_iguais(t1, t2):
    """Teste: True se t1 e t2 sao identicos."""
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and all(t1[r][c] == t2[r][c] for r in range(3) for c in range(3))

def tabuleiro_para_str(t):
    """Transformador: devolve a string do tabuleiro no formato esperado."""
    def row(r):
        # Ex.: "1 [ ]-[ ]-[ ]"
        return f"{ROWS[r]} " + '-'.join(peca_para_str(t[r][c]) for c in range(3))
    return '\n'.join([HEADER, row(0), CONN1, row(1), CONN2, row(2)])

def tuplo_para_tabuleiro(tp):
    """Transformador: (1,-1,0) -> ('X','O',' ')."""
    t = cria_tabuleiro()
    for r in range(3):
        for c in range(3):
            val = tp[r][c]
            j = 'X' if val == 1 else ('O' if val == -1 else ' ')
            t[r][c] = j
    return t

def obter_ganhador(t):
    """Alto nivel: devolve 'X' ou 'O' se ha ganhador; senao ' '."""
    if _has_winner(t, 'X'):
        return 'X'
    if _has_winner(t, 'O'):
        return 'O'
    return ' '

# -----------------------------------------------------------------------------
# Funcoes de alto nivel adicionais sobre tabuleiro
# -----------------------------------------------------------------------------
def _iter_pos_em_leitura():
    """Itera posicoes na ordem de leitura do tabuleiro.
    Ordem definida pelo enunciado: linhas 1..3 (de cima para baixo),
    e dentro de cada linha colunas a..c (da esquerda para a direita)."""
    for l in ROWS:
        for c in COLS:
            yield cria_posicao(c, l)

def obter_posicoes_livres(t):
    """Tuplo com posicoes livres (ordem de leitura)."""
    return tuple(p for p in _iter_pos_em_leitura() if eh_posicao_livre(t, p))

def obter_posicoes_jogador(t, j):
    """Tuplo com posicoes ocupadas por j (ordem de leitura)."""
    return tuple(p for p in _iter_pos_em_leitura() if obter_peca(t, p) == j)

# -----------------------------------------------------------------------------
# Apoio: fases e geracao de movimentos
# -----------------------------------------------------------------------------
def _total_pecas(t):
    """Interna: total de pecas (X+O) no tabuleiro."""
    return sum(1 for p in _iter_pos_em_leitura() if obter_peca(t, p) != ' ')

def _fase_colocacao(t):
    """Interna: True se total de pecas < 6."""
    return _total_pecas(t) < 6

def _adjacentes_livres(t, p):
    """Interna: devolve, por ordem de leitura, as posicoes adjacentes livres a p."""
    livres = []
    for q in _iter_pos_em_leitura():
        if q in obter_posicoes_adjacentes(p) and eh_posicao_livre(t, q):
            livres.append(q)
    return tuple(livres)

def _todos_movimentos(t, j):
    """
    Interna: gera todas as jogadas (src,dst) validas de movimento para j.
    - Ordem dos resultados: por ordem de leitura (primeira peca possivel,
      depois primeiro destino adjacente livre).
    - Regra de "passar": so e permitido quando NAO existe qualquer movimento
      real, caso em que devolve (p,p) usando a primeira peca por ordem de leitura.
    """
    jogadas = []
    # Ordem de leitura garantida: iteramos pelas posicoes do jogador em leitura
    for p in obter_posicoes_jogador(t, j):
        for q in _adjacentes_livres(t, p):
            jogadas.append((p, q))
    if not jogadas:
        pj = obter_posicoes_jogador(t, j)
        if pj:
            jogadas.append((pj[0], pj[0]))  # passar o turno
    return tuple(jogadas)

# -----------------------------------------------------------------------------
# obter_movimento_manual
# -----------------------------------------------------------------------------
def obter_movimento_manual(t, j):
    """
    Le a escolha do utilizador (via input) e valida:
    - Fase colocacao: 'cl' de posicao livre -> devolve (p,)
    - Fase movimento: 'c1l1c2l2' -> (origem, destino)
      * destino deve ser adjacente e livre
      * se origem==destino, interpreta como 'passar' APENAS se NAO HOUVER
        QUALQUER movimento possivel (todas as pecas do jogador bloqueadas)
    Se invalido, levanta ValueError('obter_movimento_manual: escolha invalida')
    """
    # Fase de colocacao
    if _fase_colocacao(t):
        s = input('Turno do jogador. Escolha uma posicao: ').strip()
        if len(s) == 2 and s[0] in COLS and s[1] in ROWS:
            p = cria_posicao(s[0], s[1])
            if eh_posicao_livre(t, p):
                return (p,)
        raise ValueError(ERR_MANUAL)

    # Fase de movimento
    s = input('Turno do jogador. Escolha um movimento: ').strip()
    if len(s) == 4 and s[0] in COLS and s[1] in ROWS and s[2] in COLS and s[3] in ROWS:
        p_origem = cria_posicao(s[0], s[1])
        p_destino = cria_posicao(s[2], s[3])
        tem_peca_propria = (obter_peca(t, p_origem) == j)
        movs = _todos_movimentos(t, j)
        existe_mov_real = any(not posicoes_iguais(a, b) for (a, b) in movs)
        pode_passar = tem_peca_propria and posicoes_iguais(p_origem, p_destino) and (not existe_mov_real)
        pode_mover = tem_peca_propria and (p_destino in obter_posicoes_adjacentes(p_origem)) and eh_posicao_livre(t, p_destino)
        if pode_passar or pode_mover:
            return p_origem, p_destino
    raise ValueError(ERR_MANUAL)

# -----------------------------------------------------------------------------
# obter_movimento_auto (AI)
# -----------------------------------------------------------------------------
def _posicoes_cantos():
    """Interna: posicoes de canto."""
    return cria_posicao('a','1'), cria_posicao('c','1'), cria_posicao('a','3'), cria_posicao('c','3')

def _posicoes_laterais():
    """Interna: posicoes laterais (nao centro, nao cantos)."""
    return cria_posicao('b','1'), cria_posicao('a','2'), cria_posicao('c','2'), cria_posicao('b','3')

def _encontre_jogada_vitoria_colocacao(t, j):
    """Se existe posicao livre que da vitoria imediata a j, devolve-a; senao None."""
    for p in obter_posicoes_livres(t):
        t2 = cria_copia_tabuleiro(t)
        coloca_peca(t2, j, p)
        if obter_ganhador(t2) == j:
            return p
    return None

def _encontre_jogada_bloqueio_colocacao(t, j):
    """Devolve posicao que bloqueia vitoria imediata do adversario, se existir."""
    o = 'O' if j == 'X' else 'X'
    return _encontre_jogada_vitoria_colocacao(t, o)

# --- IA: Colocacao ---------------------------------------------------------
def _auto_colocacao(t, j):
    """Heuristica: vitoria -> bloqueio -> centro -> cantos -> laterais.
    Devolve um tuplo com uma unica posicao (p,)."""
    # 1) Vitoria imediata
    p = _encontre_jogada_vitoria_colocacao(t, j)
    if p:
        return (p,)
    # 2) Bloqueio do adversario
    p = _encontre_jogada_bloqueio_colocacao(t, j)
    if p:
        return (p,)
    # 3) Centro
    b2 = cria_posicao('b','2')
    if eh_posicao_livre(t, b2):
        return (b2,)
    # 4) Cantos
    for p in _posicoes_cantos():
        if eh_posicao_livre(t, p):
            return (p,)
    # 5) Laterais
    for p in _posicoes_laterais():
        if eh_posicao_livre(t, p):
            return (p,)
    # Fallback
    livres = obter_posicoes_livres(t)
    return (livres[0],) if livres else (cria_posicao('a','1'),)

# --- Minimax (fase de movimento) ---------------------------------------
def _minimax(t, jogador_atual, max_depth=5):
    """Minimax com poda alpha-beta sobre movimentos gerados por ordem de leitura.
    Avaliacao: +1 ('X' vence), -1 ('O' vence), 0 caso contrario. X maximiza; O minimiza.
    Desempates: mantem determinismo escolhendo o primeiro melhor de acordo
    com a ordem dos movimentos gerados. Profundidade maxima por omissao: 5."""

    def aval(tb):
        g = obter_ganhador(tb)
        if g == 'X':
            return 1
        if g == 'O':
            return -1
        return 0

    def outro(j):
        return 'O' if j == 'X' else 'X'

    def ordenar_movimentos(tb, j, movs):
        # Heuristica de ordenacao: prioriza movimentos vencedores imediatos
        # do jogador atual, mantendo o restante pela ordem de geracao.
        ganhos, restantes = [], []
        for (po, pd) in movs:
            tb2 = cria_copia_tabuleiro(tb)
            if not posicoes_iguais(po, pd):
                move_peca(tb2, po, pd)
            if obter_ganhador(tb2) == j:
                ganhos.append((po, pd))
            else:
                restantes.append((po, pd))
        return tuple(ganhos + restantes)

    def mm(tb, j, depth, alpha, beta):
        g = obter_ganhador(tb)
        if g != ' ' or depth == 0:
            return aval(tb), None
        movs = _todos_movimentos(tb, j)
        if not movs:
            return aval(tb), None
        movs = ordenar_movimentos(tb, j, movs)
        if j == 'X':  # maximiza
            best_score, best_move = -10, None
            for (po, pd) in movs:
                tb2 = cria_copia_tabuleiro(tb)
                if not posicoes_iguais(po, pd):
                    move_peca(tb2, po, pd)
                score, _ = mm(tb2, outro(j), depth - 1, alpha, beta)
                if score > best_score:
                    best_score, best_move = score, (po, pd)
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break
            return best_score, best_move
        else:  # j == 'O' minimiza
            best_score, best_move = 10, None
            for (po, pd) in movs:
                tb2 = cria_copia_tabuleiro(tb)
                if not posicoes_iguais(po, pd):
                    move_peca(tb2, po, pd)
                score, _ = mm(tb2, outro(j), depth - 1, alpha, beta)
                if score < best_score:
                    best_score, best_move = score, (po, pd)
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break
            return best_score, best_move

    return mm(t, jogador_atual, max_depth, -10, 10)

# --- Movimento automatico ---------------------------------------------------
def obter_movimento_auto(t, j, nivel):
    """
    Movimento automatico:
    - Fase de colocacao (qualquer nivel): vitoria, bloqueio, centro, cantos, laterais.
    - Fase de movimento:
      * 'facil': primeiro movimento valido por ordem de leitura
      * 'normal': vitoria imediata; senao, igual a 'facil'
      * 'dificil': minimax(5)
    """
    # Fase de colocacao
    if _fase_colocacao(t):
        return _auto_colocacao(t, j)

    # Fase de movimento
    if nivel == 'facil':
        # Primeiro movimento possivel por ordem de leitura; se bloqueado, devolve (p,p).
        for p in obter_posicoes_jogador(t, j):
            for q in obter_posicoes_adjacentes(p):
                if eh_posicao_livre(t, q):
                    return p, q
        pj = obter_posicoes_jogador(t, j)
        return (pj[0], pj[0]) if pj else (cria_posicao('a','1'), cria_posicao('a','1'))

    if nivel == 'normal':
        # procura vitoria imediata
        for (po, pd) in _todos_movimentos(t, j):
            if posicoes_iguais(po, pd):
                continue
            t2 = cria_copia_tabuleiro(t)
            move_peca(t2, po, pd)
            if obter_ganhador(t2) == j:
                return po, pd
        # fallback: facil
        for p in obter_posicoes_jogador(t, j):
            for q in obter_posicoes_adjacentes(p):
                if eh_posicao_livre(t, q):
                    return p, q
        pj = obter_posicoes_jogador(t, j)
        return (pj[0], pj[0]) if pj else (cria_posicao('a','1'), cria_posicao('a','1'))

    # dificil
    score, mv = _minimax(t, j, max_depth=5)
    if mv is None:
        # fallback: algum movimento legal
        for p in obter_posicoes_jogador(t, j):
            for q in obter_posicoes_adjacentes(p):
                if eh_posicao_livre(t, q):
                    return p, q
        pj = obter_posicoes_jogador(t, j)
        return (pj[0], pj[0]) if pj else (cria_posicao('a','1'), cria_posicao('a','1'))
    return mv

# -----------------------------------------------------------------------------
# Funcao principal
# -----------------------------------------------------------------------------
def _aplicar_movimento(t, j, mv):
    """Aplica colocacao ou movimento (inclui passar). Devolve o proprio tabuleiro."""
    if _fase_colocacao(t):
        coloca_peca(t, j, mv[0])
    else:
        if len(mv) == 2 and posicoes_iguais(mv[0], mv[1]):
            pass  # passar
        else:
            move_peca(t, mv[0], mv[1])
    return t

def moinho(jogador, nivel):
    """
    Funcao principal do jogo.
    Argumentos: jogador em {'[X]','[O]'} e nivel em {'facil','normal','dificil'}.
    Se invalidos, levanta ValueError('moinho: argumentos invalidos').
    Mensagens:
    - 'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade <nivel>.'
    - 'Turno do computador (<nivel>):'
    Termina quando ha ganhador; devolve '[X]' ou '[O]'.
    """
    if not (isinstance(jogador, str) and jogador in ('[X]', '[O]') and isinstance(nivel, str) and nivel in ('facil', 'normal', 'dificil')):
        raise ValueError(ERR_MOINHO)
    humano = 'X' if jogador == '[X]' else 'O'
    cpu = 'O' if humano == 'X' else 'X'
    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {nivel}.')
    t = cria_tabuleiro()
    print(tabuleiro_para_str(t))
    turno = 'X'  # X comeca
    while obter_ganhador(t) == ' ':
        if turno == humano:
            mv = obter_movimento_manual(t, humano)
            _aplicar_movimento(t, humano, mv)
            print(tabuleiro_para_str(t))
        else:
            print(f'Turno do computador ({nivel}):')
            mv = obter_movimento_auto(t, cpu, nivel)
            _aplicar_movimento(t, cpu, mv)
            print(tabuleiro_para_str(t))
        turno = 'O' if turno == 'X' else 'X'
    g = obter_ganhador(t)

    return peca_para_str(g)

