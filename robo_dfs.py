visitados = []

def marcar_visitado(pos_I, pos_J):
    visitados.append((pos_I, pos_J))

def robo_limpeza(matriz, pos_I, pos_J, linhas, colunas):
  if(pos_I < 0 or pos_I >= linhas or pos_J < 0 or pos_J >= colunas):
    return
  if(matriz[pos_I][pos_J] == 1):
    return
  if(matriz[pos_I][pos_J] == 2):
    print("Sujeira encontrada e limpa na posição: ", pos_I, pos_J)
    matriz[pos_I][pos_J] = 0

  if (pos_I, pos_J) in visitados:
    return
  
  marcar_visitado(pos_I, pos_J)
  
  robo_limpeza(matriz,pos_I + 1, pos_J, linhas, colunas) # baixo
  robo_limpeza(matriz,pos_I - 1, pos_J, linhas, colunas) # cima
  robo_limpeza(matriz,pos_I, pos_J + 1, linhas, colunas) # direita
  robo_limpeza(matriz,pos_I, pos_J - 1, linhas, colunas) # esquerda