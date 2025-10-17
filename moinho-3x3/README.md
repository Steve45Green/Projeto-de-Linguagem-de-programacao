Projeto: Jogo do Moinho (3x3)
================================
Jose Ameixa nº18881 |  Colega x    | Colega y

Resumo
------
Este projeto implementa o jogo do Moinho (3x3, 3 pecas por jogador) em Python, ASCII-only e sem dependencias externas.

Execução
--------
- Testes publicos:
  python public_tests.py

- Jogo interativo:
  python run.py

Niveis de AI
---------------------------------
- facil: Primeira jogada valida por ordem de leitura (origem e destino)
- normal: Escolhe uma vitoria imediata; se nao houver, comporta-se como "facil"
- dificil: Minimax com profundidade 5

Nota sobre o teste publico 25
-----------------------------
 5a jogada do jogador é a1b1, mas o b1 ja tem uma jogada feita por AI (NOTA IMPORTANTE: Temos que alterar a função para def_auto_colocacao)


