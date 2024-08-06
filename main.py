import pygame
import random
import time
import math

class NQueens:
    def __init__(self, tamanho=8):
        self.tamanho = tamanho
        self.tabuleiro = [-1] * self.tamanho
        self.iteracoes = 0
        self.qualidade = 0
        self.restarts = 0  # Contador de reinicializações

    def calcular_conflitos(self):
        conflitos = 0
        for i in range(self.tamanho):
            for j in range(i + 1, self.tamanho):
                if self.tabuleiro[i] == self.tabuleiro[j] or \
                   self.tabuleiro[i] - self.tabuleiro[j] == i - j or \
                   self.tabuleiro[j] - self.tabuleiro[i] == i - j:
                    conflitos += 1
        return conflitos

    def hill_climbing(self):
        self.restarts = 0
        while True:
            self.tabuleiro = [random.randint(0, self.tamanho - 1) for _ in range(self.tamanho)]
            conflitos = self.calcular_conflitos()
            self.iteracoes = 0

            while conflitos != 0:
                self.iteracoes += 1
                vizinho = self.encontrar_vizinho()
                conflitos_vizinho = self.calcular_conflitos_vizinho(vizinho)
                if conflitos_vizinho < conflitos:
                    self.tabuleiro = vizinho
                    conflitos = conflitos_vizinho
                else:
                    break

            if conflitos == 0:
                break
            else:
                self.restarts += 1

        self.qualidade = self.tamanho - conflitos
        return True

    def encontrar_vizinho(self):
        melhor_vizinho = self.tabuleiro[:]
        melhor_conflito = self.calcular_conflitos()

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if j != self.tabuleiro[i]:
                    vizinho = self.tabuleiro[:]
                    vizinho[i] = j
                    conflitos_vizinho = self.calcular_conflitos_vizinho(vizinho)
                    if conflitos_vizinho < melhor_conflito:
                        melhor_conflito = conflitos_vizinho
                        melhor_vizinho = vizinho
        return melhor_vizinho

    def calcular_conflitos_vizinho(self, tabuleiro):
        conflitos = 0
        for i in range(self.tamanho):
            for j in range(i + 1, self.tamanho):
                if tabuleiro[i] == tabuleiro[j] or \
                   tabuleiro[i] - tabuleiro[j] == i - j or \
                   tabuleiro[j] - tabuleiro[i] == i - j:
                    conflitos += 1
        return conflitos

    def simulated_annealing(self):
        self.tabuleiro = [random.randint(0, self.tamanho - 1) for _ in range(self.tamanho)]
        # Variando temperatura e resfriamento
        temperatura = random.uniform(1.0, 5.0)  # Exemplo: temperatura inicial entre 1.0 e 5.0
        resfriamento = random.uniform(0.90, 0.99)  # Exemplo: fator de resfriamento entre 0.90 e 0.99
        print(f"temperatura {temperatura}")
        print(f"resfriamento {resfriamento}")

        conflitos = self.calcular_conflitos()
        self.iteracoes = 0

        while conflitos != 0 and temperatura > 0.01:
            self.iteracoes += 1
            vizinho = self.encontrar_vizinho()
            conflitos_vizinho = self.calcular_conflitos_vizinho(vizinho)
            delta_conflito = conflitos_vizinho - conflitos

            if delta_conflito < 0 or random.uniform(0, 1) < math.exp(-delta_conflito / temperatura):
                self.tabuleiro = vizinho
                conflitos = conflitos_vizinho

            temperatura *= resfriamento

        self.qualidade = self.tamanho - conflitos
        return conflitos == 0

    def algoritmo_genetico(self, populacao_size=200, geracoes=5000, taxa_mutacao=0.03):
        populacao = [self.gerar_individuo() for _ in range(populacao_size)]
        self.iteracoes = 0

        for _ in range(geracoes):
            self.iteracoes += 1
            populacao = sorted(populacao, key=self.calcular_conflitos_individuo)
            if self.calcular_conflitos_individuo(populacao[0]) == 0:
                self.tabuleiro = populacao[0]
                self.qualidade = self.tamanho - self.calcular_conflitos_individuo(self.tabuleiro)
                return True

            nova_populacao = populacao[:2]
            while len(nova_populacao) < populacao_size:
                pai1, pai2 = self.selecionar_pais(populacao)
                filho1, filho2 = self.crossover(pai1, pai2)
                nova_populacao.extend([self.mutar(filho1, taxa_mutacao), self.mutar(filho2, taxa_mutacao)])

            populacao = nova_populacao

        self.tabuleiro = populacao[0]
        self.qualidade = self.tamanho - self.calcular_conflitos_individuo(self.tabuleiro)
        return self.calcular_conflitos_individuo(populacao[0]) == 0

    def gerar_individuo(self):
        return [random.randint(0, self.tamanho - 1) for _ in range(self.tamanho)]

    def calcular_conflitos_individuo(self, individuo):
        nqueens_temp = NQueens(self.tamanho)
        nqueens_temp.tabuleiro = individuo
        return nqueens_temp.calcular_conflitos()

    def selecionar_pais(self, populacao):
        pais = random.choices(populacao, k=2)
        return pais[0], pais[1]

    def crossover(self, pai1, pai2):
        ponto_corte = random.randint(1, self.tamanho - 1)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        return filho1, filho2

    def mutar(self, individuo, taxa_mutacao):
        if random.random() < taxa_mutacao:
            pos = random.randint(0, self.tamanho - 1)
            individuo[pos] = random.randint(0, self.tamanho - 1)
        return individuo

    def imprimir_tabuleiro(self):
        for i in range(self.tamanho):
            linha = ['.'] * self.tamanho
            if self.tabuleiro[i] != -1:
                linha[self.tabuleiro[i]] = 'Q'
            print(' '.join(linha))
        print()

def desenhar_tabuleiro(tela, tabuleiro, tamanho_casa, cor_fundo, cor_linha, cor_rainha, x_offset, y_offset):
    for linha in range(len(tabuleiro)):
        for coluna in range(len(tabuleiro)):
            retangulo = pygame.Rect(x_offset + coluna * tamanho_casa, y_offset + linha * tamanho_casa, tamanho_casa, tamanho_casa)
            if (linha + coluna) % 2 == 0:
                pygame.draw.rect(tela, cor_fundo, retangulo)
            else:
                pygame.draw.rect(tela, cor_linha, retangulo)
            if tabuleiro[linha] == coluna:
                pygame.draw.circle(tela, cor_rainha, retangulo.center, tamanho_casa // 4)

def exibir_tabuleiros(tabuleiro_hill, tabuleiro_simulated, tabuleiro_genetic, tempo_hill, tempo_simulated, tempo_genetic, iteracoes_hill, iteracoes_simulated, iteracoes_genetic, qualidade_hill, qualidade_simulated, qualidade_genetic, restarts_hill):
    pygame.init()
    tamanho = len(tabuleiro_hill)
    largura_tela = 2000
    altura_tela = 1000
    tamanho_casa = (largura_tela // (3 * tamanho)) - 20
    espaco = 50

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("8 Rainhas - Comparação")

    cor_fundo = (255, 255, 255)
    cor_linha = (0, 0, 0)
    cor_rainha = (255, 0, 0)
    cor_texto = (0, 0, 0)

    fonte = pygame.font.Font(None, 36)

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill((192, 192, 192))

        desenhar_tabuleiro(tela, tabuleiro_hill, tamanho_casa, cor_fundo, cor_linha, cor_rainha, espaco, espaco)
        desenhar_tabuleiro(tela, tabuleiro_simulated, tamanho_casa, cor_fundo, cor_linha, cor_rainha, 2 * espaco + tamanho * tamanho_casa, espaco)
        desenhar_tabuleiro(tela, tabuleiro_genetic, tamanho_casa, cor_fundo, cor_linha, cor_rainha, 3 * espaco + 2 * tamanho * tamanho_casa, espaco)

        texto_hill = fonte.render(f'Hill Climbing: Tempo = {tempo_hill:.2f}s\n Iterações = {iteracoes_hill}\n Qualidade = {qualidade_hill}\n Restarts = {restarts_hill}', True, cor_texto)
        texto_simulated = fonte.render(f'Simulated Annealing: Tempo = {tempo_simulated:.2f}s\n Iterações = {iteracoes_simulated}\n Qualidade = {qualidade_simulated}', True, cor_texto)
        texto_genetic = fonte.render(f'Algoritmo Genético: Tempo = {tempo_genetic:.2f}s\n Iterações = {iteracoes_genetic}\n Qualidade = {qualidade_genetic}', True, cor_texto)

        tela.blit(texto_hill, (espaco, tamanho * tamanho_casa + 2 * espaco))
        tela.blit(texto_simulated, (2 * espaco + tamanho * tamanho_casa, tamanho * tamanho_casa + 2 * espaco))
        tela.blit(texto_genetic, (3 * espaco + 2 * tamanho * tamanho_casa, tamanho * tamanho_casa + 2 * espaco))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    nqueens_hill = NQueens()
    nqueens_simulated = NQueens()
    nqueens_genetic = NQueens()

    inicio_hill = time.time()
    nqueens_hill.hill_climbing()
    fim_hill = time.time()

    inicio_simulated = time.time()
    nqueens_simulated.simulated_annealing()
    fim_simulated = time.time()

    inicio_genetic = time.time()
    nqueens_genetic.algoritmo_genetico(populacao_size=200, geracoes=5000, taxa_mutacao=0.03)
    fim_genetic = time.time()

    tempo_hill = fim_hill - inicio_hill
    tempo_simulated = fim_simulated - inicio_simulated
    tempo_genetic = fim_genetic - inicio_genetic

    nqueens_hill.imprimir_tabuleiro()
    print(f'Tempo Hill Climbing: {tempo_hill:.2f}s, Iterações: {nqueens_hill.iteracoes}, Qualidade: {nqueens_hill.qualidade}, Restarts: {nqueens_hill.restarts}')

    nqueens_simulated.imprimir_tabuleiro()
    print(f'Tempo Simulated Annealing: {tempo_simulated:.2f}s, Iterações: {nqueens_simulated.iteracoes}, Qualidade: {nqueens_simulated.qualidade}')

    nqueens_genetic.imprimir_tabuleiro()
    print(f'Tempo Algoritmo Genético: {tempo_genetic:.2f}s, Iterações: {nqueens_genetic.iteracoes}, Qualidade: {nqueens_genetic.qualidade}')

    exibir_tabuleiros(nqueens_hill.tabuleiro, nqueens_simulated.tabuleiro, nqueens_genetic.tabuleiro, tempo_hill, tempo_simulated, tempo_genetic, nqueens_hill.iteracoes, nqueens_simulated.iteracoes, nqueens_genetic.iteracoes, nqueens_hill.qualidade, nqueens_simulated.qualidade, nqueens_genetic.qualidade, nqueens_hill.restarts)
