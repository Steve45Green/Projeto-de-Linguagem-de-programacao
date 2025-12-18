# Projeto: Jogo do Moinho 3x3 (Python)

Implementação em Python do Jogo do Moinho 3x3, permitindo a um jogador humano jogar contra uma Inteligência Artificial (computador), desenvolvido no âmbito de uma unidade curricular de Programação.

## Objetivo do Projeto

O objetivo deste projeto foi definir um conjunto de Tipos Abstratos de Dados (TAD) e funções em Python para implementar o Jogo do Moinho. O programa final permite que um jogador humano escolha jogar com 'X' ou 'O' e compita contra o computador em três níveis de dificuldade: 'facil', 'normal' e 'dificil'.

## Regras do Jogo

Esta implementação segue um conjunto de regras específico para a variante 3x3:

* **Tabuleiro:** O jogo é disputado num tabuleiro de jogo 3x3.
* **Peças:** Cada jogador tem três peças.
* **Vitória:** O vencedor é o primeiro jogador a conseguir alinhar as suas três peças numa linha **horizontal ou vertical**. Alinhamentos diagonais não contam como vitória.
* **Fase 1: Colocação:** O jogo começa com o tabuleiro inicialmente vazio. Os jogadores colocam, alternadamente, uma das suas três peças numa casa vazia. O jogo pode terminar nesta fase se um jogador conseguir a vitória.
* **Fase 2: Movimento:** Após todas as 6 peças (3 de 'X' e 3 de 'O') estarem no tabuleiro e não houver vencedor, começa a fase de movimento. Em cada turno, o jogador pode movimentar uma das suas peças para um espaço livre imediatamente adjacente (ligado por linha horizontal, vertical ou diagonal).
* **Bloqueio (Passar):** Se um jogador não tiver nenhum movimento possível (porque todas as suas peças estão bloqueadas), ele pode "passar" o turno. No código, isto é representado por um movimento da peça para a sua própria posição (ex: 'a1a1').

---

## Lógica do Código e Arquitetura

O projeto está estruturado em torno de três Tipos Abstratos de Dados (TADs) principais, que suportam a lógica do jogo e da IA, respeitando as barreiras de abstração.

### 1. Tipos Abstratos de Dados (TADs)

A informação do jogo é gerida sem violar as barreiras de abstração.

* **`TAD posicao`**
    * **Representação Interna:** `tuple` (ex: `('a', '1')`)
    * **Funções Principais:** `cria_posicao`, `obter_pos_c`, `obter_pos_l`, `eh_posicao`, `posicoes_iguais`, `posicao_para_str`.
    * **Lógica de Adjacência:** A função `obter_posicoes_adjacentes` usa um dicionário (`_LIGACOES`) para definir as conexões e um mapa (`_ORDEM_LEITURA_MAP`) para garantir que as posições devolvidas estão sempre na "ordem de leitura" correta (da esquerda para a direita, de cima para baixo), como exigido pelo enunciado.

* **`TAD peca`**
    * **Representação Interna:** `str` (ex: `'X'`, `'O'`, ou `' '`)
    * **Funções Principais:** `cria_peca`, `eh_peca`, `pecas_iguais`, `peca_para_str`, `peca_para_inteiro`.

* **`TAD tabuleiro`**
    * **Representação Interna:** `list[list[str]]` (uma matriz 3x3 que armazena `TADs peca`).
    * **Funções Principais:** `cria_tabuleiro`, `cria_copia_tabuleiro`, `obter_peca`, `coloca_peca`, `remove_peca`, `move_peca`, `eh_tabuleiro`, `obter_ganhador`, `obter_posicoes_livres`, `obter_posicoes_jogador`.

### 2. Ciclo de Jogo (Função `moinho`)

A função `moinho` é o ponto de entrada principal e gere o fluxo do jogo:

1.  **Inicialização:** Valida os argumentos (peça do humano e nível de dificuldade). Define quem é o `humano` e quem é o `cpu`.
2.  **Boas-vindas:** Imprime a mensagem de boas-vindas e o tabuleiro inicial vazio.
3.  **Loop Principal:** Inicia um ciclo `while` que continua enquanto `obter_ganhador(tabuleiro)` devolver a peça livre (`' '`).
4.  **Gestão de Turno:** O turno começa sempre com `'X'`.
5.  **Turno Humano:** Se o `turno` atual for igual ao `humano`:
    * Chama `obter_movimento_manual()`, que pede um `input()` ao utilizador.
    * Esta função valida a jogada (formato, regras de colocação ou regras de movimento) e levanta um erro (`ERRO_JOGADA_MANUAL`) se for inválida.
6.  **Turno do Computador:** Se o `turno` atual for igual ao `cpu`:
    * Imprime a mensagem "Turno do computador...".
    * Chama `obter_movimento_auto()`, passando o nível de dificuldade.
7.  **Execução:** A jogada (do humano ou do cpu) é aplicada ao tabuleiro através de `_executar_movimento`.
8.  **Atualização:** O tabuleiro atualizado é impresso no ecrã.
9.  **Troca de Turno:** O turno é passado para o `outro_jogador`.
10. **Fim de Jogo:** Quando o ciclo `while` termina, a função devolve a representação `string` do vencedor (ex: `'[X]'`).

### 3. Lógica da IA (Função `obter_movimento_auto`)

Esta é a função central da IA, que decide qual lógica usar com base na fase do jogo.

#### Estratégia de Colocação (Fase 1)

Se `_esta_na_fase_colocacao()` for `True`, a IA segue uma lista de prioridades estrita (`_escolher_colocacao_ia`) para decidir onde colocar a peça. A primeira regra que se aplicar é executada:

1.  **Vitória:** Joga na posição que lhe dá a vitória imediata (`_encontrar_vitoria_colocacao`).
2.  **Bloqueio:** Joga na posição que impede o adversário de ganhar na próxima jogada (`_encontrar_bloqueio_colocacao`).
3.  **Centro:** Joga na posição central (`'b2'`) se estiver livre.
4.  **Canto Vazio:** Joga no primeiro canto livre (`'a1'`, `'c1'`, `'a3'`, `'c3'`).
5.  **Lateral Vazia:** Joga na primeira lateral livre (`'b1'`, `'a2'`, `'c2'`, `'b3'`).

#### Estratégia de Movimento (Fase 2)

Se o jogo estiver na fase de movimento, a lógica depende do nível de dificuldade:

* **Nível 'facil':**
    * Chama `_calcular_movimento_facil`.
    * Esta função escolhe a **primeira peça** do computador (na ordem de leitura) que se pode mover para a sua **primeira posição adjacente livre** (também na ordem de leitura). É uma IA determinística.

* **Nível 'normal':**
    * Primeiro, a IA verifica se tem algum movimento de vitória imediata (`_encontrar_vitoria_movimento`).
    * Se tiver, joga esse movimento (esta é uma pesquisa Minimax de profundidade 1).
    * Se não tiver, joga exatamente como o nível 'facil'.

* **Nível 'dificil':**
    * Chama `_algoritmo_minimax(tabuleiro, jogador_cpu, max_depth=5)`.
    * Este algoritmo explora a árvore de jogo até 5 jogadas à frente para encontrar o melhor movimento possível.

### 4. Lógica Minimax (Nível 'difícil')

O Minimax é o cérebro da IA de nível 'difícil'. A lógica está dividida para ser mais limpa e eficiente:

1.  **`_algoritmo_minimax` (Ponto de Entrada):** É a função "wrapper" que inicia a chamada recursiva principal (`_minimax_recursivo`), definindo a profundidade e os valores iniciais de `alpha` (-10) e `beta` (10).
2.  **`_minimax_recursivo` (O Núcleo):**
    * **Estado Terminal:** Se o jogo acabou (`obter_ganhador != ' '`) ou a profundidade (`depth`) é 0, chama a `_minimax_avaliacao`.
    * **Geração de Movimentos:** Obtém a lista de todos os movimentos válidos (`_gerar_movimentos_validos`).
    * **Otimização (Poda Alpha-Beta):** Antes de testar os movimentos, chama `_minimax_ordenar_movs`. Esta função coloca as jogadas de vitória imediata no início da lista. Isto torna a Poda Alpha-Beta muito mais eficaz, pois encontra os melhores (ou piores) ramos mais cedo.
    * **Recursão:**
        * Se for o turno do 'X' (Maximizador), ele tenta encontrar o `melhor_resultado` que seja o mais alto possível (começa em -10).
        * Se for o turno do 'O' (Minimizador), ele tenta encontrar o `melhor_resultado` que seja o mais baixo possível (começa em 10).
    * **Poda (Corte):** Em ambos os casos, se `alpha >= beta`, o `break` é ativado e o resto dos movimentos para aquele ramo é ignorado, poupando tempo de cálculo.

---

## Como Executar o Jogo

1.  Certifique-se de que tem o Python 3 instalado.
2.  Guarde o código como `projeto.py` .
3.  Execute o ficheiro a partir do terminal:
    ```bash
    python3 projeto.py
    ```
4.  O jogo irá começar. Primeiro, ser-lhe-á pedido para escolher a sua peça (ex: `[X]`) e o nível de dificuldade (ex: `facil`).
5.  Siga as instruções no ecrã para introduzir as suas jogadas (ex: `a1` para colocar, ou `a1a2` para mover).

## Autores

* José Ameixa 
* Diogo Vaz 
* Pedro Duarte
