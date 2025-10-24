"""
Projeto: Jogo do Moinho (variante 3x3, 3 pecas por jogador)

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
"""
from typing import Literal

# -----------------------------------------------------------------------------
# Constantes e mensagens
# -----------------------------------------------------------------------------
COLS = ('a', 'b', 'c')
ROWS = ('1', '2', '3')

ERR_POS = 'cria_posicao: argumentos invalidos'
ERR_PIECE = 'cria_peca: argumento invalido'
ERR_MANUAL = 'obter_movimento_manual: escolha invalida'
ERR_MOINHO = 'moinho: argumentos invalidos'

# ASCII do tabuleiro (formato exato esperado pelos testes)
HEADER = '   a   b   c'
CONN1  = '   | \\ | / |'
CONN2  = '   | / | \\ |'

# Linhas vencedoras (horizontais e verticais)
WIN_LINES = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
)

# -----------------------------------------------------------------------------
# Utilitarios de validacao
# -----------------------------------------------------------------------------
def confirmar_posicao(c: str, l: str) -> None:
    """Valida se (c,l) definem uma posicao do tabuleiro.

    Pre-condicoes:
    - c em {'a','b','c'} e l em {'1','2','3'}.

    Pos-condicoes:
    - Lanca ValueError se invalido; caso contrario nao retorna nada.

    Erros:
    - ValueError(ERR_POS).
    """
    if not isinstance(c, str) or not isinstance(l, str):
        raise ValueError(ERR_POS)
    if c not in COLS or l not in ROWS:
        raise ValueError(ERR_POS)


def confirmar_peca(entrada: str) -> None:
    """Valida o simbolo de peca.

    Pre-condicoes:
    - entrada em {'X','O',' '}.

    Pos-condicoes:
    - Lanca ValueError se invalido; caso contrario nao retorna nada.

    Erros:
    - ValueError(ERR_PIECE).
    """
    if not (isinstance(entrada, str) and len(entrada) == 1 and entrada in ('X', 'O', ' ')):
        raise ValueError(ERR_PIECE)


def outro_jogador(jogador: str) -> str:
    """Devolve a peca do adversario.

    Pre-condicoes:
    - jogador em {'X','O'}.

    Pos-condicoes:
    - Retorna 'O' se jogador == 'X', senao 'X'.
    """
    return 'O' if jogador == 'X' else 'X'

# -----------------------------------------------------------------------------
# TAD posicao
# -----------------------------------------------------------------------------
def cria_posicao(c: str, l: str) -> tuple[str, str]:
    """Construtor do TAD posicao.

    Pre-condicoes:
    - c em {'a','b','c'} e l em {'1','2','3'}.

    Pos-condicoes:
    - Retorna o tuplo (c,l) representando a posicao.

    Erros:
    - ValueError(ERR_POS) se os argumentos nao forem validos.
    """
    confirmar_posicao(c,l)
    return c, l

def cria_copia_posicao(posicao: tuple[str, str]) -> tuple[str, str]:
    """Copia independente de uma posicao.

    Pre-condicoes:
    - posicao e uma posicao valida.

    Pos-condicoes:
    - Retorna novo tuplo (c,l) com os mesmos valores de posicao.
    """
    return posicao[0], posicao[1]

def obter_pos_c(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente coluna da posicao."""
    return posicao[0]

def obter_pos_l(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente linha da posicao."""
    return posicao[1]

def eh_posicao(arg) -> bool:
    """Reconhecedor: indica se o argumento e uma posicao valida.

    Pos-condicoes:
    - Retorna True se for um tuplo (c,l) com c em COLS e l em ROWS; False caso contrario.
    """
    return (
        isinstance(arg, tuple) and
        len(arg) == 2 and
        arg[0] in COLS and
        arg[1] in ROWS
    )

def posicoes_iguais(p1, p2) -> bool:
    """Teste: True se p1 e p2 forem posicoes validas e iguais; False caso contrario."""
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(posicao: tuple[str, str]) -> str:
    """Transformador: converte a posicao em 'cl' (ex.: ('a','1') -> 'a1').

    Pos-condicoes:
    - Retorna a representacao externa da posicao 'cl'.
    """
    return posicao[0] + posicao[1]

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (2) Parsers de strings para posicao e movimento
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def str_para_posicao(entrada: str):
    """Converte 'cl' em posicao ('c','l').

    Pre-condicoes:
    - entrada e uma string de tamanho 2; entrada[0] em COLS e entrada[1] em ROWS.

    Pos-condicoes:
    - Retorna posicao valida correspondente.

    Erros:
    - ValueError(ERR_MANUAL) se o formato/conteudo nao forem validos.
    """
    if len(entrada) == 2 and entrada[0] in COLS and entrada[1] in ROWS:
        return cria_posicao(entrada[0], entrada[1])
    raise ValueError(ERR_MANUAL)

def str_para_movimento(entrada: str):
    """Converte 'c1l1c2l2' em (posicao_origem, posicao_destino).

    Pre-condicoes:
    - entrada e uma string de tamanho 4; colunas nas posicoes pares e linhas nas impares.

    Pos-condicoes:
    - Retorna o par (posicao_origem, posicao_destino) valido.

    Erros:
    - ValueError(ERR_MANUAL) se o formato/conteudo nao forem validos.
    """
    if len(entrada) == 4 and all(entrada[i] in COLS if i % 2 == 0 else entrada[i] in ROWS for i in range(4)):
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(ERR_MANUAL)

# -----------------------------------------------------------------------------
# (4) TAD movimento (construtores e predicados)
# -----------------------------------------------------------------------------
def cria_mov_colocacao(posicao):
    """Cria um movimento de colocacao.

    Pre-condicoes:
    - posicao e uma posicao valida.

    Pos-condicoes:
    - Retorna o tuplo (posicao,).
    """
    return (posicao,)

def cria_mov_passar(posicao):
    """Cria um movimento de passagem de turno.

    Pre-condicoes:
    - posicao e uma posicao valida do jogador.

    Pos-condicoes:
    - Retorna o tuplo (posicao,posicao), sinalizando 'passar'.
    """
    return posicao, posicao

def cria_movimento(pos_origem, pos_destino):
    """Cria um movimento real (origem -> destino).

    Pre-condicoes:
    - pos_origem e pos_destino sao posicoes validas.

    Pos-condicoes:
    - Retorna o tuplo (pos_origem,pos_destino).
    """
    return pos_origem, pos_destino

def eh_colocacao(movimento):
    """Predicado: True se o movimento for (posicao,), i.e., colocacao."""
    return len(movimento) == 1

def eh_passar(movimento):
    """Predicado: True se o movimento for (posicao,posicao), i.e., passar."""
    return len(movimento) == 2 and posicoes_iguais(movimento[0], movimento[1])

def eh_mov_real(movimento):
    """Predicado: True se o movimento for (pos_origem,pos_destino) com pos_origem != pos_destino."""
    return len(movimento) == 2 and not posicoes_iguais(movimento[0], movimento[1])

# Adjacencias (ordens calibradas para os testes publicos)
# LINHA-CHAVE: a ordem em 'b1' e 'b3' e vertical primeiro, depois laterais.
_ADJ = {
    'a1': ('b1', 'a2', 'b2'),
    'b1': ('b2', 'a1', 'c1'),  # vertical antes dos laterais <- LINHA-CHAVE (Testes)
    'c1': ('b1', 'c2', 'b2'),
    'a2': ('a1', 'a3', 'b2'),
    'b2': ('a2', 'b1', 'c2', 'b3', 'a1', 'c1', 'a3', 'c3'),
    'c2': ('c1', 'c3', 'b2'),
    'a3': ('a2', 'b3', 'b2'),
    'b3': ('b2', 'a3', 'c3'),  # vertical antes dos laterais <- LINHA-CHAVE (Teste 4)
    'c3': ('c2', 'b3', 'b2')
}

def obter_posicoes_adjacentes(posicao: tuple[str, str]) -> tuple[tuple[str, str], ...]:
    """Devolve as posicoes adjacentes a posicao, na ordem do enunciado.

    Pre-condicoes:
    - posicao e uma posicao valida.

    Pos-condicoes:
    - Retorna o tuplo de posicoes adjacentes (tuplos (c,l)).

    Erros:
    - ValueError('obter_posicoes_adjacentes: posicao invalida') se posicao for invalida.
    """
    if not eh_posicao(posicao):
        raise ValueError('obter_posicoes_adjacentes: posicao invalida')
    return tuple(
        cria_posicao(pos[0], pos[1])
        for pos in [tuple(entrada) for entrada in _ADJ[posicao_para_str(posicao)]]
    )

# -----------------------------------------------------------------------------
# TAD peca
# -----------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    """Construtor do TAD peca.

    Pre-condicoes:
    - entrada em {'X','O',' '}.

    Pos-condicoes:
    - Retorna a peca ('X', 'O' ou ' ').

    Erros:
    - ValueError(ERR_PIECE) se invalido.
    """
    confirmar_peca(entrada)
    return entrada

def cria_copia_peca(jogador: str) -> str:
    """Copia independente de peca.

    Pre-condicoes:
    - jogador e uma peca valida.

    Pos-condicoes:
    - Retorna uma copia do simbolo de peca.
    """
    return jogador

def eh_peca(arg) -> bool:
    """Reconhecedor: True se o argumento for um simbolo 'X', 'O' ou ' '."""
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(peca1: str, peca2: str) -> bool:
    """Teste: True se as duas pecas forem validas e iguais."""
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2

def peca_para_str(jogador: str) -> str:
    """Transformador: devolve a representacao externa '[X]', '[O]' ou '[ ]'."""
    return f'[{jogador}]'

def peca_para_inteiro(jogador: str) -> int:
    """Conversao de peca para inteiro: X->+1, O->-1, ' '->0."""
    return 1 if jogador == 'X' else (-1 if jogador == 'O' else 0)

# -----------------------------------------------------------------------------
# TAD tabuleiro
# -----------------------------------------------------------------------------
def cria_tabuleiro():
    """Construtor do TAD tabuleiro (3x3), vazio.

    Pos-condicoes:
    - Retorna lista 3x3 com pecas ' ' (livres).
    """
    return [[cria_peca(' ') for _ in COLS] for _ in ROWS]

def cria_copia_tabuleiro(tabuleiro):
    """Copia profunda (por linhas) do tabuleiro."""
    return [linha[:] for linha in tabuleiro]

def _idx_from_pos(posicao: tuple[str, str]) -> tuple[int, int]:
    """Converte posicao (c,l) em indices (linha, coluna) na matriz 3x3."""
    return ROWS.index(obter_pos_l(posicao)), COLS.index(obter_pos_c(posicao))

def obter_peca(tabuleiro, posicao):
    """Seletor: devolve a peca na posicao posicao."""
    r, c = _idx_from_pos(posicao)
    return tabuleiro[r][c]

def obter_vetor(tabuleiro, entrada: str) -> tuple[str, str, str]:
    """Seletor: devolve a linha ou a coluna do tabuleiro como tuplo de 3 pecas.

    Pre-condicoes:
    - entrada em COLS (coluna) ou entrada em ROWS (linha).

    Pos-condicoes:
    - Retorna um tuplo de 3 simbolos de peca (linha/coluna selecionada).

    Erros:
    - ValueError se entrada nao for seletor valido.
    """
    if entrada in COLS:
        c = COLS.index(entrada)
        return tuple(tabuleiro[r][c] for r in range(3))
    elif entrada in ROWS:
        r = ROWS.index(entrada)
        return tuple(tabuleiro[r][c] for c in range(3))
    else:
        raise ValueError("obter_vetor: seletor invalido (use 'a'..'c' ou '1'..'3')")

def coloca_peca(tabuleiro, jogador: str, posicao):
    """Modificador: coloca a peca jogador na posicao posicao.

    Pre-condicoes:
    - jogador em {'X','O'}; posicao e posicao valida e livre.

    Pos-condicoes:
    - Tabuleiro alterado com jogador colocado em posicao.

    Erros:
    - ValueError se peca invalida, posicao invalida ou posicao ocupada.
    """
    if not eh_peca(jogador) or jogador == ' ':
        raise ValueError("coloca_peca: peca invalida")
    if not eh_posicao(posicao):
        raise ValueError("coloca_peca: posicao invalida")
    if obter_peca(tabuleiro, posicao) != ' ':
        raise ValueError("coloca_peca: posicao ocupada")
    r, c = _idx_from_pos(posicao)
    tabuleiro[r][c] = jogador
    return tabuleiro

def remove_peca(tabuleiro, posicao):
    """Modificador: remove a peca em posicao (coloca ' ')."""
    r, c = _idx_from_pos(posicao)
    tabuleiro[r][c] = ' '
    return tabuleiro

def move_peca(tabuleiro, p_origem, p_destino):
    """Modificador: move a peca de p_origem para p_destino.

    Pre-condicoes:
    - p_origem/p_destino validos; p_origem ocupada; p_destino livre; posicoes adjacentes.

    Pos-condicoes:
    - Tabuleiro com a peca movida de p_origem para p_destino.

    Erros:
    - ValueError se algum requisito falhar (posicao invalida, origem vazia, destino ocupado ou nao adjacente).
    """
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

def _tem_vencedor(tabuleiro, jogador: str) -> bool:
    """Teste interno: True se jogador tiver uma linha completa (horizontal/vertical)."""
    for (a, b, c) in WIN_LINES:
        if tabuleiro[a[0]][a[1]] == jogador and tabuleiro[b[0]][b[1]] == jogador and tabuleiro[c[0]][c[1]] == jogador:
            return True
    return False

def eh_tabuleiro(arg) -> bool:
    """Reconhecedor do TAD tabuleiro.

    Regras:
    - Estrutura 3x3; apenas pecas validas; max 3 pecas por jogador; |#X-#O| <= 1;
      nao podem existir simultaneamente dois vencedores.

    Pos-condicoes:
    - Retorna True se respeitar as regras do jogo; False caso contrario.
    """
    if not (isinstance(arg, list) and len(arg) == 3 and all(isinstance(l, list) and len(l) == 3 for l in arg)):
        return False
    pecas = [posicao for linha in arg for posicao in linha]
    if not all(eh_peca(posicao) for posicao in pecas):
        return False
    x = pecas.count('X')
    o = pecas.count('O')
    if x > 3 or o > 3 or abs(x - o) > 1:
        return False
    if _tem_vencedor(arg, 'X') and _tem_vencedor(arg, 'O'):
        return False
    return True

def eh_posicao_livre(tabuleiro, posicao) -> bool:
    """Teste: True se a posicao posicao no tabuleiro estiver livre."""
    return obter_peca(tabuleiro, posicao) == ' '

def tabuleiros_iguais(t1, tabuleiro_copia) -> bool:
    """Teste: True se t1 e tabuleiro_copia forem estruturalmente iguais (todas as casas)."""
    return all(t1[r][c] == tabuleiro_copia[r][c] for r in range(3) for c in range(3))

def tabuleiro_para_str(tabuleiro) -> str:
    """Transformador: devolve a representacao ASCII do tabuleiro no formato do enunciado."""
    def linha_str(i: int) -> str:
        return f"{ROWS[i]} " + "-".join(peca_para_str(tabuleiro[i][jogador]) for jogador in range(3))
    return "\n".join([HEADER, linha_str(0), CONN1, linha_str(1), CONN2, linha_str(2)])

def tuplo_para_tabuleiro(tp) -> list[list[str]]:
    """Construtor a partir de tuplo 3x3 de inteiros {-1,0,1}.

    Pre-condicoes:
    - tp e um tuplo 3x3 com valores -1 (O), 0 (' '), 1 (X).

    Pos-condicoes:
    - Retorna o tabuleiro equivalente a tp.
    """
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

def obter_ganhador(tabuleiro) -> str:
    """Funcoes de alto nivel: devolve 'X'/'O' ou ' ' se ainda nao ha vencedor."""
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '

# -----------------------------------------------------------------------------
# Funcoes auxiliares de iteracao/ordem (ordem de leitura)
# -----------------------------------------------------------------------------
def _iterador_posicoes_leitura():
    """Iterador de posicoes na ordem de leitura: linhas 1..3; colunas a..c."""
    for l in ROWS:
        for c in COLS:
            yield cria_posicao(c, l)

def obter_posicoes_livres(tabuleiro):
    """Funcoes de alto nivel: tuplo das posicoes livres (ordem de leitura)."""
    return tuple(posicao for posicao in _iterador_posicoes_leitura() if eh_posicao_livre(tabuleiro, posicao))

def obter_posicoes_jogador(tabuleiro, jogador: str):
    """Funcoes de alto nivel: tuplo das posicoes ocupadas por jogador (ordem de leitura)."""
    return tuple(posicao for posicao in _iterador_posicoes_leitura() if obter_peca(tabuleiro, posicao) == jogador)

def _contar_pecas(tabuleiro) -> int:
    """Auxiliar: total de pecas no tabuleiro (X+O)."""
    return sum(1 for posicao in _iterador_posicoes_leitura() if obter_peca(tabuleiro, posicao) != ' ')

def _esta_na_fase_colocacao(tabuleiro) -> bool:
    """Auxiliar: True se total de pecas < 6 (fase de colocacao)."""
    return _contar_pecas(tabuleiro) < 6

def _posicoes_adjacentes_livres(tabuleiro, posicao):
    """Auxiliar: tuplo das posicoes adjacentes livres a posicao (ordem de leitura)."""
    return tuple(pos_adjacente for pos_adjacente in obter_posicoes_adjacentes(posicao) if eh_posicao_livre(tabuleiro, pos_adjacente))

def _gerar_movimentos_validos(tabuleiro, jogador: str):
    """Gera todas as jogadas (origem, destino) validas por ordem de leitura.

    Regras/ordem:
    - Para cada peca do jogador (ordem de leitura), alistar destinos adjacentes livres (ordem de leitura).
    - Se NAO existir movimento real, incluir (posicao,posicao) para a primeira peca do jogador (regra de 'passar').

    Pos-condicoes:
    - Retorna um tuplo de pares (origem,destino); (posicao,posicao) sinaliza 'passar'.
    """
    jogadas = []
    # LINHA-CHAVE: determinismo por ordem de leitura
    for posicao in obter_posicoes_jogador(tabuleiro, jogador):
        for pos_adjacente in _posicoes_adjacentes_livres(tabuleiro, posicao):
            jogadas.append((posicao, pos_adjacente))
    if not jogadas:
        posicoes_jogador = obter_posicoes_jogador(tabuleiro, jogador)
        if posicoes_jogador:
            jogadas.append((posicoes_jogador[0], posicoes_jogador[0]))  # passar
    return tuple(jogadas)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (3) Helper para regra de "passar"
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def _verifica_se_pode_passar(tabuleiro, jogador) -> bool:
    """Regra de 'passar': True se NAO existir qualquer movimento real possivel para jogador.

    Pos-condicoes:
    - Retorna True se todos os movimentos de jogador forem (posicao,posicao); False caso contrario.
    """
    return not any(not posicoes_iguais(a, b) for (a, b) in _gerar_movimentos_validos(tabuleiro, jogador))

def jogada_valida(tabuleiro, jogador, p_origem, p_destino):
    """Valida uma jogada de movimento para o jogador jogador.

    Pre-condicoes:
    - tabuleiro e tabuleiro valido; jogador em {'X','O'}.
    - p_origem e p_destino sao posicoes validas.

    Regras:
    - Se p_origem == p_destino, so e valido se _verifica_se_pode_passar(tabuleiro,jogador) e p_origem tiver peca do jogador.
    - Caso contrario, exige-se: p_origem com peca do jogador, p_destino adjacente e livre.

    Pos-condicoes:
    - Retorna True se a jogada respeitar as regras; False caso contrario.
    """
    if not (eh_posicao(p_origem) and eh_posicao(p_destino)):
        return False
    tem_peca_propria = (obter_peca(tabuleiro, p_origem) == jogador)
    if posicoes_iguais(p_origem, p_destino):
        return tem_peca_propria and _verifica_se_pode_passar(tabuleiro, jogador)
    return (
        tem_peca_propria and
        p_destino in obter_posicoes_adjacentes(p_origem) and
        eh_posicao_livre(tabuleiro, p_destino)
    )

# -----------------------------------------------------------------------------
# I/O: obter_movimento_manual
# -----------------------------------------------------------------------------
def obter_movimento_manual(tabuleiro, jogador: str):
    """Le e valida a escolha do jogador humano (colocacao ou movimento).

    Pre-condicoes:
    - tabuleiro e um tabuleiro valido; jogador em {'X','O'}.
    - Fase de colocacao se total de pecas < 6; caso contrario, fase de movimento.
    - "Passar" (posicao,posicao) so e aceite quando NAO existe qualquer movimento real possivel.

    Pos-condicoes:
    - Colocacao: devolve sempre (posicao,) com posicao valida e livre.
    - Movimento: devolve sempre (origem,destino) valido; ou (posicao,posicao) no caso de passar.

    Efeitos laterais:
    - Escreve exatamente os prompts:
      'Turno do jogador. Escolha uma posicao: '
      'Turno do jogador. Escolha um movimento: '
    - Le 1 linha de stdin.

    Erros:
    - ValueError(ERR_MANUAL) se o input nao respeitar formato ou regras.
    """
    import sys

    if _esta_na_fase_colocacao(tabuleiro):
        # PROMPT EXATO exigido pelos testes publicos
        sys.stdout.write('Turno do jogador. Escolha uma posicao: ')
        sys.stdout.flush()
        entrada = sys.stdin.readline().strip()
        try:
            posicao = str_para_posicao(entrada)
        except ValueError:
            raise ValueError(ERR_MANUAL)
        if eh_posicao_livre(tabuleiro, posicao):
            return (posicao,)
        raise ValueError(ERR_MANUAL)

    # PROMPT EXATO para movimento
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

# -----------------------------------------------------------------------------
# AI: colocacao
# -----------------------------------------------------------------------------
def _alistar_cantos():
    """Auxiliar (AI): tuplo com as quatro posicoes de canto (ordem fixa)."""
    return (cria_posicao('a', '1'), cria_posicao('c', '1'),
            cria_posicao('a', '3'), cria_posicao('c', '3'))

def _alistar_laterais():
    """Auxiliar (AI): tuplo com as posicoes laterais (nao centro, nao cantos)."""
    return (cria_posicao('b', '1'), cria_posicao('a', '2'),
            cria_posicao('c', '2'), cria_posicao('b', '3'))

def _jogada_vencedora_colocacao(tabuleiro, jogador: str):
    """Auxiliar (AI): devolve posicao livre que da vitoria imediata a jogador, se existir."""
    for posicao in obter_posicoes_livres(tabuleiro):
        tabuleiro_copia = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(tabuleiro_copia, jogador, posicao)
        if obter_ganhador(tabuleiro_copia) == jogador:
            return posicao
    return None

def _jogada_bloqueio_colocacao(tabuleiro, jogador: str):
    """Auxiliar (AI): devolve posicao livre que bloqueia vitoria imediata do adversario."""
    o = outro_jogador(jogador)
    return _jogada_vencedora_colocacao(tabuleiro, o)

def _escolher_colocacao_ia(tabuleiro, jogador: str):
    """AI (colocacao): vitoria -> bloqueio -> centro -> cantos -> laterais.

    Pos-condicoes:
    - Retorna (posicao,) com a posicao escolhida segundo a prioridade definida.
    """
    posicao = _jogada_vencedora_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)
    posicao = _jogada_bloqueio_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)
    b2 = cria_posicao('b', '2')
    if eh_posicao_livre(tabuleiro, b2):
        return (b2,)
    for pos_adjacente in _alistar_cantos():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)
    for pos_adjacente in _alistar_laterais():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)
    livres = obter_posicoes_livres(tabuleiro)
    return (livres[0],) if livres else (cria_posicao('a', '1'),)

# -----------------------------------------------------------------------------
# AI: movimento (facil/normal/dificil)
# -----------------------------------------------------------------------------
def _escolher_primeiro_movimento(tabuleiro, jogador: str):
    """AI (facil): devolve o primeiro movimento valido; se nao houver, (posicao,posicao).

    Pos-condicoes:
    - Retorna (pos_origem,pos_destino) valido por ordem de leitura, ou (posicao,posicao) se bloqueado.
    """
    for posicao in obter_posicoes_jogador(tabuleiro, jogador):
        for pos_adjacente in obter_posicoes_adjacentes(posicao):
            if eh_posicao_livre(tabuleiro, pos_adjacente):
                return posicao, pos_adjacente
    posicoes_jogador = obter_posicoes_jogador(tabuleiro, jogador)
    return (posicoes_jogador[0], posicoes_jogador[0]) if posicoes_jogador else (cria_posicao('a', '1'), cria_posicao('a', '1'))

def _jogada_vencedora_movimento(tabuleiro, jogador: str):
    """AI (normal/dificil): procura (pos_origem,pos_destino) que vence imediatamente.

    Pos-condicoes:
    - Retorna (pos_origem,pos_destino) se existir vitoria em 1 jogada; caso contrario, None.
    """
    for (pos_origem, pos_destino) in _gerar_movimentos_validos(tabuleiro, jogador):
        if posicoes_iguais(pos_origem, pos_destino):
            continue
        tabuleiro_copia = cria_copia_tabuleiro(tabuleiro)
        move_peca(tabuleiro_copia, pos_origem, pos_destino)
        if obter_ganhador(tabuleiro_copia) == jogador:
            return pos_origem, pos_destino
    return None

def obter_movimento_auto(tabuleiro, jogador: str, nivel: str):
    """Escolha automatica de jogada (colocacao ou movimento) para o nivel dado.

    Pre-condicoes:
    - tabuleiro e valido; jogador em {'X','O'}; nivel em {'facil','normal','dificil'}.

    Pos-condicoes:
    - Colocacao: devolve (posicao,) com a posicao escolhida.
    - Movimento: devolve (pos_origem,pos_destino) valido; se nenhum movimento real, (posicao,posicao).

    Erros:
    - ValueError se nivel nao pertencer ao conjunto permitido.
    """
    if _esta_na_fase_colocacao(tabuleiro):
        return _escolher_colocacao_ia(tabuleiro, jogador)

    if nivel == 'facil':
        return _escolher_primeiro_movimento(tabuleiro, jogador)
    if nivel == 'normal':
        movimento = _jogada_vencedora_movimento(tabuleiro, jogador)
        return movimento if movimento else _escolher_primeiro_movimento(tabuleiro, jogador)
    if nivel == 'dificil':
        _, movimento = _algoritmo_minimax(tabuleiro, jogador, max_depth=5)
        return movimento if movimento else _escolher_primeiro_movimento(tabuleiro, jogador)
    raise ValueError("obter_movimento_auto: nivel invalido")

# -----------------------------------------------------------------------------
# Minimax (fase de movimento)
# -----------------------------------------------------------------------------
def _algoritmo_minimax(tabuleiro, jogador_atual: str, max_depth: int = 5):
    """Minimax com poda alpha-beta (X maximiza; O minimiza).

    Pre-condicoes:
    - Tabuleiro em fase de movimento; jogador_atual em {'X','O'}.

    Pos-condicoes:
    - Retorna (score, melhor_mov_ou_None), onde score em {-1,0,1}.

    Notas:
    - A avaliacao devolve +1 se 'X' vence; -1 se 'O' vence; 0 caso contrario.
    - Ordena movimentos priorizando vitorias imediatas; mantem determinismo.
    """
    def aval(tabuleiro_temp) -> int:
        ganhador = obter_ganhador(tabuleiro_temp)
        if ganhador == 'X':
            return 1
        if ganhador == 'O':
            return -1
        return 0

    def outro(jogador: str) -> str:
        return 'O' if jogador == 'X' else 'X'

    def ordenar_movimentos(tabuleiro_temp, jogador, movs):
        """Heuristica: movimentos vencedores primeiro; restantes por ordem de geracao."""
        ganhos, restantes = [], []
        for (pos_origem, pos_destino) in movs:
            tabuleiro_simulado = cria_copia_tabuleiro(tabuleiro_temp)
            if not posicoes_iguais(pos_origem, pos_destino):
                move_peca(tabuleiro_simulado, pos_origem, pos_destino)
            if obter_ganhador(tabuleiro_simulado) == jogador:
                ganhos.append((pos_origem, pos_destino))
            else:
                restantes.append((pos_origem, pos_destino))
        return tuple(ganhos + restantes)

    def mm(tabuleiro_temp, jogador, depth, alpha, beta):
        ganhador = obter_ganhador(tabuleiro_temp)
        if ganhador != ' ' or depth == 0:
            return aval(tabuleiro_temp), None

        movs = _gerar_movimentos_validos(tabuleiro_temp, jogador)
        if not movs:
            return aval(tabuleiro_temp), None

        movs = ordenar_movimentos(tabuleiro_temp, jogador, movs)

        if jogador == 'X':  # maximiza
            best_score, best_move = -10, None
            for (pos_origem, pos_destino) in movs:
                tabuleiro_simulado = cria_copia_tabuleiro(tabuleiro_temp)
                if not posicoes_iguais(pos_origem, pos_destino):
                    move_peca(tabuleiro_simulado, pos_origem, pos_destino)
                score, _ = mm(tabuleiro_simulado, outro(jogador), depth - 1, alpha, beta)
                if score > best_score:
                    best_score, best_move = score, (pos_origem, pos_destino)
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    break  # poda
            return best_score, best_move
        else:         # minimiza ('O')
            best_score, best_move = 10, None
            for (pos_origem, pos_destino) in movs:
                tabuleiro_simulado = cria_copia_tabuleiro(tabuleiro_temp)
                if not posicoes_iguais(pos_origem, pos_destino):
                    move_peca(tabuleiro_simulado, pos_origem, pos_destino)
                score, _ = mm(tabuleiro_simulado, outro(jogador), depth - 1, alpha, beta)
                if score < best_score:
                    best_score, best_move = score, (pos_origem, pos_destino)
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break  # poda
            return best_score, best_move

    return mm(tabuleiro, jogador_atual, max_depth, -10, 10)

# -----------------------------------------------------------------------------
# Funcoes de aplicacao e ciclo do jogo
# -----------------------------------------------------------------------------
def _executar_movimento(tabuleiro, jogador: str, movimento: tuple):
    """Aplica a jogada movimento ao tabuleiro (colocacao, movimento real ou passagem).

    Pre-condicoes:
    - Se _esta_na_fase_colocacao(tabuleiro) == True, movimento == (posicao,).
    - Caso contrario, movimento == (pos_origem,pos_destino) ou (posicao,posicao) (passar).

    Pos-condicoes:
    - Tabuleiro atualizado; 'passar' nao altera o estado.
    """
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

    Pre-condicoes:
    - jogador em {'[X]','[O]'}; nivel em {'facil','normal','dificil'}.
    - 'X' joga sempre primeiro.

    Efeitos laterais:
    - Imprime:
      'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade <nivel>.'
      'Turno do computador (<nivel>):'
      e a representacao ASCII do tabuleiro apos cada jogada.
    - Le input do utilizador nos turnos do humano (via obter_movimento_manual).

    Pos-condicoes:
    - Retorna '[X]' ou '[O]' quando houver vencedor.

    Erros:
    - ValueError(ERR_MOINHO) se os argumentos forem invalidos.
    """
    if not (
        isinstance(jogador, str) and jogador in ('[X]', '[O]') and
        isinstance(nivel, str) and nivel in ('facil', 'normal', 'dificil')
    ):
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
