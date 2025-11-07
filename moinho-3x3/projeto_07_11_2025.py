from typing import Tuple, List, Optional
from functools import reduce

# -------------------------------------------------------------------------------------------------
# Constantes e mensagens
# -------------------------------------------------------------------------------------------------
colunas = ('a', 'b', 'c')
linhas = ('1', '2', '3')
erro_posicao = 'cria_posicao: argumentos invalidos'
erro_peca = 'cria_peca: argumento invalido'
erro_movimento_manual = 'obter_movimento_manual: escolha invalida'
erro_moinho = 'moinho: argumentos invalidos'
# ASCII do tabuleiro
cabecalho = '   a   b   c'
conexao1 = '   | \\ | / |'
conexao2 = '   | / | \\ |'
# Linhas vencedoras (horizontais e verticais)
linhas_vencedoras = (
    ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
)
infinito = 10  # Constante para valores iniciais de alpha/beta no Minimax


# -------------------------------------------------------------------------------------------------
# Utilitarios de validacao
# -------------------------------------------------------------------------------------------------
def _validar_posicao(coluna: str, linha: str) -> None:
    """Verifica se a coluna e a linha fornecidas sao validas para uma posicao no tabuleiro.

    Args:
        coluna (str): A coluna da posicao ('a', 'b' ou 'c').
        linha (str): A linha da posicao ('1', '2' ou '3').

    Raises:
        ValueError: Se os argumentos nao forem validos.
    """
    if not (isinstance(coluna, str) and isinstance(linha, str) and coluna in colunas and linha in linhas):
        raise ValueError(erro_posicao)


def _validar_peca(entrada: str) -> None:
    """Verifica se a entrada representa uma peca valida.

    Args:
        entrada (str): O identificador da peca ('X', 'O' ou ' ').

    Raises:
        ValueError: Se o argumento nao for valido.
    """
    if not (isinstance(entrada, str) and len(entrada) == 1 and entrada in ('X', 'O', ' ')):
        raise ValueError(erro_peca)


def _obter_adversario(jogador: str) -> str:
    """Retorna o identificador do adversario do jogador dado.

    Args:
        jogador (str): O identificador do jogador atual ('X' ou 'O').

    Returns:
        str: O identificador do adversario.
    """
    return 'O' if jogador == 'X' else 'X'


# -------------------------------------------------------------------------------------------------
# TAD posicao
# -------------------------------------------------------------------------------------------------
adjacencias = {
    'a1': ('b1', 'a2', 'b2'), 'b1': ('a1', 'c1', 'b2'), 'c1': ('b1', 'b2', 'c2'),
    'a2': ('a1', 'a3', 'b2'), 'b2': ('a1', 'a2', 'a3', 'b1', 'b3', 'c1', 'c2', 'c3'),
    'c2': ('c1', 'b2', 'c3'), 'a3': ('a2', 'b2', 'b3'), 'b3': ('a3', 'b2', 'c3'),
    'c3': ('b2', 'c2', 'b3')
}


def _indice_posicao_leitura(posicao: Tuple[str, str]) -> int:
    """Calcula o indice de leitura da posicao para ordenacao.

    Args:
        posicao (Tuple[str, str]): A posicao (coluna, linha).

    Returns:
        int: O indice calculado.
    """
    return linhas.index(posicao[1]) * 3 + colunas.index(posicao[0])


def cria_posicao(coluna: str, linha: str) -> Tuple[str, str]:
    """Cria uma nova posicao no tabuleiro.

    Args:
        coluna (str): A coluna da posicao ('a', 'b' ou 'c').
        linha (str): A linha da posicao ('1', '2' ou '3').

    Returns:
        Tuple[str, str]: A posicao criada.

    Raises:
        ValueError: Se os argumentos nao forem validos.
    """
    _validar_posicao(coluna, linha)
    return coluna, linha


def cria_copia_posicao(posicao: Tuple[str, str]) -> Tuple[str, str]:
    """Cria uma copia de uma posicao existente.

    Args:
        posicao (Tuple[str, str]): A posicao a copiar.

    Returns:
        Tuple[str, str]: A copia da posicao.
    """
    return posicao


def obter_pos_c(posicao: Tuple[str, str]) -> str:
    """Obtem a coluna de uma posicao.

    Args:
        posicao (Tuple[str, str]): A posicao.

    Returns:
        str: A coluna da posicao.
    """
    return posicao[0]


def obter_pos_l(posicao: Tuple[str, str]) -> str:
    """Obtem a linha de uma posicao.

    Args:
        posicao (Tuple[str, str]): A posicao.

    Returns:
        str: A linha da posicao.
    """
    return posicao[1]


def eh_posicao(arg) -> bool:
    """Verifica se o argumento e uma posicao valida.

    Args:
        arg: O argumento a verificar.

    Returns:
        bool: True se for uma posicao, False caso contrario.
    """
    return isinstance(arg, tuple) and len(arg) == 2 and arg[0] in colunas and arg[1] in linhas


def posicoes_iguais(posicao1, posicao2) -> bool:
    """Verifica se duas posicoes sao iguais.

    Args:
        posicao1 (Tuple[str, str]): Primeira posicao.
        posicao2 (Tuple[str, str]): Segunda posicao.

    Returns:
        bool: True se as posicoes forem iguais, False caso contrario.
    """
    return eh_posicao(posicao1) and eh_posicao(posicao2) and posicao1 == posicao2


def posicao_para_str(posicao: Tuple[str, str]) -> str:
    """Converte uma posicao para uma cadeia de caracteres.

    Args:
        posicao (Tuple[str, str]): A posicao.

    Returns:
        str: A representacao em cadeia de caracteres da posicao (ex: 'a1').
    """
    return ''.join(posicao)


def obter_posicoes_adjacentes(posicao: Tuple[str, str]) -> Tuple[Tuple[str, str], ...]:
    """Obtem as posicoes adjacentes a uma dada posicao.

    Args:
        posicao (Tuple[str, str]): A posicao de referencia.

    Returns:
        Tuple[Tuple[str, str], ...]: Tuplo de posicoes adjacentes ordenadas.
    """
    adj_strs = adjacencias[posicao_para_str(posicao)]
    return tuple(sorted((cria_posicao(p[0], p[1]) for p in adj_strs), key=_indice_posicao_leitura))


# -------------------------------------------------------------------------------------------------
# TAD peca
# -------------------------------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    """Cria uma nova peca.

    Args:
        entrada (str): O identificador da peca ('X', 'O' ou ' ').

    Returns:
        str: A peca criada.

    Raises:
        ValueError: Se o argumento nao for valido.
    """
    _validar_peca(entrada)
    return entrada


def cria_copia_peca(peca: str) -> str:
    """Cria uma copia de uma peca existente.

    Args:
        peca (str): A peca a copiar.

    Returns:
        str: A copia da peca.
    """
    return peca


def eh_peca(arg) -> bool:
    """Verifica se o argumento e uma peca valida.

    Args:
        arg: O argumento a verificar.

    Returns:
        bool: True se for uma peca, False caso contrario.
    """
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')


def pecas_iguais(peca1: str, peca2: str) -> bool:
    """Verifica se duas pecas sao iguais.

    Args:
        peca1 (str): Primeira peca.
        peca2 (str): Segunda peca.

    Returns:
        bool: True se as pecas forem iguais, False caso contrario.
    """
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2


def peca_para_str(peca: str) -> str:
    """Converte uma peca para uma cadeia de caracteres representativa.

    Args:
        peca (str): A peca.

    Returns:
        str: A representacao em cadeia de caracteres (ex: '[X]').
    """
    return f'[{peca}]'


def peca_para_inteiro(peca: str) -> int:
    """Converte uma peca para um valor inteiro.

    Args:
        peca (str): A peca.

    Returns:
        int: 1 para 'X', -1 para 'O', 0 para ' '.
    """
    return {'X': 1, 'O': -1, ' ': 0}[peca]


# -------------------------------------------------------------------------------------------------
# TAD tabuleiro
# -------------------------------------------------------------------------------------------------
def cria_tabuleiro() -> List[List[str]]:
    """Cria um novo tabuleiro vazio.

    Returns:
        List[List[str]]: O tabuleiro criado.
    """
    return [[' ' for _ in range(3)] for _ in range(3)]


def cria_copia_tabuleiro(tabuleiro: List[List[str]]) -> List[List[str]]:
    """Cria uma copia de um tabuleiro existente.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro a copiar.

    Returns:
        List[List[str]]: A copia do tabuleiro.
    """
    return [row[:] for row in tabuleiro]


def _indice(posicao: Tuple[str, str]) -> Tuple[int, int]:
    """Calcula os indices de linha e coluna para uma posicao.

    Args:
        posicao (Tuple[str, str]): A posicao.

    Returns:
        Tuple[int, int]: Os indices (linha, coluna).
    """
    return int(posicao[1]) - 1, ord(posicao[0]) - ord('a')


def obter_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> str:
    """Obtem a peca em uma posicao especifica do tabuleiro.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): A posicao.

    Returns:
        str: A peca na posicao.
    """
    r, c = _indice(posicao)
    return tabuleiro[r][c]


def obter_vetor(tabuleiro: List[List[str]], seletor: str) -> Tuple[str, ...]:
    """Obtem um vetor de pecas de uma linha ou coluna.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        seletor (str): A linha ou coluna a obter.

    Returns:
        Tuple[str, ...]: O tuplo de pecas.

    Raises:
        ValueError: Se o seletor for invalido.
    """
    if seletor in colunas:
        c = ord(seletor) - ord('a')
        return tuple(tabuleiro[r][c] for r in range(3))
    elif seletor in linhas:
        r = int(seletor) - 1
        return tuple(tabuleiro[r])
    raise ValueError('obter_vetor: argumento invalido')


def coloca_peca(tabuleiro: List[List[str]], peca: str, posicao: Tuple[str, str]) -> List[List[str]]:
    """Coloca uma peca em uma posicao do tabuleiro.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        peca (str): A peca a colocar.
        posicao (Tuple[str, str]): A posicao.

    Returns:
        List[List[str]]: O tabuleiro modificado.
    """
    r, c = _indice(posicao)
    tabuleiro[r][c] = peca
    return tabuleiro


def remove_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> List[List[str]]:
    """Remove uma peca de uma posicao do tabuleiro.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): A posicao.

    Returns:
        List[List[str]]: O tabuleiro modificado.
    """
    r, c = _indice(posicao)
    tabuleiro[r][c] = ' '
    return tabuleiro


def move_peca(tabuleiro: List[List[str]], posicao_origem: Tuple[str, str], posicao_destino: Tuple[str, str]) -> List[
    List[str]]:
    """Move uma peca de uma posicao de origem para destino.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao_origem (Tuple[str, str]): A posicao de origem.
        posicao_destino (Tuple[str, str]): A posicao de destino.

    Returns:
        List[List[str]]: O tabuleiro modificado.
    """
    peca = obter_peca(tabuleiro, posicao_origem)
    remove_peca(tabuleiro, posicao_origem)
    coloca_peca(tabuleiro, peca, posicao_destino)
    return tabuleiro


def eh_tabuleiro(arg) -> bool:
    """Verifica se o argumento e um tabuleiro valido.

    Args:
        arg: O argumento a verificar.

    Returns:
        bool: True se for um tabuleiro valido, False caso contrario.
    """
    if not (isinstance(arg, list) and len(arg) == 3 and all(
            isinstance(r, list) and len(r) == 3 and all(eh_peca(p) for p in r) for r in arg)):
        return False
    pieces = reduce(list.__add__, arg)
    count_x, count_o = pieces.count('X'), pieces.count('O')
    if count_x > 3 or count_o > 3 or abs(count_x - count_o) > 1:
        return False
    winner_x = _tem_vencedor(arg, 'X')
    winner_o = _tem_vencedor(arg, 'O')
    return not (winner_x and winner_o)


def eh_posicao_livre(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> bool:
    """Verifica se uma posicao no tabuleiro esta livre.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): A posicao.

    Returns:
        bool: True se a posicao estiver livre, False caso contrario.
    """
    return obter_peca(tabuleiro, posicao) == ' '


def tabuleiros_iguais(tabuleiro1: List[List[str]], tabuleiro2: List[List[str]]) -> bool:
    """Verifica se dois tabuleiros sao iguais.

    Args:
        tabuleiro1 (List[List[str]]): Primeiro tabuleiro.
        tabuleiro2 (List[List[str]]): Segundo tabuleiro.

    Returns:
        bool: True se os tabuleiros forem iguais, False caso contrario.
    """
    return tabuleiro1 == tabuleiro2


def tabuleiro_para_str(tabuleiro: List[List[str]]) -> str:
    """Converte um tabuleiro para uma representacao em cadeia de caracteres.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.

    Returns:
        str: A cadeia de caracteres representando o tabuleiro.
    """
    linhas_tabuleiro = [f'{linhas[r]} ' + '-'.join(peca_para_str(tabuleiro[r][c]) for c in range(3)) for r in range(3)]
    return '\n'.join([cabecalho, linhas_tabuleiro[0], conexao1, linhas_tabuleiro[1], conexao2, linhas_tabuleiro[2]])


def tuplo_para_tabuleiro(tuplo: Tuple[Tuple[int, ...], ...]) -> List[List[str]]:
    """Converte um tuplo de inteiros para um tabuleiro.

    Args:
        tuplo (Tuple[Tuple[int, ...], ...]): O tuplo representando o tabuleiro.

    Returns:
        List[List[str]]: O tabuleiro criado.

    Raises:
        ValueError: Se o tuplo for invalido.
    """
    if not (isinstance(tuplo, tuple) and len(tuplo) == 3 and all(
            isinstance(l, tuple) and len(l) == 3 and all(v in (1, 0, -1) for v in l) for l in tuplo)):
        raise ValueError('tuplo_para_tabuleiro: argumento invalido')
    tabuleiro = cria_tabuleiro()
    for r in range(3):
        for c in range(3):
            v = tuplo[r][c]
            if v != 0:
                coloca_peca(tabuleiro, 'X' if v == 1 else 'O', cria_posicao(colunas[c], linhas[r]))
    return tabuleiro


def _tem_vencedor(tabuleiro: List[List[str]], jogador: str) -> bool:
    """Verifica se um jogador tem uma linha vencedora.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador a verificar.

    Returns:
        bool: True se o jogador tiver vencido, False caso contrario.
    """
    for linha_vencedora in linhas_vencedoras:
        if all(obter_peca(tabuleiro, cria_posicao(colunas[c], linhas[r])) == jogador for r, c in linha_vencedora):
            return True
    return False


def obter_ganhador(tabuleiro: List[List[str]]) -> str:
    """Obtem o ganhador do jogo, se houver.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.

    Returns:
        str: O jogador vencedor ('X', 'O') ou ' ' se nao houver vencedor.
    """
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '


def obter_posicoes_livres(tabuleiro: List[List[str]]) -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes livres no tabuleiro.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.

    Returns:
        Tuple[Tuple[str, str], ...]: Tuplo de posicoes livres.
    """
    return tuple(pos for pos in _todas_posicoes() if eh_posicao_livre(tabuleiro, pos))


def obter_posicoes_jogador(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes ocupadas por um jogador.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador.

    Returns:
        Tuple[Tuple[str, str], ...]: Tuplo de posicoes do jogador.
    """
    return tuple(pos for pos in _todas_posicoes() if obter_peca(tabuleiro, pos) == jogador)


def _todas_posicoes() -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes possiveis no tabuleiro.

    Returns:
        Tuple[Tuple[str, str], ...]: Tuplo de todas as posicoes.
    """
    return tuple(cria_posicao(c, l) for l in linhas for c in colunas)


# -------------------------------------------------------------------------------------------------
# Funcoes adicionais
# -------------------------------------------------------------------------------------------------
def _analisar_entrada(entrada: str) -> Tuple[Tuple[str, str], ...]:
    """Analisa a entrada do utilizador para obter posicoes.

    Args:
        entrada (str): A entrada do utilizador.

    Returns:
        Tuple[Tuple[str, str], ...]: Tuplo de posicoes analisadas.

    Raises:
        ValueError: Se a entrada for invalida.
    """
    if len(entrada) == 2:
        return (cria_posicao(entrada[0], entrada[1]),)
    if len(entrada) == 4:
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(erro_movimento_manual)


def obter_movimento_manual(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    """Obtem o movimento manual do jogador humano.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro atual.
        jogador (str): O jogador atual.

    Returns:
        Tuple[Tuple[str, str], ...]: O movimento (posicao ou origem/destino).

    Raises:
        ValueError: Se a escolha for invalida.
    """
    import sys
    mensagem = 'Turno do jogador. Escolha uma ' + ('posicao' if _fase_colocacao(tabuleiro) else 'movimento') + ': '
    print(mensagem, end='')
    entrada = sys.stdin.readline().strip().lower()
    movimento = _analisar_entrada(entrada)
    if len(movimento) == 1:
        if not _fase_colocacao(tabuleiro) or not eh_posicao_livre(tabuleiro, movimento[0]):
            raise ValueError(erro_movimento_manual)
        return movimento
    pos_origem, pos_destino = movimento
    if obter_peca(tabuleiro, pos_origem) != jogador or (not posicoes_iguais(pos_origem, pos_destino) and (
            obter_peca(tabuleiro, pos_destino) != ' ' or pos_destino not in obter_posicoes_adjacentes(pos_origem))):
        raise ValueError(erro_movimento_manual)
    if posicoes_iguais(pos_origem, pos_destino) and any(
            eh_posicao_livre(tabuleiro, adj) for pos in obter_posicoes_jogador(tabuleiro, jogador) for adj in
            obter_posicoes_adjacentes(pos)):
        raise ValueError(erro_movimento_manual)
    return movimento


def _fase_colocacao(tabuleiro: List[List[str]]) -> bool:
    """Verifica se o jogo esta na fase de colocacao.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.

    Returns:
        bool: True se estiver na fase de colocacao, False caso contrario.
    """
    return len(obter_posicoes_jogador(tabuleiro, 'X')) < 3 or len(obter_posicoes_jogador(tabuleiro, 'O')) < 3


def _encontrar_posicao(tabuleiro: List[List[str]], jogador: str, predicado) -> Optional[Tuple[str, str]]:
    """Encontra uma posicao baseada num predicado.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador.
        predicado: A funcao predicado para testar.

    Returns:
        Optional[Tuple[str, str]]: A posicao encontrada ou None.
    """
    for pos in obter_posicoes_livres(tabuleiro):
        tab_copia = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(tab_copia, jogador, pos)
        if predicado(tab_copia):
            return pos
    return None


def _posicao_vitoria(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    """Encontra uma posicao que resulta em vitoria para o jogador.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador.

    Returns:
        Optional[Tuple[str, str]]: A posicao de vitoria ou None.
    """
    return _encontrar_posicao(tabuleiro, jogador, lambda tc: obter_ganhador(tc) == jogador)


def _posicao_bloqueio(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    """Encontra uma posicao que bloqueia a vitoria do adversario.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador.

    Returns:
        Optional[Tuple[str, str]]: A posicao de bloqueio ou None.
    """
    return _posicao_vitoria(tabuleiro, _obter_adversario(jogador))


def obter_movimento_auto(tabuleiro: List[List[str]], jogador: str, nivel: str) -> Tuple[Tuple[str, str], ...]:
    """Obtem o movimento automatico do computador baseado no nivel de dificuldade.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro atual.
        jogador (str): O jogador (computador).
        nivel (str): O nivel de dificuldade ('facil', 'normal', 'dificil').

    Returns:
        Tuple[Tuple[str, str], ...]: O movimento calculado.
    """
    if _fase_colocacao(tabuleiro):
        pos = _posicao_vitoria(tabuleiro, jogador) or _posicao_bloqueio(tabuleiro, jogador)
        if pos:
            return (pos,)
        centro = cria_posicao('b', '2')
        if eh_posicao_livre(tabuleiro, centro):
            return (centro,)
        for canto in (cria_posicao('a', '1'), cria_posicao('c', '1'), cria_posicao('a', '3'), cria_posicao('c', '3')):
            if eh_posicao_livre(tabuleiro, canto):
                return (canto,)
        for lateral in (cria_posicao('b', '1'), cria_posicao('a', '2'), cria_posicao('c', '2'), cria_posicao('b', '3')):
            if eh_posicao_livre(tabuleiro, lateral):
                return (lateral,)
        return (obter_posicoes_livres(tabuleiro)[0],)
    movimentos = [(pos, adj) for pos in obter_posicoes_jogador(tabuleiro, jogador) for adj in
                  obter_posicoes_adjacentes(pos) if eh_posicao_livre(tabuleiro, adj)]
    if not movimentos:
        return (obter_posicoes_jogador(tabuleiro, jogador)[0],) * 2
    if nivel == 'facil':
        return movimentos[0]
    if nivel == 'normal':
        for mov in movimentos:
            tab_copia = cria_copia_tabuleiro(tabuleiro)
            move_peca(tab_copia, mov[0], mov[1])
            if obter_ganhador(tab_copia) == jogador:
                return mov
        return movimentos[0]
    if nivel == 'dificil':
        _, mov = _minimax(tabuleiro, jogador, 5, -infinito, infinito, jogador == 'X')
        return mov or movimentos[0]


def _avaliar_tabuleiro(tabuleiro: List[List[str]]) -> int:
    """Avalia o estado do tabuleiro.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.

    Returns:
        int: Valor de avaliacao (1 para 'X' vencedor, -1 para 'O', 0 caso contrario).
    """
    ganhador = obter_ganhador(tabuleiro)
    return 1 if ganhador == 'X' else -1 if ganhador == 'O' else 0


def _ordenar_movimentos(tabuleiro: List[List[str]], jogador: str,
                        movimentos: Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]) -> Tuple[
    Tuple[Tuple[str, str], Tuple[str, str]], ...]:
    """Ordena movimentos priorizando os que levam a vitoria.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador.
        movimentos (Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]): Os movimentos.

    Returns:
        Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]: Movimentos ordenados.
    """
    movs_ganho, movs_restantes = [], []
    for mov in movimentos:
        tab_sim = cria_copia_tabuleiro(tabuleiro)
        move_peca(tab_sim, mov[0], mov[1])
        if obter_ganhador(tab_sim) == jogador:
            movs_ganho.append(mov)
        else:
            movs_restantes.append(mov)
    return tuple(movs_ganho + movs_restantes)


def _minimax(tabuleiro: List[List[str]], jogador: str, profundidade: int, alpha: int, beta: int, maximizando: bool) -> \
Tuple[int, Optional[Tuple[Tuple[str, str], Tuple[str, str]]]]:
    """Implementa o algoritmo Minimax com poda alpha-beta.

    Args:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): O jogador atual.
        profundidade (int): Profundidade restante.
        alpha (int): Valor alpha.
        beta (int): Valor beta.
        maximizando (bool): True se maximizando, False se minimizando.

    Returns:
        Tuple[int, Optional[Tuple[Tuple[str, str], Tuple[str, str]]]]: (valor, melhor movimento).
    """
    if obter_ganhador(tabuleiro) != ' ' or profundidade == 0:
        return _avaliar_tabuleiro(tabuleiro), None
    movimentos = [(pos, adj) for pos in obter_posicoes_jogador(tabuleiro, jogador) for adj in
                  obter_posicoes_adjacentes(pos) if eh_posicao_livre(tabuleiro, adj)]
    if not movimentos:
        return _avaliar_tabuleiro(tabuleiro), None
    movimentos = _ordenar_movimentos(tabuleiro, jogador, tuple(movimentos))
    melhor_valor = -infinito if maximizando else infinito
    melhor_movimento = None
    adversario = _obter_adversario(jogador)
    for mov in movimentos:
        tab_sim = cria_copia_tabuleiro(tabuleiro)
        move_peca(tab_sim, mov[0], mov[1])
        valor, _ = _minimax(tab_sim, adversario, profundidade - 1, alpha, beta, not maximizando)
        if (maximizando and valor > melhor_valor) or (not maximizando and valor < melhor_valor):
            melhor_valor, melhor_movimento = valor, mov
        if maximizando:
            alpha = max(alpha, valor)
        else:
            beta = min(beta, valor)
        if alpha >= beta:
            break
    return melhor_valor, melhor_movimento


def moinho(jogador_str: str, nivel_dificuldade: str) -> str:
    """Funcao principal para jogar o jogo do moinho.

    Args:
        jogador_str (str): Representacao da peca do jogador humano ('[X]' ou '[O]').
        nivel_dificuldade (str): Nivel de dificuldade ('facil', 'normal', 'dificil').

    Returns:
        str: Representacao da peca vencedora.

    Raises:
        ValueError: Se os argumentos forem invalidos.
    """
    if jogador_str not in ('[X]', '[O]') or nivel_dificuldade not in ('facil', 'normal', 'dificil'):
        raise ValueError(erro_moinho)
    humano = 'X' if jogador_str == '[X]' else 'O'
    computador = _obter_adversario(humano)
    print(f'Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade {nivel_dificuldade}.')
    tabuleiro = cria_tabuleiro()
    print(tabuleiro_para_str(tabuleiro))
    turno_atual = 'X'
    while obter_ganhador(tabuleiro) == ' ':
        if turno_atual == humano:
            movimento = obter_movimento_manual(tabuleiro, humano)
        else:
            print(f'Turno do computador ({nivel_dificuldade}):')
            movimento = obter_movimento_auto(tabuleiro, computador, nivel_dificuldade)
        if len(movimento) == 1:
            coloca_peca(tabuleiro, turno_atual, movimento[0])
        elif not posicoes_iguais(movimento[0], movimento[1]):
            move_peca(tabuleiro, movimento[0], movimento[1])
        print(tabuleiro_para_str(tabuleiro))
        turno_atual = _obter_adversario(turno_atual)
    return peca_para_str(obter_ganhador(tabuleiro))