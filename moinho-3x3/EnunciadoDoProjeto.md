Projeto
Jogo do Monho

Neste projeto irão desenvolver as funções de forma a implementar um programa em Python
que permita a um jogador humano jogar o Jogo do Moinho contra o computador.

Descrição do jogo
O jogo do moinho é um antigo jogo tradicional de tabuleiro para dois jogadores com uma
multitude de variantes dependendo do número de peças disponíveis para cada jogador e a
disposição do tabuleiro de jogo. O jogo do moinho é conhecido com vários nomes. Em inglês,
conhece-se como Nine men’s morris.

O tabuleiro de jogo
O tabuleiro de jogo considerado é uma estrutura retangular de tamanho 3x3. Cada posição
do tabuleiro é indexada pela coluna e a linha que ocupa. Num tabuleiro, uma posição pode
estar livre ou ocupada pela peça de um jogador. O exemplo da Figura 1 mostra um tabuleiro
com duas peças diferentes nas posições 𝑎 1 e 𝑏 2. A ordem de leitura das posições do tabuleiro
é definida da esquerda para a direita seguida de cima para baixo.

Figura 1 : Tabuleiro do jogo do moinho com peças diferentes nas posições 𝑎 1 e 𝑏 2.
Regras do jogo
Na variante do jogo do moinho considerada, cada jogador tem três peças e o vencedor é o
primeiro jogador a alinhar suas três peças numa linha vertical ou horizontal. O jogo
desenvolve-se em duas fases: colocação e movimento.

Na fase de colocação, tal como no jogo do galo, o tabuleiro começa inicialmente vazio
e os jogadores colocam de forma alternada uma das suas peças no tabuleiro. Após ter
colocado todas as peças, e se nenhum jogador conseguiu ganhar até então, começa a
fase de movimento.
Durante a fase de movimento, os jogadores continuam a alternar turnos, neste caso
podendo movimentar qualquer uma das peças próprias a qualquer um dos espaços
livres imediatamente adjacentes conectados por uma linha horizontal, vertical ou
diagonal.
O jogo continua até que um dos jogadores consegue ganhar.
Estratégia de jogo automático
Neste projeto consideraremos estratégias de jogo diferentes dependendo da fase de jogo.

Fase de colocação
Na fase de colocação, o jogador computador escolherá a primeira ação disponível da lista a
seguir:

Vitória: Se o jogador tiver duas das suas peças em linha e uma posição livre, então
deve marcar na posição livre (ganhando o jogo);
Bloqueio: Se o adversário tiver duas das suas peças em linha e uma posição livre, então
deve marcar na posição livre (para bloquear o adversário);
Centro: Se a posição central estiver livre, então jogar na posição central;
Canto vazio: Se um canto for uma posição livre, então jogar nesse canto;
Lateral vazio: Se uma posição lateral (que nem é o centro, nem um canto) for livre,
então jogar nesse lateral.
Fase de movimento
Na fase de movimento, o jogador computador utilizará o algoritmo minimax^1 para escolher o
seu seguinte movimento. O minimax é um algoritmo recursivo muito utilizado em teoria de
jogos que se pode sumarizar como a escolha do melhor movimento para um próprio
assumindo que o adversário irá a escolher o pior possível. Na prática, o algoritmo minimax
pode ser implementado como uma função recursiva que recebe um tabuleiro e o jogador com
o turno atual. A função explora todos os movimentos legais desse jogador chamando a função
recursiva com o tabuleiro modificado com um dos movimentos e o jogador adversário como
novos parâmetros. No caso geral, o algoritmo escolherá/devolverá o movimento que mais
favoreça o jogador do turno atual. A recursão finaliza quando existe um ganhador ou quando
se atinge um nível máximo de profundidade da recursão. O valor que devolve a função é o
valor do estado do tabuleiro para cada jogador, sendo positivo para estados de tabuleiro que
favoreçam ao jogador ‘X’ e negativo se favorecem ao jogador ‘O’. No projeto definimos uma
função simples para o valor dum tabuleiro: +1 se o ganhador é o joqador ‘X’, -1 se o ganhador
é jogador ‘O’, ou 0 se não há ganhador. Assim, no caso geral, quando é o jogador ‘X’ a escolher
movimento, escolherá/devolverá o primeiro movimento de valor máximo, e quando é o
jogador ‘O’ a escolher movimento, escolherá/devolverá o primeiro movimento de valor
mínimo. Adicionalmente, a função recursiva pode ter como argumento uma estrutura que é
utilizada para registar a sequência de movimentos realizados e que é atualizada na chamada
à função recursiva. O pseudo-código correspondente é descrito no Algoritmo 1.

Trabalho a realizar
O objetivo deste segundo projecto é definirem um conjunto de Tipos Abstratos de Dados
(TAD) que deverão ser utilizados para representar a informação necessária, bem como um
conjunto de funções adicionais que permitirão executar corretamente o jogo do moinho.

Tipos Abstratos de Dados
Atenção:

Apenas os construtores e as funções para as quais a verificação da correção dos
argumentos é explicitamente pedida devem verificar a validade dos argumentos.
Os modificadores, e as funções de alto nível que os utilizam, alteram de modo
destrutivo o seu argumento.
(^1) https://en.wikipedia.org/wiki/Minimax

Todas as funções de alto nível (ou seja, que não correspondem a operações básicas)
devem respeitar as barreiras de abstração.
TAD posicao (1.5 valores)
O TAD posicao é usado para representar uma posição do tabuleiro de jogo. Cada posição é
caraterizada pela coluna e linha que ocupa no tabuleiro. As operações associadas a este TAD
são:

Construtor:
o cria_posicao : str × str → posicao
▪ cria_posicao(c,l) recebe duas cadeias de carateres correspondentes à
coluna c e à linha l de uma posição e devolve a posição correspondente.
O construtor verifica a validade dos seus argumentos, gerando um
ValueError com a mensagem ‘cria_posicao: argumentos
invalidos’ caso os seus argumentos não sejam válidos.
o cria_copia_posicao : posicao → posicao
▪ cria_copia_posicao(p) recebe uma posição e devolve uma cópia nova
da posição.
Seletores:
o obter_pos_c : posicao → str
▪ obter_pos_c(p) devolve a componente coluna c da posição p.
o obter_pos_l : posicao → str
▪ obter_pos_l(p) devolve a componente linha l da posição p.
Reconhecedor:
o eh_posicao : universal → booleano
▪ eh_posicao(arg) devolve True caso o seu argumento seja um TAD
posicao e False caso contrário.
Teste:
o posicoes_iguais : posicao × posicao → booleano
▪ posicoes_iguais(p1,p2) devolve True apenas se p1 e p2 são posições e
são iguais.
Transformador:
o posição_para_str : posicao → str
▪ posicao_para_str(p) devolve a cadeia de caracteres ‘ cl ’ que representa
o seu argumento, sendo os valores c e l as componentes coluna e linha
de p.
Função de alto nível:
o obter_posicoes_adjacentes : posicao → tuplo de posicoes
▪ obter_posicoes_adjacentes(p) devolve um tuplo com as posições
adjacentes à posição p de acordo com a ordem de leitura do tabuleiro.
Exemplos de interação:

p1 = cria_posicao(’a’, ’4’)
Traceback (most recent call last): <...>
ValueError: cria_posicao: argumentos invalidos
p1 = cria_posicao(’a’, ’2’)
p2 = cria_posicao(’b’, ’3’)
posicoes_iguais(p1, p2)
False
posicao_para_str(p1)
’a2’
tuple(posicao_para_str(p) for p in obter_posicoes_adjacentes(p2))
(’b2’, ’a3’, ’c3’)

TAD peca (1.5 valores)
O TAD peca é usado para representar as peças do jogo. Cada peça é caracterizada pelo jogador
a quem pertencem, podendo ser peças do jogador ‘X’ ou do jogador ‘O’. Por conveniência, é
também definido o conceito peça livre, que é uma peça que não pertence a nenhum jogador.
As operações associadas a este TAD são:

Construtor:
o cria_peca : str → peca
▪ cria_peca(s) recebe uma cadeia de carateres correspondente ao
identificador de um dos dois jogadores (‘X’ ou ‘O’) ou a uma peça livre
(‘ ‘) e devolve a peça correspondente. O construtor verifica a validade
dos seus argumentos, gerando um ValueError com a mensagem
‘cria_peca: argumento invalido’ caso o seu argumento não seja
válido.
o cria_copia_peca : peca → peca
▪ cria_copia_peca(j) recebe uma peça e devolve uma cópia nova da peça.
Reconhecedor:
o eh_peca : universal → booleano
▪ eh_peca(arg) devolve True caso o seu argumento seja um TAD peca e
False caso contrário.
Teste:
o pecas_iguais : peca × peca → booleano
▪ pecas_iguais(j1,j 2 ) devolve True apenas se j 1 e j 2 são peças e são
iguais.
Transformador:
o peca_para_str : peca → str
▪ peca_para_str(j) devolve a cadeia de caracteres que representa o
jogador dono da peça, isto é, ‘[X]’, ‘[O]’, ou ‘[ ]’.
Função de alto nível:
o peca_para_inteiro : peca → N
▪ peca_para_inteiro(j) devolve um inteiro valor 1, -1, ou 0, dependendo
se a peça é do jogador ‘X’, ‘O’, ou livre, respetivamente.
Exemplos de interação:

j1 = cria_peca(’x’)
Traceback (most recent call last): <...> ValueError: cria_peca: argumento
invalido
j1 = cria_peca(’X’)
j2 = cria_peca(’O’)
pecas_iguais(j1, j2)
False
peca_para_str(j1)
’[X]’
peca_para_inteiro(cria_peca(’ ’))
0

TAD tabuleiro (3 valores)
O TAD tabuleiro é usado para representar um tabuleiro do jogo do moinho de 3x3 posições e
as peças dos jogadores que nele são colocadas. As operações associadas a este TAD são:

Construtor:
o cria_tabuleiro : {} → tabuleiro
▪ cria_tabuleiro() devolve um tabuleiro de jogo do moinho de 3x3 sem
posições ocupadas por peças de jogador.
o cria_copia_tabuleiro : tabuleiro → tabuleiro
▪ cria_copia_tabuleiro(t) recebe um tabuleiro e devolve uma cópia nova
do tabuleiro.
Seletores:
o obter_peca : tabuleiro × posicao → peca
▪ obter_peca(t,p) devolve a peça na posição p do tabuleiro. Se a posição
não estiver ocupada, devolve uma peça livre.
o obter_vetor : tabuleiro × str → tuplo de pecas
▪ obter_vetor(t,s) devolve todas as peças da linha ou coluna especificada
pelo seu argumento_._
Modificadores:
o coloca_peca : tabuleiro × peca × posicao → tabuleiro
▪ coloca_peca(t,j,p) modifica destrutivamente o tabuleiro t colocando a
peça j na posição p , e devolve o próprio tabuleiro.
o remove_peca : tabuleiro × posicao → tabuleiro
▪ _remove peca(t,p) modifica destrutivamente o tabuleiro t removendo
a peça da posição p , e devolve o próprio tabuleiro.
o move_peca : tabuleiro × posicao × posicao → tabuleiro
▪ move_peca(t,p1,p2) modifica destrutivamente o tabuleiro t movendo
a peça que se encontra na posição p 1 para a posição p2 , e devolve o
próprio tabuleiro.
Reconhecedor:
o eh_tabuleiro : universal → booleano
▪ eh_tabuleiro(arg) devolve True caso o seu argumento seja um TAD
tabuleiro e False caso contrário. Um tabuleiro válido pode ter um
máximo de 3 peças de cada jogador, não pode conter mais de 1 peça
mais de um jogador que do contrário, e apenas pode haver um
ganhador em simultâneo.
o eh_posicao_livre : tabuleiro × posicao → booleano
▪ eh_posicao_livre(t,p) devolve True apenas no caso da posição p do
tabuleiro corresponder a uma posição livre.
Teste:
o tabuleiros_iguais : tabuleiro × tabuleiro → booleano
▪ tabuleiro s _iguais(t1,t 2 ) devolve True apenas se t 1 e t 2 são tabuleiros
e são iguais.
Transformador:
o tabuleiro_para_str : tabuleiro → str
▪ tabuleiro_para_str(t) devolve a cadeia de caracteres que representa o
tabuleiro t como mostrado nos exemplos a seguir.
o tuplo_para_tabuleiro : tuplo → tabuleiro
▪ tuplo_para_tabuleiro(t) devolve o tabuleiro que é representado pelo
tuplo t com 3 tuplos, cada um deles contendo 3 valores inteiros iguais
a 1, -1 ou 0, tal como no enunciado do primeiro projeto.
Funções de alto nível:
o obter_ganhador : tabuleiro → peca
▪ obter_ganhador(t) devolve uma peça do jogador que tenha as suas 3
peças em linha na vertical ou na horizontal no tabuleiro. Se não existir
nenhum ganhador, devolve uma peça livre.
o obter_posicoes_livres : tabuleiro → tuplo de posicoes
▪ obter_posicoes_livres(t) devolve um tuplo com as posições não
ocupadas pelas peças de qualquer um dos dois jogadores na ordem de
leitura do tabuleiro.
o obter_posicoes_jogador : tabuleiro × peca → tuplo de posicoes
▪ obter_posicoes_jogador(t,j) devolve um tuplo com as posições
ocupadas pelas peças j de um dos dois jogadores na ordem de leitura
do tabuleiro.
Exemplos de interação:

t = cria_tabuleiro()
tabuleiro_para_str(coloca_peca(t, cria_peca(’X’),
ria_posicao(’a’,’1’)))
‘ a b c\n1 [X]-[ ]-[ ]\n | \ | / |\n2 [ ]-[ ]-[ ]\n | / | \
|\n3 [ ]-[ ]-[ ]’
print(tabuleiro_para_str(t))
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [ ]-[ ]-[ ]
| \ | / |
3 [ ]-[ ]-[ ]
print(tabuleiro_para_str(coloca_peca(t, cria_peca(’O’),
cria_posicao(’b’,’2’))))
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [ ]-[O]-[ ]
| \ | / |
3 [ ]-[ ]-[ ]
print(tabuleiro_para_str(move_peca(t, cria_posicao(’a’,’1’),
cria_posicao(’b’,’1’))))
a b c
1 [ ]-[X]-[ ]
| \ | / |
2 [ ]-[O]-[ ]
| \ | / |
3 [ ]-[ ]-[ ]
t = tuplo_para_tabuleiro(((0,1,-1),(-0,1,-1),(1,0,-1)))
print(tabuleiro_para_str(t))
a b c
1 [ ]-[X]-[O]
| \ | / |
2 [ ]-[X]-[O]
| \ | / |
3 [X]-[ ]-[O]
peca_para_str(obter_ganhador(t))
’[O]’
tuple(posicao_para_str(p) for p in obter_posicoes_livres(t))
(’a1’, ’a2’, ’b3’)
tuple(peca_para_str(peca) for peca in obter_vetor(t, ’a’))
(’[ ]’, ’[ ]’, ’[X]’)
tuple(peca_para_str(peca) for peca in obter_vetor(t, ’2’))
(’[ ]’, ’[X]’, ’[O]’)

Funções adicionais
obter_movimento_manual: tabuleiro × peca → tuplo de posicoes ( 1 .5 valores)

Função auxiliar que recebe um tabuleiro e uma peça de um jogador, e devolve um tuplo com
uma ou duas posições que representam uma posição ou um movimento introduzido
manualmente pelo jogador. Na fase de colocação, o tuplo contém apenas a posição escolhida
pelo utilizador onde colocar uma nova peça. Na fase de movimento, o tuplo contém a posição
de origem da peça que se deseja movimentar e a posição de destino. Se não for possível
movimentar nenhuma peça por estarem todas bloqueadas, o jogador pode passar o turno
escolhendo como movimento a posição duma peça própria seguida da mesma posição que

ocupa. Se o valor introduzido pelo jogador não corresponder a uma posição ou movimento
válidos, a função deve gerar um erro com a mensagem ’obter_movimento_manual: escolha
invalida’. A função deve apresentar a mensagem ’Turno do jogador. Escolha uma
posicao: ’ ou ’Turno do jogador. Escolha um movimento: ’, para pedir ao utilizador
para introduzir uma posição ou um movimento.

t = cria_tabuleiro()
m = obter_movimento_manual(t, cria_peca(’X’))
Turno do jogador. Escolha uma posicao: a
posicao_para_str(m[0])
’a1’
t = tuplo_para_tabuleiro(((0,1,-1),(1,-1,0),(1,-1,0)))
m = obter_movimento_manual(t, cria_peca(’X’))
Turno do jogador. Escolha um movimento: b1a
posicao_para_str(m[0]), posicao_para_str(m[1])
(’b1’, ’a1’)
m = obter_movimento_manual(t, cria_peca(’O’))
Turno do jogador. Escolha um movimento: a2a
Traceback (most recent call last): <...>
ValueError: obter_movimento_manual: escolha invalida

obter_movimento_auto: tabuleiro × peca × str → tuplo de posicoes (3 valores)

Função auxiliar que recebe um tabuleiro, uma peça de um jogador e uma cadeia de carateres
representando o nível de dificuldade do jogo, e devolve um tuplo com uma ou duas posições
que representam uma posição ou um movimento escolhido automaticamente. Na fase de
colocação, o tuplo contém apenas a posição escolhida automaticamente onde colocar uma
nova peça seguindo as regras da secção “Fase de colocação” automática. Se não for possível
movimentar nenhuma peça por estarem todas bloqueadas, a função devolve como
movimento a posição da primeira peça do jogador correspondente seguida da mesma posição
que ocupa. Na fase de movimento, o tuplo contém a posição de origem da peça a movimentar
e a posição de destino. A escolha automática do movimento depende do nível de dificuldade
do jogo:

‘facil’ (1 valor): a peça a movimentar é sempre a que ocupa a primeira posição em
ordem de leitura do tabuleiro que tenha alguma posição adjacente livre. A posição de
destino é a primeira posição adjacente livre.
‘normal’ (1 valor): o movimento é escolhido utilizando o algoritmo descrito na secção
“Fase de movimento” automática com nível de profundidade máximo de recursão
igual a 1. Este nível é equivalente a escolher o primeiro movimento possível que
permita obter uma vitória. Se não existir nenhum movimento de vitória, então é
seguido o mesmo critério de escolha do nível ‘facil’.
‘dificil’ (1 valor): o movimento é escolhido utilizando o algoritmo descrito na secção
“Fase de movimento” automática com nível de profundidade máximo de recursão
igual a 5.
t = cria_tabuleiro()
m = obter_movimento_auto(t, cria_peca(’X’), ’facil’)
posicao_para_str(m[0])
’b2’
t = tuplo_para_tabuleiro(((1,0,-1),(0,1,-1),(1,-1,0)))
m = obter_movimento_auto(t, cria_peca(’X’), ’facil’)
posicao_para_str(m[0]), posicao_para_str(m[1])

(’a1’, ’b1’)

m = obter_movimento_auto(t, cria_peca(’X’), ’normal’)
posicao_para_str(m[0]), posicao_para_str(m[1])
(’b2’, ’a2’)
t = tuplo_para_tabuleiro(((1,-1,-1),(-1,1,0),(0,0,1)))
m = obter_movimento_auto(t, cria_peca(’X’), ’normal’)
posicao_para_str(m[0]), posicao_para_str(m[1])
(’b2’, ’c2’)
m = obter_movimento_auto(t, cria_peca(’X’), ’dificil’)
posicao_para_str(m[0]), posicao_para_str(m[1])
(’c3’, ’c2’)

moinho: str × str → str (1.5 valores)
Função principal que permite jogar um jogo completo do jogo do moinho de um jogador
contra o computador. A função recebe duas cadeias de caracteres e devolve a representação
externa da peça ganhadora (‘[X]’ ou ‘[O]’). O primeiro argumento corresponde à
representação externa da peça com que deseja jogar o jogador humano, e o segundo
argumento selecciona o nível de dificuldade do jogo. Se algum dos argumentos dados forem
inválidos, a função deve gerar um erro com a mensagem ‘moinho: argumentos invalidos’.
A função deve apresentar a mensagem ‘Turno do computador ():’, em que
corresponde à cadeia de caracteres passada como segundo argumento, quando for
o turno do computador.

moinho(’[X]’, ’facil’)
Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade facil.
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [ ]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: a
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
m = obter_movimento_auto(t, cria_peca(’X’), ’normal’)
>>> posicao_para_str(m[0]), posicao_para_str(m[1])
(’b2’, ’c2’)
>>> m = obter_movimento_auto(t, cria_peca(’X’), ’dificil’)
>>> posicao_para_str(m[0]), posicao_para_str(m[1])
(’c3’, ’c2’)

moinho: str × str → str (1.5 valores)
Função principal que permite jogar um jogo completo do jogo do moinho de um jogador
contra o computador. A função recebe duas cadeias de caracteres e devolve a representação
externa da peça ganhadora (‘[X]’ ou ‘[O]’). O primeiro argumento corresponde à
representação externa da peça com que deseja jogar o jogador humano, e o segundo
argumento selecciona o nível de dificuldade do jogo. Se algum dos argumentos dados forem
inválidos, a função deve gerar um erro com a mensagem ‘moinho: argumentos invalidos’.
A função deve apresentar a mensagem ‘Turno do computador ():’, em que
corresponde à cadeia de caracteres passada como segundo argumento, quando for
o turno do computador.

>>> moinho(’[X]’, ’facil’)
Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade facil.
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [ ]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: a
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: a
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
posicao_para_str(m[0]), posicao_para_str(m[1])
(’c3’, ’c2’)

moinho: str × str → str (1.5 valores)
Função principal que permite jogar um jogo completo do jogo do moinho de um jogador
contra o computador. A função recebe duas cadeias de caracteres e devolve a representação
externa da peça ganhadora (‘[X]’ ou ‘[O]’). O primeiro argumento corresponde à
representação externa da peça com que deseja jogar o jogador humano, e o segundo
argumento selecciona o nível de dificuldade do jogo. Se algum dos argumentos dados forem
inválidos, a função deve gerar um erro com a mensagem ‘moinho: argumentos invalidos’.
A função deve apresentar a mensagem ‘Turno do computador ():’, em que
corresponde à cadeia de caracteres passada como segundo argumento, quando for
o turno do computador.

>>> moinho(’[X]’, ’facil’)
Bem-vindo ao JOGO DO MOINHO. Nivel de dificuldade facil.
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [ ]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: a
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[ ]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [ ]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: a
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [ ]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [X]-[ ]-[ ]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |

3 [O]-[ ]-[ ]
Turno do jogador. Escolha uma posicao: c
a b c
1 [X]-[ ]-[X]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [O]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [X]-[O]-[X]
| \ | / |
2 [X]-[O]-[ ]
| / | \ |
3 [O]-[ ]-[ ]
Turno do jogador. Escolha um movimento: c1c
a b c
1 [X]-[O]-[ ]
| \ | / |
2 [X]-[O]-[X]
| / | \ |
3 [O]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [X]-[ ]-[O]
| \ | / |
2 [X]-[O]-[X]
| / | \ |
3 [O]-[ ]-[ ]
Turno do jogador. Escolha um movimento: a1b
a b c
1 [ ]-[X]-[O]
| \ | / |
2 [X]-[O]-[X]
| / | \ |
3 [O]-[ ]-[ ]
Turno do computador (facil):
a b c
1 [O]-[X]-[O]
| \ | / |
2 [X]-[ ]-[X]
| / | \ |
3 [O]-[ ]-[ ]
Turno do jogador. Escolha um movimento: b1b
a b c
1 [O]-[ ]-[O]
| \ | / |
2 [X]-[X]-[X]
| / | \ |
3 [O]-[ ]-[ ]
‘[X]’

Condições de Realização e Prazos
A entrega do projeto será efetuada exclusivamente por via eletrónica. Deverão
submeter através do sistema Moodle, até às 23:59 do dia 16 de dezembro de 202 5.
Depois desta hora, a nota do projeto sofre uma penalização de dois valores por cada
hora de atraso. Por exemplo, uma entrega às 00h de dia 17 terá dois valores de
desconto, e uma entrega às 01h terá quatro.
Apenas um elemento do grupo deverá submeter um único ficheiro GXX.zip com um
ficheiro com extensão .py contendo todo o código do projeto e um ficheiro .txt com a
percentagem de esforço de cada elemento do grupo na elaboração do projeto. O
grupo 1 deve submeter como G01.zip.
No vosso ficheiro de código não devem ser utilizados caracteres acentuados ou
qualquer outro carácter não pertencente à tabela ASCII. Todos os testes automáticos
falharão, mesmo que os caracteres não ASCII sejam utilizados dentro de comentários
ou cadeias de caracteres. Programas que não cumpram este requisito serão
penalizados em três valores.
Não é permitida a utilização de qualquer módulo ou função não disponível built-in no
Python 3, com exceção da função reduce do functools. Projetos que não cumpram
este requisito terão 0.
Pode, ou não, haver uma discussão oral do trabalho e/ou uma demonstração do
funcionamento do programa (será decidido caso a caso).
Lembrem-se que no IPBeja a fraude académica é levada muito a sério e que a cópia
numa prova (projetos incluídos) leva à reprovação na disciplina. O docente da cadeira
será o único juiz do que se considera ou não copiar.
Será considerada para avaliação a última submissão feita por um elemento do grupo.
Deverão, portanto, verificar cuidadosamente que a última entrega realizada
corresponde à versão do projeto que pretendem que seja avaliada.
Classificação
A nota do projeto será baseada nos seguintes aspetos:

Avaliação automática ( 6 0%). A avaliação da correta execução será feita através de
testes automáticos. O tempo de execução de cada teste está limitado, bem como a
memória utilizada. Os alunos terão acesso a uma bateria de testes públicos. O facto
de um projeto completar com sucesso os testes públicos fornecidos não implica que
esse projeto esteja totalmente correto, pois estes não são exaustivos. É da
responsabilidade de cada grupo garantir que o código produzido está de acordo com
a especificação do enunciado, para completar com sucesso os testes privados.
Respeito pelas barreiras de abstração (20%). Esta componente da avaliação é feita
automaticamente, recorrendo a um conjunto de scripts que testam posteriormente o
respeito pelas barreiras de abstração do código desenvolvido pelo grupo.
Avaliação manual (20%). Estilo de programação e facilidade de leitura^2. Em particular,
serão consideradas as seguintes componentes:
o Boas práticas (1.5 valores): serão considerados entre outros a clareza do
código, a integração de conhecimento adquirido durante a UC e a criatividade
das soluções propostas.
o Comentários (1 valor): deverão incluir a assinatura das funções definidas,
comentários para o utilizador (docstring) e comentários para o programador.
o Tamanho de funções, duplicação de código e abstração procedimental (
valor).
o Escolha de nomes (0.5 valores).
(^2) Podem encontrar algumas boas práticas relacionadas em https://gist.github.com/ruimaranhao/4e18cbe3dad6f68040c32ed6709090a3

Recomendações e aspetos a evitar
As seguintes recomendações e aspetos correspondem a sugestões para evitar maus hábitos
de trabalho (e, consequentemente, más notas no projeto):

Leiam todo o enunciado, procurando perceberem o objetivo das várias funções
pedidas. Em caso de dúvida de interpretação, contactem o docente para esclarecerem
as vossas questões.
No processo de desenvolvimento do projeto, comecem por implementar as várias
funções pela ordem apresentada no enunciado, seguindo as metodologias estudadas
na disciplina. Ao desenvolverem cada uma das funções pedidas, comecem por
perceber se podem usar alguma das criadas anteriormente.
Para verificar a funcionalidade das vossas funções, utilizem os exemplos fornecidos
como casos de teste. Tenham o cuidado de reproduzir fielmente as mensagens de erro
e restantes outputs, conforme ilustrado nos vários exemplos.
Não pensem que o projeto se pode fazer nos últimos dias. Se apenas iniciarem o vosso
trabalho neste período irão ver a Lei de Murphy em funcionamento (todos os
problemas são mais difíceis do que parecem; tudo demora mais tempo do que nós
pensamos; e se alguma coisa puder correr mal, ela vai correr mal, na pior das alturas
possíveis).
Não dupliquem código. Se duas funções são muito semelhantes é natural que estas
possam ser fundidas numa única, eventualmente com mais argumentos.
Não se esqueçam que as funções excessivamente grandes são penalizadas no que
respeita ao estilo de programação.
A atitude “vou pôr agora o programa a correr de qualquer maneira e depois preocupo-
me com o estilo” é totalmente errada.
Quando o programa gerar um erro, preocupem-se em descobrir qual a causa do erro.

As “marteladas” no código têm o efeito de distorcer cada vez mais o código.

