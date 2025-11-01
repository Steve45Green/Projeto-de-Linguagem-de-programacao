from .constantes import *
from .posicao import *
# -------------------------------------------------------------------------------------------------
# TAD peca
# -------------------------------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    """Construtor do TAD peca. Lanca ValueError(ERR_PIECE) se invalido."""
    confirmar_peca(entrada)
    return entrada

def _idx_from_pos(posicao: tuple[str, str]) -> tuple[int, int]:
    """Converte posicao (c,l) em indices (linha, coluna) na matriz 3x3."""
    return ROWS.index(obter_pos_l(posicao)), COLS.index(obter_pos_c(posicao))

def obter_peca(tabuleiro, posicao):
    """Seletor: devolve a peca na posicao."""
    r, c = _idx_from_pos(posicao)
    return tabuleiro[r][c]

def obter_pos_c(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente coluna da posicao."""
    return posicao[0]

def obter_pos_l(posicao: tuple[str, str]) -> str:
    """Seletor: devolve a componente linha da posicao."""
    return posicao[1]

def cria_copia_peca(jogador: str) -> str:
    """Copia independente de peca."""
    return jogador

def eh_peca(arg) -> bool:
    """Reconhecedor: True se o argumento for 'X', 'O' ou ' '."""
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(peca1: str, peca2: str) -> bool:
    """Teste: True se as duas pecas forem validas e iguais."""
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2

def peca_para_str(jogador: str) -> str:
    """Transformador: devolve '[X]', '[O]' ou '[ ]'."""
    return f'[{jogador}]'

def peca_para_inteiro(jogador: str) -> int:
    """Conversao de peca para inteiro: X->+1, O->-1, ' '->0."""
    return 1 if jogador == 'X' else (-1 if jogador == 'O' else 0)

def coloca_peca(tabuleiro, jogador: str, posicao):
    """Modificador: coloca a peca jogador na posicao posicao."""
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
    """Modificador: move a peca de p_origem para p_destino."""
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


# -------------------------------------------------------------------------------------------------
# Utilitarios de validacao
# -------------------------------------------------------------------------------------------------
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