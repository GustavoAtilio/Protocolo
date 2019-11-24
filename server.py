#!/usr/bin/python3

import socket
import os
import random
#from random import randrange

USUARIOS = ["USER1", "USER2", "USER3"]
SENHAS = ["SENHA1", "SENHA2", "SENHA3"]
BANCO = []
logado = False

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
          logado = False
          break
       
       resultado = "ERRO a operação '" + comando + "' não existe"

       if comando == "login":
          if len(lista) == 3:
             for i in range(0, len(USUARIOS)):
                if lista[1] == USUARIOS[i]:
                   if lista[2] == SENHAS[i]:
                      logado = True
                      break
             if logado == True:
                resultado = "Logado com sucesso"
             else:
                resultado = "Usuário e/ou senha incorretos"
          else:
             resultado = "ERRO a operação login exige os argumentos <usuario> <senha>."

       if comando == "insert":
          if logado == True:
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
          else:
            resultado = "É necessário realizar login para usar essa operação: login <usuario> <senha>"

       if comando == "list":
          if logado == True:
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
          else:
            resultado = "É necessário realizar login para usar essa operação: login <usuario> <senha>"

       if comando == "update":
          if logado == True:
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
                   if indice < len(BANCO) and indice >= 0:
                      BANCO[indice] = nome
                      resultado = "OK"
                   else:
                      resultado = "ERRO indice " + str(indice) + " não existe."
                except ValueError:
                   resultado = "ERRO o argumento <indice> precisa ser um valor inteiro."
             else:
                resultado = "ERRO a operação update exige os argumentos <indice> <nome>."
          else:
            resultado = "É necessário realizar login para usar essa operação: login <usuario> <senha>"

       if comando == "delete":
          if logado == True:
             if len(lista) == 2:
                try:
                   indice = int(lista[1])
                   if indice < len(BANCO) and indice >= 0:
                      del BANCO[indice]
                      resultado = "OK"
                   else:
                      resultado = "ERRO indice " + str(indice) + " não existe."
                except ValueError:
                   resultado = "ERRO o argumento <indice> precisa ser um valor inteiro."
             else:
                resultado = "ERRO a operação delete exige um argumento <indice>."
          else:
            resultado = "É necessário realizar login para usar essa operação: login <usuario> <senha>"

       if comando == "find":
          if logado == True:
             if len(lista) == 2:
                qtd = len(BANCO)
                find = lista[1]
                select = ""
                for i in range(0, qtd):
                   pesquisa = BANCO[i]
                   if find in pesquisa:
                      select = select + "[" + str(i) + "] " + BANCO[i] + "\n"
                if select != "":
                   posicao = len(select)
                   resultado = select[:posicao - 1]
                else:
                   resultado = "Nenhum resultado encontrado para ’" + find + "’."
                str(resultado)
             else:
                resultado = "ERRO a operação find exige um argumento <busca>."
          else:
            resultado = "É necessário realizar login para usar essa operação: login <usuario> <senha>"

       #Envia para o cliente o conteúdo da variável resultado 
       con.sendall(resultado.encode())  
  
    con.close() 

