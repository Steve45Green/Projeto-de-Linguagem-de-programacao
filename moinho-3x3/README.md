Projeto: Jogo do Moinho (3x3)
================================
Jose Ameixa nº18881 

Resumo
------
Este projeto implementa o jogo do Moinho (3x3, 3 pecas por jogador) em Python, ASCII-only e sem dependencias externas.

Execução
--------
- Testes publicos:
  python public_tests.py

- Jogo interativo:
  python run.py

Niveis de IA 
---------------------------------
- facil: Primeira jogada valida por ordem de leitura (origem e destino)
- normal: Escolhe uma vitoria imediata; se nao houver, comporta-se como "facil"
- dificil: Minimax com profundidade 5

Nota sobre o teste publico 25
-----------------------------
Em conformidade estrita com o enunciado, o nivel "dificil" usa minimax profundidade 5. 
Isto permite ao computador (peca 'O' quando aplicavel) encontrar vitorias imediatas na fase de movimento. 
O teste publico 25 assume um comportamento nao otimo do computador e pode falhar quando a IA joga de forma otima. 
Este comportamento é esperado e não representa um erro na implementação, de acordo com a declaração.
Para passar no teste 25 artificialmente, seria necessário rebaixar a IA de «difícil» para «O» na fase de movimento, o que não é recomendado.
