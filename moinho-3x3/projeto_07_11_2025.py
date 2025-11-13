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
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
)
infinito = 10  # Valor simbolico para inicializacao de alpha/beta no algoritmo Minimax
# -------------------------------------------------------------------------------------------------
# Utilitarios de validacao
# -------------------------------------------------------------------------------------------------
def _validar_posicao(coluna: str, linha: str) -> None:
    """Verifica se a coluna e a linha fornecidas representam uma posicao valida no tabuleiro.
    Argumentos:
        coluna (str): Letra da coluna ('a', 'b' ou 'c').
        linha (str): N?mero da linha ('1', '2' ou '3').
    Excecoes:
        ValueError: E gerado se a coluna ou a linha nao forem validas.
    """
    if not (isinstance(coluna, str) and isinstance(linha, str) and coluna in colunas and linha in linhas):
        raise ValueError(erro_posicao)

def _validar_peca(entrada: str) -> None:
    """Verifica se simbolo fornecido representa uma peca valida do jogo.
    Argumentos:
        entrada (str): Caracter que identifica a peca ('X', 'O' ou '').
    Excecoes:
        ValueError: Da erro se o argumento nao corresponder a uma peca valida.
    """
    if not (isinstance(entrada, str) and len(entrada) == 1 and entrada in ('X', 'O', ' ')):
        raise ValueError(erro_peca)

def _obter_adversario(jogador: str) -> str:
    """Devolve o identificador do adversario do jogador indicado.
    Argumentos:
        jogador (str): Identificador do jogador atual ('X' ou 'O').
    Retorna:
        str: O identificador do adversario ('O' se o jogador for 'X', e vice-versa).
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
    """Calcula o indice de leitura de uma posicao, usado para efeitos de ordenacao.
    Argumentos:
        posicao (Tuple[str, str]): A posi??o (coluna, linha).
    Retorna:
        int: Indice numerico associado a posicao.
    """
    return linhas.index(posicao[1]) * 3 + colunas.index(posicao[0])

def cria_posicao(coluna: str, linha: str) -> Tuple[str, str]:
    """Cria uma nova posicao valida no tabuleiro.
    Argumentos:
        coluna (str): Letra da coluna ('a', 'b' ou 'c').
        linha (str): Numero da linha ('1', '2' ou '3').
    Retorna:
        Tuple[str, str]: A posicao criada no formato (coluna, linha).
    Exce??es:
        ValueError:E gerada se os argumentos nao forem validos.
    """
    _validar_posicao(coluna, linha)
    return coluna, linha

def cria_copia_posicao(posicao: Tuple[str, str]) -> Tuple[str, str]:
    """Cria uma copia independente de uma posicao existente.
    Argumentos:
        posicao (Tuple[str, str]): A posicao a copiar.
    Retorna:
        Tuple[str, str]: Uma copia da posicao fornecida.
    """
    return posicao

def obter_pos_c(posicao: Tuple[str, str]) -> str:
    """Devolve a coluna correspondente a uma posicao.
    Argumentos:
        posicao (Tuple[str, str]): A posicao a analisar.
    Retorna:
        str: A coluna da posicao ('a', 'b' ou 'c').
    """
    return posicao[0]

def obter_pos_l(posicao: Tuple[str, str]) -> str:
    """Devolve a linha correspondente a uma posicao.
    Argumentos:
        posicao (Tuple[str, str]): A posicao a analisar.
    Retorna:
        str: A linha da posicao ('1', '2' ou '3').
    """
    return posicao[1]

def eh_posicao(arg) -> bool:
    """Verifica se o argumento corresponde a uma posicao valida do tabuleiro.
    Argumentos:
        arg: O valor a verificar.
    Retorna:
        bool: True se for uma posicao valida, False, caso contrario.
    """
    return isinstance(arg, tuple) and len(arg) == 2 and arg[0] in colunas and arg[1] in linhas

def posicoes_iguais(posicao1, posicao2) -> bool:
    """Verifica se duas posicoes s?o exatamente iguais.
    Argumentos:
        posicao1 (Tuple[str, str]): Primeira posicao.
        posicao2 (Tuple[str, str]): Segunda posicao.
    Retorna:
        bool: True se forem identicas, False, caso contrario.
    """
    return eh_posicao(posicao1) and eh_posicao(posicao2) and posicao1 == posicao2

def posicao_para_str(posicao: Tuple[str, str]) -> str:
    """Converte uma posicao para a sua representacao textual.
    Argumentos:
        posicao (Tuple[str, str]): A posicao a converter.
    Retorna:
        str: A representacao em formato de texto (exemplo: 'a1').
    """
    return ''.join(posicao)

def obter_posicoes_adjacentes(posicao: Tuple[str, str]) -> Tuple[Tuple[str, str], ...]:
    """Devolve todas as posicoes diretamente adjacentes a posicao indicada.
    Argumentos:
        posicao (Tuple[str, str]): A posicao de referencia.
    Retorna:
        Tuple[Tuple[str, str], ...]: Tuplo contendo as posicoes adjacentes, ordenadas.
    """
    adj_strs = adjacencias[posicao_para_str(posicao)]
    return tuple(sorted((cria_posicao(p[0], p[1]) for p in adj_strs), key=_indice_posicao_leitura))
# -------------------------------------------------------------------------------------------------
# TAD peca
# -------------------------------------------------------------------------------------------------
def cria_peca(entrada: str) -> str:
    """Cria uma nova peca do jogo, garantindo que o simbolo e valido.
    Argumentos:
        entrada (str): Caracter que identifica a peca ('X', 'O' ou '').
    Retorna:
        str: A peca criada.
    Exce??es:
        ValueError: E gerado se o argumento nao corresponder a uma peca valida.
    """
    _validar_peca(entrada)
    return entrada

def cria_copia_peca(peca: str) -> str:
    """Cria uma copia de uma pe?a existente.
    Argumentos:
        peca (str): A peca a copiar.
    Retorna:
        str: A copia da peca fornecida.
    """
    return peca

def eh_peca(arg) -> bool:
    """Verifica se o argumento corresponde a uma pe?a valida do jogo.
    Argumentos:
        arg: O valor a verificar.
    Retorna:
        bool: True se for uma peca valida ('X', 'O' ou ''), False, caso contrario.
    """
    return isinstance(arg, str) and len(arg) == 1 and arg in ('X', 'O', ' ')

def pecas_iguais(peca1: str, peca2: str) -> bool:
    """Verifica se duas pecas sao iguais.
    Argumentos:
        peca1 (str): Primeira peca.
        peca2 (str): Segunda peca.
    Retorna:
        bool: True se forem identicas, False, caso contrario.
    """
    return eh_peca(peca1) and eh_peca(peca2) and peca1 == peca2

def peca_para_str(peca: str) -> str:
    """Converte uma peca para a sua representacao textual.
       Argumentos:
           peca (str): A peca a converter.
       Retorna:
           str: Representacao textual da peca (exemplo: '[X]').
       """
    return f'[{peca}]'

def peca_para_inteiro(peca: str) -> int:
    """Converte uma peca para um valor numerico.
    Argumentos:
        peca (str): A peca a converter.
    Retorna:
        int: 1 para 'X', -1 para 'O', 0 para espaco vazio.
    """
    return {'X': 1, 'O': -1, ' ': 0}[peca]

# -------------------------------------------------------------------------------------------------
# TAD tabuleiro
# -------------------------------------------------------------------------------------------------
def cria_tabuleiro() -> List[List[str]]:
    """Cria um tabuleiro vazio de 3x3 para o jogo.
     Retorna:
         List[List[str]]: Tabuleiro inicial com todas as posicoes vazias.
     """
    return [[' ' for _ in range(3)] for _ in range(3)]

def cria_copia_tabuleiro(tabuleiro: List[List[str]]) -> List[List[str]]:
    """Cria uma copia independente de um tabuleiro existente.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro a copiar.
    Retorna:
        List[List[str]]: Copia do tabuleiro fornecido.
    """
    return [row[:] for row in tabuleiro]

def _indice(posicao: Tuple[str, str]) -> Tuple[int, int]:
    """Converte uma posicao em indices de linha e coluna.
    Argumentos:
        posicao (Tuple[str, str]): A posicao converter.
    Retorna:
        Tuple[int, int]: indices correspondentes (linha, coluna) no tabuleiro.
    """
    return int(posicao[1]) - 1, ord(posicao[0]) - ord('a')

def obter_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> str:
    """Obtem a peca presente numa posicao especifica do tabuleiro.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): Posicao a consultar.
    Retorna:
        str: A peca presente na posicao ('X', 'O' ou ' ').
    """
    r, c = _indice(posicao)
    return tabuleiro[r][c]

def obter_vetor(tabuleiro: List[List[str]], seletor: str) -> Tuple[str, ...]:
    """Obtem todas as pecas de uma linha ou coluna do tabuleiro.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        seletor (str): Letra da coluna ou numero da linha.
    Retorna:
        Tuple[str, ...]: Tuplo de pecas correspondentes.
    Exce??es:
        ValueError: Da erro se o seletor for invalido.
    """
    if seletor in colunas:
        c = ord(seletor) - ord('a')
        return tuple(tabuleiro[r][c] for r in range(3))
    elif seletor in linhas:
        r = int(seletor) - 1
        return tuple(tabuleiro[r])
    raise ValueError('obter_vetor: argumento invalido')

def coloca_peca(tabuleiro: List[List[str]], peca: str, posicao: Tuple[str, str]) -> List[List[str]]:
    """Coloca uma peca numa posicao especifica do tabuleiro.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        peca (str): Peca a colocar ('X' ou 'O').
        posicao (Tuple[str, str]): Posicao onde colocar a peca.
    Retorna:
        List[List[str]]Tabuleiro atualizado.
    """
    r, c = _indice(posicao)
    tabuleiro[r][c] = peca
    return tabuleiro

def remove_peca(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> List[List[str]]:
    """Remove a peca de uma posicao especifica do tabuleiro.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): Posicao a limpar.
    Retorna:
        List[List[str]]: Tabuleiro atualizado.
    """
    r, c = _indice(posicao)
    tabuleiro[r][c] = ' '
    return tabuleiro

def move_peca(tabuleiro: List[List[str]], posicao_origem: Tuple[str, str], posicao_destino: Tuple[str, str]) -> List[List[str]]:
    """Move uma peca de uma posicao de origem para uma posicao de destino.
        Argumentos:
            tabuleiro (List[List[str]]): O tabuleiro.
            posicao_origem (Tuple[str, str]): Posicao atual da peca.
            posicao_destino (Tuple[str, str]): Nova posicao da peca.
        Retorna:
            List[List[str]]: Tabuleiro atualizado.
        """
    peca = obter_peca(tabuleiro, posicao_origem)
    remove_peca(tabuleiro, posicao_origem)
    coloca_peca(tabuleiro, peca, posicao_destino)
    return tabuleiro

def eh_tabuleiro(arg) -> bool:
    """Verifica se um argumento representa um tabuleiro valido do jogo.
    Argumentos:
        arg: Valor a verificar.
    Retorna:
        bool: True se o argumento for um tabuleiro v?lido, False, caso contrario.
              Um tabuleiro e valido se:
                - for uma lista 3x3 de pecas validas,
                - contiver no moximo 3 pecas de cada jogador,
                - a diferenca de pecas entre os jogadores nao for superior a 1,
                - nao existirem simultaneamente vencedores.
    """
    if not (isinstance(arg, list) and len(arg) == 3 and all(
            isinstance(r, list) and len(r) == 3 and all(eh_peca(p) for p in r) for r in arg)):
        return False
    pieces = reduce(list.__add__, arg)
    count_x, count_o = pieces.count('X'), pieces.count('O')
    if count_x > 3 or count_o > 3 or abs(count_x - count_o) > 1:
        return False
    vencedor_x = _tem_vencedor(arg, 'X')
    vencedor_o = _tem_vencedor(arg, 'O')
    return not (vencedor_x and vencedor_o)

def eh_posicao_livre(tabuleiro: List[List[str]], posicao: Tuple[str, str]) -> bool:
    """Verifica se uma posicao no tabuleiro esta livre (nao ocupada).
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        posicao (Tuple[str, str]): Posicao a verificar.
    Retorna:
        bool: True se a posicao estiver vazia, False, caso contr?rio.
    """
    return obter_peca(tabuleiro, posicao) == ' '

def tabuleiros_iguais(tabuleiro1: List[List[str]], tabuleiro2: List[List[str]]) -> bool:
    """Verifica se dois tabuleiros sao identicos.
    Argumentos:
        tabuleiro1 (List[List[str]]): Primeiro tabuleiro.
        tabuleiro2 (List[List[str]]): Segundo tabuleiro.
    Retorna:
        bool: True se ambos forem iguais, False caso contrario.
    """
    return tabuleiro1 == tabuleiro2

def tabuleiro_para_str(tabuleiro: List[List[str]]) -> str:
    """Converte um tabuleiro numa representacao textual legivel.
      Argumentos:
          tabuleiro (List[List[str]]): O tabuleiro.
      Retorna:
          str: Representacao visual do tabuleiro, com linhas, colunas e conex?es.
      """
    linhas_tabuleiro = [f'{linhas[r]} ' + '-'.join(peca_para_str(tabuleiro[r][c]) for c in range(3)) for r in range(3)]
    return '\n'.join([cabecalho, linhas_tabuleiro[0], conexao1, linhas_tabuleiro[1], conexao2, linhas_tabuleiro[2]])

def tuplo_para_tabuleiro(tuplo: Tuple[Tuple[int, ...], ...]) -> List[List[str]]:
    """Converte um tuplo de inteiros para um tabuleiro de pecas.
    Argumentos:
        tuplo (Tuple[Tuple[int, ...], ...]): Tuplo representando o tabuleiro (1=X, -1=O, 0=vazio).
    Retorna:
        List[List[str]]: Tabuleiro correspondente.
    Excecoes:
        ValueError: Se o tuplo nao estiver no formato correto.
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
    """Verifica se um jogador possui uma linha vencedora no tabuleiro.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro.
        jogador (str): Identificador do jogador ('X' ou 'O').
    Retorna:
        bool: True se o jogador tiver vencido, False caso contrario.
    """
    for linha_vencedora in linhas_vencedoras:
        if all(obter_peca(tabuleiro, cria_posicao(colunas[c], linhas[r])) == jogador for r, c in linha_vencedora):
            return True
    return False

def obter_ganhador(tabuleiro: List[List[str]]) -> str:
    """Obtem o vencedor do jogo, caso exista.
      Argumentos:
          tabuleiro (List[List[str]]): O tabuleiro atual.
      Retorna:
          str: 'X' se X venceu, 'O' se O venceu, ' ' se n?o houver vencedor.
      """
    if _tem_vencedor(tabuleiro, 'X'):
        return 'X'
    if _tem_vencedor(tabuleiro, 'O'):
        return 'O'
    return ' '

def obter_posicoes_livres(tabuleiro: List[List[str]]) -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes livres no tabuleiro.
       Argumentos:
           tabuleiro (List[List[str]]): O tabuleiro.
       Retorna:
           Tuple[Tuple[str, str], ...]: Tuplo com todas as posicoes nao ocupadas.
       """
    return tuple(pos for pos in _todas_posicoes() if eh_posicao_livre(tabuleiro, pos))

def obter_posicoes_jogador(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes ocupadas por um jogador.
      Argumentos:
          tabuleiro (List[List[str]]): O tabuleiro.
          jogador (str): Identificador do jogador ('X' ou 'O').
      Retorna:
          Tuple[Tuple[str, str], ...]: Tuplo com todas as posicoes do jogador.
      """
    return tuple(pos for pos in _todas_posicoes() if obter_peca(tabuleiro, pos) == jogador)

def _todas_posicoes() -> Tuple[Tuple[str, str], ...]:
    """Obtem todas as posicoes poss?veis no tabuleiro.
      Retorna:
          Tuple[Tuple[str, str], ...]: Tuplo contendo todas as posicoes (3x3).
      """
    return tuple(cria_posicao(c, l) for l in linhas for c in colunas)

# -------------------------------------------------------------------------------------------------
# Funcoes adicionais
# -------------------------------------------------------------------------------------------------
def _analisar_entrada(entrada: str) -> Tuple[Tuple[str, str], ...]:
    """Analisa a entrada do utilizador para obter posicoes de movimento ou colocacao.
    Argumentos:
        entrada (str): Entrada textual do utilizador (ex: 'a1' ou 'a1b2').
    Retorna:
        Tuple[Tuple[str, str], ...]: Tuplo de posi??es interpretadas.
    Excecoes:
        ValueError: Se a entrada nao for valida.
    """
    if len(entrada) == 2:
        return (cria_posicao(entrada[0], entrada[1]),)
    if len(entrada) == 4:
        return cria_posicao(entrada[0], entrada[1]), cria_posicao(entrada[2], entrada[3])
    raise ValueError(erro_movimento_manual)

def obter_movimento_manual(tabuleiro: List[List[str]], jogador: str) -> Tuple[Tuple[str, str], ...]:
    """Obtem o movimento do jogador humano, validando a entrada.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador atual ('X' ou 'O').
    Retorna:
        Tuple[Tuple[str, str], ...]: Movimento escolhido (posicao ou origem/destino).
    Excecoes:
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
    """Determina se o jogo ainda se encontra na fase de colocacao de pecas.
    Argumentos:
        tabuleiro (List[List[str]]): O tabuleiro atual.
    Retorna:
        bool: True se algum jogador ainda nao colocou as 3 pecas, False, caso contrario.
    """
    return len(obter_posicoes_jogador(tabuleiro, 'X')) < 3 or len(obter_posicoes_jogador(tabuleiro, 'O')) < 3

def _encontrar_posicao(tabuleiro: List[List[str]], jogador: str, predicado) -> Optional[Tuple[str, str]]:
    """Procura uma posicao que satisfaca um predicado especifico.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador que vai testar a posicao.
        predicado: Funcao que retorna True se a posicao for desejavel.
    Retorna:
        Optional[Tuple[str, str]]: Posicao encontrada ou None.
    """
    for pos in obter_posicoes_livres(tabuleiro):
        tab_copia = cria_copia_tabuleiro(tabuleiro)
        coloca_peca(tab_copia, jogador, pos)
        if predicado(tab_copia):
            return pos
    return None

def _posicao_vitoria(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    """Encontra uma posicao que permita ao jogador ganhar imediatamente.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador a testar.
    Retorna:
        Optional[Tuple[str, str]]: Posicao de vitoria ou None.
    """
    return _encontrar_posicao(tabuleiro, jogador, lambda tc: obter_ganhador(tc) == jogador)


def _posicao_bloqueio(tabuleiro: List[List[str]], jogador: str) -> Optional[Tuple[str, str]]:
    """Encontra uma posicao que bloqueie a vitoria do adversario.
       Argumentos:
           tabuleiro (List[List[str]]): Tabuleiro atual.
           jogador (str): Jogador a proteger.
       Retorna:
           Optional[Tuple[str, str]]: Posicao de bloqueio ou None.
       """
    return _posicao_vitoria(tabuleiro, _obter_adversario(jogador))

def obter_movimento_auto(tabuleiro: List[List[str]], jogador: str, nivel: str) -> Tuple[Tuple[str, str], ...]:
    """Calcula o movimento automatico do computador com base no nivel de dificuldade.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador do computador ('X' ou 'O').
        nivel (str): N?vel de dificuldade ('facil', 'normal', 'dificil').
    Retorna:
        Tuple[Tuple[str, str], ...]: Movimento calculado.
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
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
    Retorna:
        int: 1 se X venceu, -1 se O venceu, 0 caso contrario.
    """
    ganhador = obter_ganhador(tabuleiro)
    return 1 if ganhador == 'X' else -1 if ganhador == 'O' else 0

def _ordenar_movimentos(tabuleiro: List[List[str]], jogador: str,movimentos: Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]) -> Tuple[Tuple[Tuple[str, str], Tuple[str, str]], ...]:
    """Ordena movimentos, priorizando aqueles que levam a vitoria.
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador a analisar.
        movimentos: Tuplo de movimentos possiveis (origem, destino).
    Retorna:
        Tuple: Movimentos ordenados com prioridade para vitoria imediata.
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
    Argumentos:
        tabuleiro (List[List[str]]): Tabuleiro atual.
        jogador (str): Jogador atual.
        profundidade (int): Profundidade restante.
        alpha (int): Valor alpha para poda.
        beta (int): Valor beta para poda.
        maximizando (bool): True se estiver a maximizar, False, se a minimizar.
    Retorna:
        Tuple[int, Optional[Tuple]]: (valor do tabuleiro, melhor movimento).
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
    """Funcao principal para jogar o jogo do Moinho.
    Argumentos:
        jogador_str (str): Peca do jogador humano ('[X]' ou '[O]').
        nivel_dificuldade (str): N?vel de dificuldade do computador ('facil', 'normal', 'dificil').
    Retorna:
        str: Representacao da peca vencedora ('[X]', '[O]').
    Exce??es:
        ValueError: Se os argumentos forem inv?lidos.
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
