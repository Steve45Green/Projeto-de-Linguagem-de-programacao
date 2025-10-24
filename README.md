Projeto: Jogo do Moinho (3x3)
================================
Jose Ameixa nº18881 | Diogo Vaz n-21132 | Pedro Duarte n-21190
## Descrição
Este projeto implementa o Jogo do Moinho (variante 3x3 com três peças por jogador) em Python 3, permitindo que um jogador humano jogue contra o computador em diferentes níveis de dificuldade.
## Objetivo
Desenvolver um programa modular que respeite as barreiras de abstração, utilizando Tipos Abstratos de Dados (TADs) para representar posições, peças e tabuleiro para implementar estratégias automáticas para o computador, incluindo o algoritmo minimax.
## Regras do Jogo
Tabuleiro 3x3.

Cada jogador dispõe de três peças.

Vence o jogador que alinhar as três peças na horizontal ou vertical.

O jogo decorre em duas fases:

1. Colocação: os jogadores colocam alternadamente as peças.
2. Movimento: após todas as peças estarem colocadas, os jogadores movem peças para posições adjacentes livres.
#### Estratégia do Computador
Fase de colocação:

1. Vitória imediata;
2. Bloqueio do adversário;
3. Centro;
4. Cantos;
5. Laterais.

Fase de movimento:

Utiliza o algoritmo minimax com profundidade definida pelo nível de dificuldade.

### Níveis de Dificuldade:
##### Fácil:
Escolhe a primeira jogada válida.
##### Normal:
Tenta vitória imediata; caso não seja possível, joga como fácil.

##### Difícil: 
Utiliza o algoritmo minimax com profundidade 5.
## Estrutura do Código
TAD Posição: cria_posicao, obter_pos_c, obter_pos_l, etc.

TAD Peça: cria_peca, peca_para_str, peca_para_inteiro, etc.

TAD Tabuleiro: cria_tabuleiro, coloca_peca, move_peca, obter_ganhador, etc.

Funções de jogo: obter_movimento_manual, obter_movimento_auto, moinho.

### Como Executar
#### Testes Públicos
```text
python public_tests.py
```
#### Jogo Interativo
```text
python run.py
```
### Notas Importantes
Apenas caracteres ASCII são permitidos.

Não utilizar bibliotecas externas além das fornecidas pelo Python.

O código deve respeitar as barreiras de abstração e as mensagens de erro definidas no enunciado.
## Exemplo de Execução
```text
Bem-vindo ao JOGO DO MOINHO. Nível de dificuldade fácil.
   a   b   c
1 [ ]-[ ]-[ ]
 | \ | / |
2 [ ]-[ ]-[ ]
 | / | \ |
3 [ ]-[ ]-[ ]
Turno do jogador. Escolha uma posição: a1
