8 Rainhas

Este repositório contém uma implementação de diferentes algoritmos para resolver o problema das 8 Rainhas, desenvolvida como parte da disciplina de Inteligência Artificial. O código compara as abordagens de Hill Climbing, Simulated Annealing e Algoritmo Genético, proporcionando uma visualização interativa dos resultados usando Pygame.

Funcionalidades
Hill Climbing: Algoritmo de subida de encosta com detecção de pontos de reinicialização para evitar mínimos locais.
Simulated Annealing: Implementa o algoritmo de recozimento simulado, variando a temperatura inicial e o fator de resfriamento.
Algoritmo Genético: Utiliza operações de crossover e mutação para evoluir uma população de soluções, buscando a melhor configuração para o problema das N Rainhas.
Visualização
O Pygame é utilizado para desenhar os tabuleiros resultantes de cada algoritmo, permitindo uma comparação visual dos métodos. O tempo de execução, o número de iterações, a qualidade da solução e o número de reinicializações (no caso de Hill Climbing) são exibidos na interface.

Requisitos
Python 3.x
Pygame
