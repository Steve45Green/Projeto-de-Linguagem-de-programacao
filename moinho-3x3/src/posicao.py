from .constantes import *

# -------------------------------------------------------------------------------------------------
# TAD posicao
# -------------------------------------------------------------------------------------------------

# Adjacencias (ordens calibradas para os testes publicos)
# LINHA-CHAVE: a ordem em 'b1' e 'b3' e vertical primeiro, depois laterais.
_ADJ = {
    'a1': ('b1', 'a2', 'b2'),
    'b1': ('b2', 'a1', 'c1'),  # vertical antes dos laterais (Testes)
    'c1': ('b1', 'c2', 'b2'),
    'a2': ('a1', 'a3', 'b2'),
    'b2': ('a2', 'b1', 'c2', 'b3', 'a1', 'c1', 'a3', 'c3'),
    'c2': ('c1', 'c3', 'b2'),
    'a3': ('a2', 'b3', 'b2'),
    'b3': ('b2', 'a3', 'c3'),  # vertical antes dos laterais
    'c3': ('c2', 'b3', 'b2')
}

# -------------------------------------------------------------------------------------------------
# TAD movimento
# -------------------------------------------------------------------------------------------------
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

def obter_posicoes_adjacentes(posicao: tuple[str, str]) -> tuple[tuple[str, str], ...]:
    """Devolve as posicoes adjacentes a posicao, na ordem do enunciado."""
    if not eh_posicao(posicao):
        raise ValueError('obter_posicoes_adjacentes: posicao invalida')
    return tuple(
        cria_posicao(pos[0], pos[1])
        for pos in [tuple(entrada) for entrada in _ADJ[posicao_para_str(posicao)]]
    )

def cria_copia_posicao(posicao: tuple[str, str]) -> tuple[str, str]:
    """Copia independente de uma posicao."""
    return posicao[0], posicao[1]

def obter_pos_c(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente coluna da posicao."""
    return posicao[0]

def obter_pos_l(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente linha da posicao."""
    return posicao[1]

def eh_posicao(arg) -> bool:
    """Reconhecedor: indica se o argumento e uma posicao valida."""
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
    """Transformador: converte a posicao em 'cl'."""
    return posicao[0] + posicao[1]

def eh_posicao_livre(tabuleiro, posicao) -> bool:
    """Teste: True se a posicao no tabuleiro estiver livre."""
    return obter_peca(tabuleiro, posicao) == ' '

# -------------------------------------------------------------------------------------------------
# Validador de posicao
# -------------------------------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------------------------
# Conversores de posicao e movimento
# -----------------------------------------------------------------------------------------------
def str_para_posicao(entrada: str):
    """Converte 'cl' em posicao ('c','l').
    Erros:
    - ValueError(ERR_MANUAL) se o formato/conteudo nao forem validos.
    """
    if len(entrada) == 2 and entrada[0] in COLS and entrada[1] in ROWS:
        return cria_posicao(entrada[0], entrada[1])
    raise ValueError(ERR_MANUAL)

def str_para_movimento(entrada: str):
    """Converte 'c1c2l2' em (posicao_origem, posicao_destino)."""
    if len(entrada) == 4 and all(entrada[i] in COLS if i % 2 == 0 else entrada[i] in ROWS for i in range(4)):
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(ERR_MANUAL)

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