# -------------------------------------------------------------------------------------------------
# Constantes e mensagens
# -------------------------------------------------------------------------------------------------

COLS = ('a', 'b', 'c')
ROWS = ('1', '2', '3')
ERR_POS = 'cria_posicao: argumentos invalidos'
ERR_PIECE = 'cria_peca: argumento invalido'
ERR_MANUAL = 'obter_movimento_manual: escolha invalida'
ERR_MOINHO = 'moinho: argumentos invalidos'
# ASCII do tabuleiro
HEADER = '   a   b   c'
CONN1 = '   | \\ | / |'
CONN2 = '   | / | \\ |'
# Linhas vencedoras (horizontais e verticais)
WIN_LINES = (
    ((0,0), (0,1), (0,2)),
    ((1,0), (1,1), (1,2)),
    ((2,0), (2,1), (2,2)),
    ((0,0), (1,0), (2,0)),
    ((0,1), (1,1), (2,1)),
    ((0,2), (1,2), (2,2)),
)
