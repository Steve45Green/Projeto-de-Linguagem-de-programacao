"""
Projeto: Jogo do Moinho (variante 3x3, 3 pecas por jogador)
Autor: <Jose Ameixa | Diogo Vaz | Pedro Duarte >
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
import sys

# -------------------------------------------------------------------------------------------------
# Constantes e mensagens
# -------------------------------------------------------------------------------------------------
# --- Identificadores ---
COLUNAS = ('a', 'b', 'c')
LINHAS = ('1', '2', '3')

# --- Mensagens de Erro  ---
ERRO_POSICAO = 'cria_posicao: argumentos invalidos'
ERRO_PECA = 'cria_peca: argumento invalido'
ERRO_JOGADA_MANUAL = 'obter_movimento_manual: escolha invalida'
ERRO_JOGO = 'moinho: argumentos invalidos'

# --- Representacao ASCII ---
CABECALHO = '   a   b   c'
CONEXAO_1 = '   | \\ | / |'
CONEXAO_2 = '   | / | \\ |'

# --- Logica de Vitoria ---
LINHAS_VENCEDORAS = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
)

# -------------------------------------------------------------------------------------------------
# Utilitarios de validacao
# -------------------------------------------------------------------------------------------------
def confirmar_posicao(coluna: str, linha: str) -> None:
    """
    Valida se uma coluna e linha formam uma posicao valida no tabuleiro 3x3.
    Levanta um erro se os componentes nao forem validos.

    Args:
        coluna (str): A componente coluna (esperado: 'a', 'b' ou 'c').
        linha (str): A componente linha (esperado: '1', '2' ou '3').

    Raises:
        ValueError: Se os argumentos forem invalidos (ERRO_POSICAO).
    """
    if not isinstance(coluna, str) or not isinstance(linha, str):
        raise ValueError(ERRO_POSICAO)
    if coluna not in COLUNAS or linha not in LINHAS:
        raise ValueError(ERRO_POSICAO)

def confirmar_peca(entrada: str) -> None:
    """
    Valida se a string de entrada corresponde a um simbolo de peca valido.
    Levanta um erro se o simbolo nao for valido.

    Args:
        entrada (str): O simbolo a validar (esperado: 'X', 'O' ou ' ').

    Raises:
        ValueError: Se o argumento for invalido (ERRO_PECA).
    """
    if not (isinstance(entrada, str) and len(entrada) == 1 and entrada in ('X', 'O', ' ')):
        raise ValueError(ERRO_PECA)

def outro_jogador(jogador: str) -> str:
    """
    Devolve o simbolo do jogador adversario.

    Args:
        jogador (str): O jogador atual ('X' ou 'O').

    Returns:
        str: O jogador adversario ('O' ou 'X').
    """
    return 'O' if jogador == 'X' else 'X'

# -------------------------------------------------------------------------------------------------
# TAD posicao
# -------------------------------------------------------------------------------------------------
def cria_posicao(coluna: str, linha: str) -> tuple:
    """
    Construtor do TAD posicao.
    Valida os argumentos e devolve a posicao como um tuplo interno.

    Args:
        coluna (str): A componente coluna ('a', 'b' ou 'c').
        linha (str): A componente linha ('1', '2' ou '3').

    Returns:
        tuple: O TAD posicao (coluna, linha).

    Raises:
        ValueError: Se os argumentos forem invalidos (ERRO_POSICAO).
    """
    confirmar_posicao(coluna, linha)
    return coluna, linha

def cria_copia_posicao(posicao: tuple) -> tuple:
    """
    Cria uma copia de uma posicao (TAD).

    Args:
        posicao (tuple): O TAD posicao a copiar.

    Returns:
        tuple: Uma nova instancia do TAD posicao.
    """
    return posicao[0], posicao[1]

def obter_pos_c(posicao: tuple) -> str:
    """
    Seletor da coluna de uma posicao.

    Args:
        posicao (tuple): O TAD posicao.

    Returns:
        str: A componente coluna.
    """
    return posicao[0]


def obter_pos_l(posicao: tuple) -> str:
    """
    Seletor da linha de uma posicao.

    Args:
        posicao (tuple): O TAD posicao.

    Returns:
        str: A componente linha.
    """
    return posicao[1]

def eh_posicao(arg) -> bool:
    """
    Reconhecedor do TAD posicao. Verifica se o argumento e um TAD posicao valido.

    Args:
        arg (any): O argumento a testar.

    Returns:
        bool: True se 'arg' for um TAD posicao valido, False caso contrario.
    """
    return (
            isinstance(arg, tuple) and
            len(arg) == 2 and
            arg[0] in COLUNAS and
            arg[1] in LINHAS
    )

def posicoes_iguais(posicao_1, posicao_2) -> bool:
    """
    Testa se dois argumentos sao TADs posicao e se sao iguais.

    Args:
        posicao_1 (any): O primeiro argumento a testar.
        posicao_2 (any): O segundo argumento a testar.

    Returns:
        bool: True se posicao_1 e posicao_2 forem TADs posicao validos e iguais, False caso contrario.
    """
    return eh_posicao(posicao_1) and eh_posicao(posicao_2) and posicao_1 == posicao_2

def posicao_para_str(posicao: tuple) -> str:
    """
    Transformador: Converte o TAD posicao para a sua representacao externa (string).

    Args:
        posicao (tuple): O TAD posicao.

    Returns:
        str: A representacao em string (ex: 'a1').
    """
    return posicao[0] + posicao[1]

# -----------------------------------------------------------------------------------------------
# (2) Parsers de strings para posicao e movimento
# -----------------------------------------------------------------------------------------------
def str_para_posicao(entrada: str) -> tuple:
    """
    Converte uma string (ex: 'a1') num TAD posicao.
    Usado para ler a entrada do utilizador.

    Args:
        entrada (str): A string a converter.

    Returns:
        tuple: O TAD posicao correspondente.

    Raises:
        ValueError: Se a string nao for uma posicao valida (ERRO_JOGADA_MANUAL).
    """
    if len(entrada) == 2 and entrada[0] in COLUNAS and entrada[1] in LINHAS:
        return cria_posicao(entrada[0], entrada[1])
    raise ValueError(ERRO_JOGADA_MANUAL)

def str_para_movimento(entrada: str) -> tuple:
    """
    Converte uma string (ex: 'a1a2') num tuplo de TADs posicao (origem, destino).
    Usado para ler a entrada do utilizador na fase de movimento.

    Args:
        entrada (str): A string a converter (formato 'c1l1c2l2').

    Returns:
        tuple: Um tuplo (posicao_origem, posicao_destino).

    Raises:
        ValueError: Se a string nao for um movimento valido (ERRO_JOGADA_MANUAL).
    """
    if len(entrada) == 4 and all(entrada[i] in COLUNAS if i % 2 == 0 else entrada[i] in LINHAS for i in range(4)):
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(ERRO_JOGADA_MANUAL)

# -------------------------------------------------------------------------------------------------
# (4) TAD movimento (construtores e predicados)
# -------------------------------------------------------------------------------------------------
def cria_mov_colocacao(posicao: tuple) -> tuple:
    """Cria um movimento de colocacao (tuplo com 1 elemento)."""
    return (posicao,)

def cria_mov_passar(posicao: tuple) -> tuple:
    """Cria um movimento de passagem (origem e destino iguais)."""
    return posicao, posicao

def cria_movimento(pos_origem: tuple, pos_destino: tuple) -> tuple:
    """Cria um movimento real (origem e destino diferentes)."""
    return pos_origem, pos_destino

def eh_colocacao(movimento: tuple) -> bool:
    """Testa se um movimento e do tipo colocacao."""
    return len(movimento) == 1

def eh_passar(movimento: tuple) -> bool:
    """Testa se um movimento e do tipo passagem."""
    return len(movimento) == 2 and posicoes_iguais(movimento[0], movimento[1])

def eh_mov_real(movimento: tuple) -> bool:
    """Testa se um movimento e um movimento real (nao e passagem)."""
    return len(movimento) == 2 and not posicoes_iguais(movimento[0], movimento[1])

# --- Logica de Adjacencia ---
_LIGACOES = {
    'a1': ('b1', 'a2', 'b2'),
    'b1': ('a1', 'c1', 'b2'),
    'c1': ('b1', 'c2', 'b2'),
    'a2': ('a1', 'a3', 'b2'),
    'b2': ('a1', 'b1', 'c1', 'a2', 'c2', 'a3', 'b3', 'c3'),
    'c2': ('c1', 'c3', 'b2'),
    'a3': ('a2', 'b3', 'b2'),
    'b3': ('a3', 'c3', 'b2'),
    'c3': ('c2', 'b3', 'b2')
}

_ORDEM_LEITURA_MAP = {
    'a1': 0, 'b1': 1, 'c1': 2,
    'a2': 3, 'b2': 4, 'c2': 5,
    'a3': 6, 'b3': 7, 'c3': 8
}

def _chave_ordem_leitura(pos: tuple) -> int:
    """Funcao auxiliar usada como 'key' para ordenar posicoes pela ordem de leitura."""
    return _ORDEM_LEITURA_MAP[posicao_para_str(pos)]
  
def obter_posicoes_adjacentes(posicao: tuple) -> tuple:
    """
    Devolve um tuplo com as posicoes adjacentes a 'posicao', ordenadas
    de acordo com a ordem de leitura do tabuleiro (a1, b1, c1, ...).

    Args:
        posicao (tuple): O TAD posicao.

    Returns:
        tuple: Um tuplo de TADs posicao adjacentes.

    Raises:
        ValueError: Se a posicao nao for valida (erro interno).
    """
    if not eh_posicao(posicao):
        raise ValueError('obter_posicoes_adjacentes: posicao invalida')

    pos_str = posicao_para_str(posicao)
    adjacentes_str = _LIGACOES[pos_str]

    # Cria lista de TADs posicao
    lista_pos_adjacentes = []
    for s in adjacentes_str:
        lista_pos_adjacentes.append(cria_posicao(s[0], s[1]))

    # Ordena a lista de acordo com a ordem de leitura
    lista_pos_adjacentes.sort(key=_chave_ordem_leitura)

    return tuple(lista_pos_adjacentes)
# -------------------------------------------------------------------------------------------------
# TAD peca
# -------------------------------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    """
    Construtor do TAD peca.
    Valida o simbolo e devolve a peca (string interna).

    Args:
        entrada (str): O simbolo a criar ('X', 'O' ou ' ').

    Returns:
        str: O TAD peca.

    Raises:
        ValueError: Se o argumento for invalido (ERRO_PECA).
    """
    confirmar_peca(entrada)
    return entrada

def cria_copia_peca(peca: str) -> str:
    """
    Cria uma copia de uma peca (TAD).

    Args:
        peca (str): O TAD peca a copiar.

    Returns:
        str: Uma nova instancia do TAD peca.
    """
    return peca

def eh_peca(arg) -> bool:
    """
    Reconhecedor do TAD peca. Verifica se o argumento e um TAD peca valido.

    Args:
        arg (any): O argumento a testar.

    Returns:
        bool: True se 'arg' for um TAD peca valido, False caso contrario.
    """
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(peca1, peca2) -> bool:
    """
    Testa se dois argumentos sao TADs peca e se sao iguais.

    Args:
        peca1 (any): O primeiro argumento a testar.
        peca2 (any): O segundo argumento a testar.

    Returns:
        bool: True se p1 e p2 forem TADs peca validos e iguais, False caso contrario.
    """
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2

def peca_para_str(peca: str) -> str:
    """
    Transformador: Converte o TAD peca para a sua representacao externa (string).

    Args:
        peca (str): O TAD peca.

    Returns:
        str: A representacao em string (ex: '[X]').
    """
    return f'[{peca}]'

def peca_para_inteiro(peca: str) -> int:
    """
    Transformador: Converte o TAD peca para a sua representacao inteira (para IA).

    Args:
        peca (str): O TAD peca.

    Returns:
        int: 1 para 'X', -1 para 'O', 0 para ' '.
    """
    return 1 if peca == 'X' else (-1 if peca == 'O' else 0)

# -------------------------------------------------------------------------------------------------
# TAD tabuleiro
# -------------------------------------------------------------------------------------------------
def cria_tabuleiro() -> list:
    """
    Construtor do TAD tabuleiro.

    Returns:
        list: Um tabuleiro 3x3 (lista de listas) vazio.
    """
    return [[cria_peca(' ') for _ in COLUNAS] for _ in LINHAS]

def cria_copia_tabuleiro(tabuleiro: list) -> list:
    """
    Cria uma copia profunda de um tabuleiro (TAD).

    Args:
        tabuleiro (list): O TAD tabuleiro a copiar.

    Returns:
        list: Uma nova instancia do TAD tabuleiro.
    """
    return [linha[:] for linha in tabuleiro]

def _idx_from_pos(posicao: tuple) -> tuple:
    """Converte um TAD posicao em indices de matriz (linha, coluna)."""
    return LINHAS.index(obter_pos_l(posicao)), COLUNAS.index(obter_pos_c(posicao))

def obter_peca(tabuleiro: list, posicao: tuple) -> str:
    """
    Seletor: devolve a peca (TAD) numa dada posicao do tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        posicao (tuple): O TAD posicao.

    Returns:
        str: O TAD peca ('X', 'O' ou ' ') nessa posicao.
    """
    r, c = _idx_from_pos(posicao)
    return tabuleiro[r][c]

def obter_vetor(tabuleiro: list, entrada: str) -> tuple:
    """
    Seletor: Devolve um tuplo com as pecas de uma linha ou coluna.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        entrada (str): O identificador da coluna ('a', 'b', 'c') ou linha ('1', '2', '3').

    Returns:
        tuple: Um tuplo com os 3 TADs peca.
    """
    if entrada in COLUNAS:
        c = COLUNAS.index(entrada)
        return tuple(tabuleiro[r][c] for r in range(3))
    elif entrada in LINHAS:
        r = LINHAS.index(entrada)
        return tuple(tabuleiro[r][c] for c in range(3))
    else:
        raise ValueError("obter_vetor: seletor invalido (use 'a'..'c' ou '1'..'3')")

def coloca_peca(tabuleiro: list, jogador: str, posicao: tuple) -> list:
    """
    Modificador: Coloca uma peca numa posicao livre do tabuleiro.
    Modifica destrutivamente o tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca ('X' ou 'O').
        posicao (tuple): O TAD posicao onde colocar.

    Returns:
        list: O proprio tabuleiro, modificado.
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

def remove_peca(tabuleiro: list, posicao: tuple) -> list:
    """
    Modificador: Remove uma peca de uma posicao (coloca ' ').
    Modifica destrutivamente o tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        posicao (tuple): O TAD posicao de onde remover.

    Returns:
        list: O proprio tabuleiro, modificado.
    """
    r, c = _idx_from_pos(posicao)
    tabuleiro[r][c] = ' '
    return tabuleiro

def move_peca(tabuleiro: list, p_origem: tuple, p_destino: tuple) -> list:
    """
    Modificador: Move uma peca de p_origem para p_destino.
    Modifica destrutivamente o tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        p_origem (tuple): O TAD posicao de origem.
        p_destino (tuple): O TAD posicao de destino.

    Returns:
        list: O proprio tabuleiro, modificado.
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

def _tem_vencedor(tabuleiro: list, jogador: str) -> bool:
    """Verifica se um jogador tem uma linha vitoriosa (horizontal ou vertical)."""
    for (a, b, c) in LINHAS_VENCEDORAS:
        if tabuleiro[a[0]][a[1]] == jogador and tabuleiro[b[0]][b[1]] == jogador and tabuleiro[c[0]][c[1]] == jogador:
            return True
    return False

def eh_tabuleiro(arg) -> bool:
    """
    Reconhecedor do TAD tabuleiro. Verifica se o argumento e um TAD tabuleiro valido.
    Um tabuleiro valido obedece as regras (max 3 pecas, diferenca max 1, etc.).

    Args:
        arg (any): O argumento a testar.

    Returns:
        bool: True se 'arg' for um TAD tabuleiro valido, False caso contrario.
    """
    if not (isinstance(arg, list) and len(arg) == 3 and all(isinstance(l, list) and len(l) == 3 for l in arg)):
        return False
    pecas = [pos for linha in arg for pos in linha]
    if not all(eh_peca(pos) for pos in pecas):
        return False
    x = pecas.count('X')
    o = pecas.count('O')
    if x > 3 or o > 3 or abs(x - o) > 1:
        return False
    if _tem_vencedor(arg, 'X') and _tem_vencedor(arg, 'O'):
        return False
    return True

def eh_posicao_livre(tabuleiro: list, posicao: tuple) -> bool:
    """
    Testa se uma posicao especifica no tabuleiro esta livre (' ').

    Args:
        tabuleiro (list): O TAD tabuleiro.
        posicao (tuple): O TAD posicao a verificar.

    Returns:
        bool: True se a posicao estiver livre, False caso contrario.
    """
    return obter_peca(tabuleiro, posicao) == ' '

def tabuleiros_iguais(tabuleiro_1, tabuleiro_2) -> bool:
    """
    Testa se dois argumentos sao TADs tabuleiro e se sao iguais (peca a peca).

    Args:
        tabuleiro_1 (any): O primeiro argumento a testar.
        tabuleiro_2 (any): O segundo argumento a testar.

    Returns:
        bool: True se ambos forem tabuleiros validos e iguais, False caso contrario.
    """
    if not (eh_tabuleiro(tabuleiro_1) and eh_tabuleiro(tabuleiro_2)):
        return False
    return all(tabuleiro_1[r][c] == tabuleiro_2[r][c] for r in range(3) for c in range(3))

def tabuleiro_para_str(tabuleiro: list) -> str:
    """
    Transformador: Converte o TAD tabuleiro para a sua representacao externa.

    Args:
        tabuleiro (list): O TAD tabuleiro.

    Returns:
        str: A representacao em string do tabuleiro, com varias linhas.
    """

    def linha_str(i: int) -> str:
        return f"{LINHAS[i]} " + "-".join(peca_para_str(tabuleiro[i][j]) for j in range(3))

    return "\n".join([CABECALHO, linha_str(0), CONEXAO_1, linha_str(1), CONEXAO_2, linha_str(2)])


def tuplo_para_tabuleiro(tuplo_3x3: tuple) -> list:
    """
    Construtor: Cria um TAD tabuleiro a partir de um tuplo de tuplos 3x3
    contendo inteiros (1 para 'X', -1 para 'O', 0 para ' ').

    Args:
        tuplo_3x3 (tuple): O tuplo 3x3 de inteiros.

    Returns:
        list: O TAD tabuleiro correspondente.
    """
    # --- Validacoes minimas ---
    if not (isinstance(tuplo_3x3, tuple) and len(tuplo_3x3) == 3 and all(
            isinstance(l, tuple) and len(l) == 3 for l in tuplo_3x3)):
        raise ValueError("tuplo_para_tabuleiro: argumento deve ser um tuplo 3x3")
    valores_validos = {1, 0, -1}
    for r in range(3):
        for c in range(3):
            if tuplo_3x3[r][c] not in valores_validos:
                raise ValueError("tuplo_para_tabuleiro: valores invalidos (usar 1, 0, -1)")

    tabuleiro = cria_tabuleiro()
    for r in range(3):
        for c in range(3):
            val = tuplo_3x3[r][c]
            if val == 1:
                jogador = 'X'
            elif val == -1:
                jogador = 'O'
            else:
                jogador = ' '
            tabuleiro[r][c] = jogador
    return tabuleiro

def obter_ganhador(tabuleiro: list) -> str:
    """
    Funcao de alto nivel: Verifica se ha um ganhador no tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.

    Returns:
        str: O TAD peca do ganhador ('X' ou 'O'), ou ' ' se nao houver ganhador.
    """
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '

# -------------------------------------------------------------------------------------------------
# Funcoes auxiliares (ordem de leitura)
# -------------------------------------------------------------------------------------------------
def _iterador_posicoes_leitura():
    """Gera posicoes (TAD) na ordem de leitura do tabuleiro (a1, b1, c1, ...)."""
    for l in LINHAS:
        for c in COLUNAS:
            yield cria_posicao(c, l)


def obter_posicoes_livres(tabuleiro: list) -> tuple:
    """
    Funcao de alto nivel: Devolve as posicoes livres, pela ordem de leitura.

    Args:
        tabuleiro (list): O TAD tabuleiro.

    Returns:
        tuple: Um tuplo de TADs posicao livres.
    """
    return tuple(pos for pos in _iterador_posicoes_leitura() if eh_posicao_livre(tabuleiro, pos))

def obter_posicoes_jogador(tabuleiro: list, jogador: str) -> tuple:
    """
    Funcao de alto nivel: Devolve as posicoes ocupadas por um jogador,
    pela ordem de leitura.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador ('X' ou 'O').

    Returns:
        tuple: Um tuplo de TADs posicao ocupadas.
    """
    return tuple(pos for pos in _iterador_posicoes_leitura() if obter_peca(tabuleiro, pos) == jogador)

def _contar_pecas(tabuleiro: list) -> int:
    """Conta o numero total de pecas ('X' e 'O') no tabuleiro."""
    return sum(1 for pos in _iterador_posicoes_leitura() if obter_peca(tabuleiro, pos) != ' ')

def _esta_na_fase_colocacao(tabuleiro: list) -> bool:
    """
    Verifica se o jogo esta na fase de colocacao (menos de 6 pecas no total).

    Args:
        tabuleiro (list): O TAD tabuleiro.

    Returns:
        bool: True se estiver na fase de colocacao, False caso contrario.
    """
    return _contar_pecas(tabuleiro) < 6


def _posicoes_adjacentes_livres(tabuleiro: list, posicao: tuple) -> tuple:
    """Devolve um tuplo de posicoes adjacentes a 'posicao' que estao livres."""
    return tuple(p for p in obter_posicoes_adjacentes(posicao) if eh_posicao_livre(tabuleiro, p))

def _gerar_movimentos_validos(tabuleiro: list, jogador: str) -> tuple:
    """
    Gera todos os movimentos legais (origem, destino) para um jogador
    na fase de movimento. Inclui a jogada de "passar" (pos, pos)
    apenas se o jogador estiver bloqueado.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador.

    Returns:
        tuple: Um tuplo de movimentos validos (cada movimento e um tuplo de 2 posicoes).
    """
    jogadas = []
    for pos in obter_posicoes_jogador(tabuleiro, jogador):
        for adj in _posicoes_adjacentes_livres(tabuleiro, pos):
            jogadas.append((pos, adj))
    if not jogadas:
        posicoes_do_jogador = obter_posicoes_jogador(tabuleiro, jogador)
        if posicoes_do_jogador:
            jogadas.append((posicoes_do_jogador[0], posicoes_do_jogador[0]))  # passar
    return tuple(jogadas)

# -----------------------------------------------------------------------------------------------
# (3) Regra de "passar"
# -----------------------------------------------------------------------------------------------
def _verifica_se_pode_passar(tabuleiro: list, jogador: str) -> bool:
    """Verifica se o jogador esta totalmente bloqueado e, portanto, pode passar."""
    return not any(not posicoes_iguais(a, b) for (a, b) in _gerar_movimentos_validos(tabuleiro, jogador))

def jogada_valida(tabuleiro: list, jogador: str, p_origem: tuple, p_destino: tuple) -> bool:
    """
    Valida uma jogada de movimento (origem, destino) para o input manual.
    Verifica se a peca pertence ao jogador, se o destino e adjacente e livre,
    ou se e uma jogada de "passar" valida.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador.
        p_origem (tuple): O TAD posicao de origem.
        p_destino (tuple): O TAD posicao de destino.

    Returns:
        bool: True se a jogada for valida, False caso contrario.
    """
    if not (eh_posicao(p_origem) and eh_posicao(p_destino)):
        return False
    tem_propria = (obter_peca(tabuleiro, p_origem) == jogador)
    if posicoes_iguais(p_origem, p_destino):
        return tem_propria and _verifica_se_pode_passar(tabuleiro, jogador)
    return (tem_propria and p_destino in obter_posicoes_adjacentes(p_origem) and eh_posicao_livre(tabuleiro, p_destino))

# -------------------------------------------------------------------------------------------------
# I/O: obter_movimento_manual
# -------------------------------------------------------------------------------------------------
def obter_movimento_manual(tabuleiro: list, jogador: str) -> tuple:
    """
    Funcao de I/O. Pede ao utilizador humano uma jogada (colocacao ou movimento)
    e valida-a.

    Mostra "Turno do jogador. Escolha uma posicao: " ou
    "Turno do jogador. Escolha um movimento: ".

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador humano.

    Returns:
        tuple: Um tuplo de movimento (1 posicao para colocacao, 2 para movimento).

    Raises:
        ValueError: Se a jogada introduzida for invalida (ERRO_JOGADA_MANUAL).
    """
    if _esta_na_fase_colocacao(tabuleiro):
        sys.stdout.write('Turno do jogador. Escolha uma posicao: ')
        sys.stdout.flush()
        entrada = sys.stdin.readline().strip()
        try:
            pos = str_para_posicao(entrada)
        except ValueError:
            raise ValueError(ERRO_JOGADA_MANUAL)
        if eh_posicao_livre(tabuleiro, pos):
            return (pos,)
        raise ValueError(ERRO_JOGADA_MANUAL)

    sys.stdout.write('Turno do jogador. Escolha um movimento: ')
    sys.stdout.flush()
    entrada = sys.stdin.readline().strip()
    try:
        p_origem, p_destino = str_para_movimento(entrada)
    except ValueError:
        raise ValueError(ERRO_JOGADA_MANUAL)
    if jogada_valida(tabuleiro, jogador, p_origem, p_destino):
        return p_origem, p_destino
    raise ValueError(ERRO_JOGADA_MANUAL)

# -------------------------------------------------------------------------------------------------
# AI: colocacao
# -------------------------------------------------------------------------------------------------
def _obter_posicoes_canto() -> tuple:
    """Devolve um tuplo fixo com os TADs posicao dos 4 cantos."""
    return (cria_posicao('a', '1'), cria_posicao('c', '1'),
            cria_posicao('a', '3'), cria_posicao('c', '3'))

def _obter_posicoes_laterais() -> tuple:
    """Devolve um tuplo fixo com os TADs posicao das 4 laterais."""
    return (cria_posicao('b', '1'), cria_posicao('a', '2'),
            cria_posicao('c', '2'), cria_posicao('b', '3'))

def _encontrar_vitoria_colocacao(tabuleiro: list, jogador: str):
    """Encontra a primeira posicao livre (ordem de leitura) que resulta
    em vitoria imediata para o 'jogador'."""
    for pos in obter_posicoes_livres(tabuleiro):
        t_sim = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t_sim, jogador, pos)
        if obter_ganhador(t_sim) == jogador:
            return pos
    return None

def _encontrar_bloqueio_colocacao(tabuleiro: list, jogador: str):
    """Encontra a primeira posicao livre que bloqueia uma vitoria
    imediata do adversario."""
    adversario = outro_jogador(jogador)
    return _encontrar_vitoria_colocacao(tabuleiro, adversario)

# -------- Heuristica (nao usada, mas mantida por demonstracao) -------------------------------
def _existe_2_em_linha(tabuleiro: list, jogador: str) -> bool:
    """Retorna True se existir uma linha com exatamente 2 'jogador' e 1 vazia (sem oponente)."""
    adversario = outro_jogador(jogador)
    for (a, b, c) in LINHAS_VENCEDORAS:
        linha = [tabuleiro[a[0]][a[1]], tabuleiro[b[0]][b[1]], tabuleiro[c[0]][c[1]]]
        if linha.count(jogador) == 2 and linha.count(' ') == 1 and linha.count(adversario) == 0:
            return True
    return False

def _posicao_2_em_linha_segura(tabuleiro: list, jogador: str):
    """(HEURISTICA EXTRA, NAO USADA) Encontra uma posicao que cria 2-em-linha
    sem permitir que o oponente ganhe na proxima jogada."""
    adversario = outro_jogador(jogador)
    for pos in obter_posicoes_livres(tabuleiro):
        t_sim = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(t_sim, jogador, pos)
        if _existe_2_em_linha(t_sim, jogador):
            if _encontrar_vitoria_colocacao(t_sim, adversario) is None:
                return pos
    return None

# -------------------------------------------------------------------------------------------------
def _escolher_colocacao_ia(tabuleiro: list, jogador: str) -> tuple:
    """
    Calcula a jogada da IA para a fase de colocacao, seguindo a estrategia
    definida no enunciado (Vitoria -> Bloqueio -> Centro -> Canto -> Lateral).

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador (IA).

    Returns:
        tuple: Um tuplo de movimento (de 1 elemento) para a colocacao.
    """
    # 1. Vitoria
    posicao = _encontrar_vitoria_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)
    # 2. Bloqueio
    posicao = _encontrar_bloqueio_colocacao(tabuleiro, jogador)
    if posicao:
        return (posicao,)

    # 3. Centro
    b2 = cria_posicao('b', '2')
    if eh_posicao_livre(tabuleiro, b2):
        return (b2,)

    # Heuristica extra _posicao_2_em_linha_segura foi removida daqui
    # para seguir estritamente o enunciado.

    # 4. Canto vazio
    for pos_adjacente in _obter_posicoes_canto():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    # 5. Lateral vazio
    for pos_adjacente in _obter_posicoes_laterais():
        if eh_posicao_livre(tabuleiro, pos_adjacente):
            return (pos_adjacente,)

    # Fallback (caso de emergencia, improvavel)
    livres = obter_posicoes_livres(tabuleiro)
    return (livres[0],) if livres else (cria_posicao('a', '1'),)

# -------------------------------------------------------------------------------------------------
# AI: movimento (facil/normal/dificil)
# -------------------------------------------------------------------------------------------------
def _calcular_movimento_facil(tabuleiro: list, jogador: str) -> tuple:
    """
    Calcula a jogada da IA para o nivel 'facil'.
    E a primeira peca (ordem de leitura) que se pode mover para a sua
    primeira posicao adjacente livre (ordem de leitura).

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador (IA).

    Returns:
        tuple: Um tuplo de movimento (de 2 elementos).
    """
    for pos in obter_posicoes_jogador(tabuleiro, jogador):
        for adj in obter_posicoes_adjacentes(pos):
            if eh_posicao_livre(tabuleiro, adj):
                return pos, adj
    # Se bloqueado, passa (primeira peca)
    posicoes_do_jogador = obter_posicoes_jogador(tabuleiro, jogador)
    return (posicoes_do_jogador[0], posicoes_do_jogador[0]) if posicoes_do_jogador else (cria_posicao('a', '1'),cria_posicao('a', '1'))

def _encontrar_vitoria_movimento(tabuleiro: list, jogador: str):
    """
    Encontra o primeiro movimento (origem, destino) que resulta em
    vitoria imediata para o 'jogador'.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador (IA).

    Returns:
        tuple: O movimento vitorioso (origem, destino), ou None se nao existir.
    """
    for (pos_origem, pos_destino) in _gerar_movimentos_validos(tabuleiro, jogador):
        if posicoes_iguais(pos_origem, pos_destino):
            continue
        t_sim = cria_copia_tabuleiro(tabuleiro)
        move_peca(t_sim, pos_origem, pos_destino)
        if obter_ganhador(t_sim) == jogador:
            return pos_origem, pos_destino
    return None

def obter_movimento_auto(tabuleiro: list, jogador: str, nivel: str) -> tuple:
    """
    Funcao principal da IA. Escolhe um movimento (colocacao ou movimento)
    com base no nivel de dificuldade.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador (IA).
        nivel (str): A dificuldade ('facil', 'normal', 'dificil').

    Returns:
        tuple: O tuplo de movimento escolhido.
    """
    # Fase de Colocacao (logica e a mesma para todos os niveis)
    if _esta_na_fase_colocacao(tabuleiro):
        return _escolher_colocacao_ia(tabuleiro, jogador)

    # Fase de Movimento
    if nivel == 'facil':
        return _calcular_movimento_facil(tabuleiro, jogador)

    if nivel == 'normal':
        # 1. Tenta vitoria imediata (Minimax profundidade 1)
        movimento = _encontrar_vitoria_movimento(tabuleiro, jogador)
        # 2. Se nao, joga como 'facil'
        return movimento if movimento else _calcular_movimento_facil(tabuleiro, jogador)

    if nivel == 'dificil':
        # 3. Minimax com profundidade 5
        _, movimento = _algoritmo_minimax(tabuleiro, jogador, max_depth=5)
        # 4. Fallback (se minimax falhar)
        return movimento if movimento else _calcular_movimento_facil(tabuleiro, jogador)

    raise ValueError("obter_movimento_auto: nivel invalido")

# -------------------------------------------------------------------------------------------------
# Minimax (fase de movimento) com filtragem de ramos alpha-beta
# (Refatorado para funcoes privadas separada
# -------------------------------------------------------------------------------------------------
def _minimax_avaliacao(tabuleiro: list) -> int:
    """
    Avalia um estado final do tabuleiro para o Minimax.
    Devolve +1 para vitoria de 'X', -1 para vitoria de 'O', 0 para outros casos.

    Args:
        tabuleiro (list): O TAD tabuleiro a avaliar.

    Returns:
        int: A pontuacao (1, -1, ou 0).
    """
    ganhador = obter_ganhador(tabuleiro)
    if ganhador == 'X':
        return 1
    if ganhador == 'O':
        return -1
    return 0

def _minimax_ordenar_movs(tabuleiro: list, jogador: str, movimentos: tuple) -> tuple:
    """
    Ordena uma lista de movimentos, priorizando vitorias imediatas.
    Isto otimiza drasticamente os cortes alpha-beta.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O jogador a mover.
        movimentos (tuple): O tuplo de movimentos validos a ordenar.

    Returns:
        tuple: O tuplo de movimentos ordenado.
    """
    ganhos, restantes = [], []
    for (pos_origem, pos_destino) in movimentos:
        t_sim = cria_copia_tabuleiro(tabuleiro)
        if not posicoes_iguais(pos_origem, pos_destino):
            move_peca(t_sim, pos_origem, pos_destino)
        if obter_ganhador(t_sim) == jogador:
            ganhos.append((pos_origem, pos_destino))
        else:
            restantes.append((pos_origem, pos_destino))
    return tuple(ganhos + restantes)

def _minimax_recursivo(tabuleiro: list, jogador: str, depth: int, alpha: int, beta: int) -> tuple:
    """
    Funcao recursiva principal do Minimax com cortes alpha-beta.

    Args:
        tabuleiro (list): O estado atual do tabuleiro.
        jogador (str): O jogador com o turno atual ('X' ou 'O').
        depth (int): A profundidade restante da pesquisa.
        alpha (int): O melhor valor encontrado ate agora para o maximizador (X).
        beta (int): O pior valor encontrado ate agora para o minimizador (O).

    Returns:
        tuple (int, tuple | None): (pontuacao, melhor_movimento)
    """

    # 1. Condicao de paragem (estado terminal ou profundidade maxima)
    ganhador = obter_ganhador(tabuleiro)
    if ganhador != ' ' or depth == 0:
        return _minimax_avaliacao(tabuleiro), None

    # 2. Obter movimentos (e ordena-los para otimizar)
    movimentos = _gerar_movimentos_validos(tabuleiro, jogador)
    if not movimentos:
        # Sem movimentos, jogo empatado ou bloqueado
        return _minimax_avaliacao(tabuleiro), None

    movimentos = _minimax_ordenar_movs(tabuleiro, jogador, movimentos)

    # 3. Logica MAX (Jogador 'X')
    if jogador == 'X':
        melhor_resultado, melhor_movimento = -10, None
        for (pos_origem, pos_destino) in movimentos:
            t_sim = cria_copia_tabuleiro(tabuleiro)
            if not posicoes_iguais(pos_origem, pos_destino):
                move_peca(t_sim, pos_origem, pos_destino)

            # Chamada recursiva para o MIN
            resultado, _ = _minimax_recursivo(t_sim, outro_jogador(jogador), depth - 1, alpha, beta)

            if resultado > melhor_resultado:
                melhor_resultado, melhor_movimento = resultado, (pos_origem, pos_destino)
            alpha = max(alpha, resultado)  # Atualiza alpha
            if alpha >= beta:
                break  # Corte Beta
        return melhor_resultado, melhor_movimento

    # 4. Logica MIN (Jogador 'O')
    else:
        melhor_resultado, melhor_movimento = 10, None
        for (pos_origem, pos_destino) in movimentos:
            t_sim = cria_copia_tabuleiro(tabuleiro)
            if not posicoes_iguais(pos_origem, pos_destino):
                move_peca(t_sim, pos_origem, pos_destino)

            # Chamada recursiva para o MAX
            resultado, _ = _minimax_recursivo(t_sim, outro_jogador(jogador), depth - 1, alpha, beta)

            if resultado < melhor_resultado:
                melhor_resultado, melhor_movimento = resultado, (pos_origem, pos_destino)
            beta = min(beta, resultado)  # Atualiza beta
            if alpha >= beta:
                break  # Corte Alpha
        return melhor_resultado, melhor_movimento

def _algoritmo_minimax(tabuleiro: list, jogador_atual: str, max_depth: int = 5) -> tuple:
    """
    Ponto de entrada do Minimax. Inicia a busca recursiva.

    Args:
        tabuleiro (list): O estado atual do tabuleiro.
        jogador_atual (str): O jogador a fazer o movimento ('X' ou 'O').
        max_depth (int): A profundidade maxima da pesquisa.

    Returns:
        tuple (int, tuple | None): (pontuacao, melhor_movimento)
    """
    return _minimax_recursivo(tabuleiro, jogador_atual, max_depth, -10, 10)


# -------------------------------------------------------------------------------------------------
# Funcoes de aplicacao e ciclo do jogo
# -------------------------------------------------------------------------------------------------
def _executar_movimento(tabuleiro: list, jogador: str, movimento: tuple) -> list:
    """
    Aplica um movimento (colocacao ou fase de movimento) ao tabuleiro.
    Modifica destrutivamente o tabuleiro.

    Args:
        tabuleiro (list): O TAD tabuleiro.
        jogador (str): O TAD peca do jogador.
        movimento (tuple): O tuplo de movimento (1 ou 2 elementos).

    Returns:
        list: O proprio tabuleiro, modificado.
    """
    if _esta_na_fase_colocacao(tabuleiro):
        coloca_peca(tabuleiro, jogador, movimento[0])
    else:
        if eh_passar(movimento):
            pass  # Movimento de passar (p,p) nao altera o tabuleiro
        else:
            move_peca(tabuleiro, movimento[0], movimento[1])
    return tabuleiro


def moinho(jogador: str, nivel: str) -> str:
    """
    Funcao principal do jogo.
    Executa um jogo completo do Moinho (Humano vs Computador).

    Mostra "Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade <nivel>."
    Mostra "Turno do computador (<nivel>):"

    Args:
        jogador (str): A peca do jogador humano ('[X]' ou '[O]').
        nivel (str): O nivel de dificuldade ('facil', 'normal', 'dificil').

    Returns:
        str: A representacao string da peca ganhadora ('[X]' ou '[O]').

    Raises:
        ValueError: Se 'jogador' ou 'nivel' forem invalidos (ERRO_JOGO).
    """
    if not (
            isinstance(jogador, str) and jogador in ('[X]', '[O]') and
            isinstance(nivel, str) and nivel in ('facil', 'normal', 'dificil')):
        raise ValueError(ERRO_JOGO)

    humano = 'X' if jogador == '[X]' else 'O'
    cpu = outro_jogador(humano)

    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {nivel}.')
    tabuleiro = cria_tabuleiro()
    print(tabuleiro_para_str(tabuleiro))

    turno = 'X'  # 'X' comeca sempre
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

        # Proximo turno
        turno = outro_jogador(turno)

    return peca_para_str(obter_ganhador(tabuleiro))


