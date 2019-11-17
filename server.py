#!/usr/bin/python3

import socket
import os
import random
#from random import randrange

USUARIOS = ["USER1", "USER2", "USER3"]
SENHAS = ["SENHA1", "SENHA2", "SENHA3"]
BANCO = []

host = "" #Nome ou endereço IP da máquina servidora
port = 3000        #Porta que o servidor vai aguardar conexões 

# Cria um socket usando o protocolo TCP
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Essa linha abaixo é pra fechar o socket caso o programa seja interrompido, por exemplo, com CONTROL+C
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# Associa a porta e o host ao socket 
soc.bind((host,port)) 

# Inicia uma thread que aguarda por uma conexão
soc.listen(100)

# Loop infinito que aguarda conexões, uma de cada vez
while True:
    print("Aguardando conexão na porta " + str(port) + " ...")
    con, client = soc.accept() 
    
    while True:
       msg = con.recv(1024).decode()
       print("Recebeu de " + str(client) + ": " + msg)
       print(">> " + str(client) + ": " + msg)
      
       #Cria uma lista com a mensagem enviada pelo usuário
       lista = msg.split() 
       
       #garante que o servidor não feche ao ser digitado quit ou pressionado ctrl+c
       if len(lista) > 0:
          comando = lista[0]
       else:
          break
       
       resultado = "ERRO a operação '" + comando + "' não existe"
       
       if comando == "insert":
          if len(lista) > 1:
             qtd = len(lista)
             nome = ""
             for i in range(1, qtd):
                if i == qtd - 1:
                   nome = nome + lista[i]
                else:
                   nome = nome + lista[i] + " "
                str(nome)
             BANCO.append(nome)
             resultado = "OK"
          else:
             resultado = "ERRO a operação insert exige um argumento <nome>."

       if comando == "list":
          if len(lista) == 1:
             resultado = ""
             if len(BANCO) > 0:
                for i in range(0, len(BANCO)):
                   if i == len(BANCO) - 1:
                      result = "[" + str(i) + "] " + str(BANCO[i])
                   else:
                      result = "[" + str(i) + "] " + str(BANCO[i]) + "\n"
                   resultado = resultado + result
                str(resultado)
             else:
                resultado = "A lista de nomes está vazia."
          else:
             resultado = "ERRO a operação list não recebe argumentos."

       if comando == "update":
          if len(lista) > 2:
             try:
                indice = int(lista[1])
                nome = ""
                qtd = len(lista)
                for i in range(2, qtd):
                   if i == qtd - 1:
                      nome = nome + lista[i]
                   else:
                      nome = nome + lista[i] + " "
                   str(nome)
                if indice < len(BANCO):
                   BANCO[indice] = nome
                   resultado = "OK"
                else:
                   resultado = "ERRO indice " + str(indice) + " não existe."
             except ValueError:
                resultado = "ERRO o argumento <indice> precisa ser um valor inteiro."
          else:
             resultado = "ERRO a operação update exige os argumentos <indice> <nome>."

       if comando == "delete":
          if len(lista) == 2:
             try:
                indice = int(lista[1])
                if indice < len(BANCO):
                   del BANCO[indice]
                   resultado = "OK"
                else:
                   resultado = "ERRO indice " + str(indice) + " não existe."
             except ValueError:
                resultado = "ERRO o argumento <indice> precisa ser um valor inteiro."
          else:
             resultado = "ERRO a operação delete exige um argumento <indice>."

       if comando == "find":
          if len(lista) == 2:
             qtd = len(BANCO)
             find = lista[1]
             select = ""
             for i in range(0, qtd):
                pesquisa = BANCO[i]
                if find in pesquisa:
                   select = select + "[" + str(i) + "] " + BANCO[i] + "\n"
                   #print("[" + str(i) + "] " + BANCO[i])
             if select != "":
                posicao = len(select)
                resultado = select[:posicao - 1]
             else:
                resultado = "Nenhum resultado encontrado para ’" + find + "’."
             str(resultado)
          else:
             resultado = "ERRO a operação find exige um argumento <busca>."

       #Envia para o cliente o conteúdo da variável resultado 
       con.sendall(resultado.encode())  
  
    con.close() 

