from ambiente import Ambiente
from robo_dfs import robo_limpeza

print("Digite o número de linhas do ambiente:")
linhas = int(input())
print("Digite o número de colunas do ambiente:")
colunas = int(input())

ambiente = Ambiente(linhas, colunas)
ambiente.gerar_ambiente()

print("Matriz inicial:")
ambiente.mostrar_matriz()

linha_robo, coluna_robo = ambiente.posicao_robo
print("Posição inicial do robô: ", linha_robo, coluna_robo)
robo_limpeza(ambiente.matriz, linha_robo, coluna_robo, linhas, colunas)
print("Matriz final após a limpeza:")
ambiente.mostrar_matriz()