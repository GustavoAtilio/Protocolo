#!/usr/bin/python3
import time
import socket

host = "" #Nome ou endereço IP da máquina servidora
port = 3000        #Porta que o servidor vai aguardar conexões 
palavra = ["insert","update","delete","find","list"]
resultado = "Protocolo inválido."  
comandoNaoEncontrado = 1;
dados = []


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
soc.bind((host,port)) 
soc.listen(100)

def comunicacao():
  while True:
    print("Aguardando conexão na porta " + str(port) + " ...")
    con, client = soc.accept() 
    while(True):
      try:
          msg = con.recv(1024).decode()
          print(">> " + str(client) + ": " + msg)
          lista = msg.split()   
          comando = lista[0]

          if comando == palavra[0]:
              dados.append(lista[1])
              con.sendall("palavra adicionada".encode())    

          if comando == palavra[1]:
              prin("....")

          if comando == palavra[2]:
              prin("....")

          if comando == palavra[3]:
              prin("....")   

          if comando == palavra[4]:
              aux = 1;
              for x in dados:
                  con.sendall( (x+"\n").encode() ) 
                  ++aux

          for teste in palavra:
              if teste == comando:
                  ++comandoNaoEncontrado
          if comandoNaoEncontrado == 4:
              con.sendall((resultado+",").encode()) 


      except Exception as e:   
              print("servidor parado...\n reconectando em 3s\n") 
              time.sleep(3) 
              comunicacao()
comunicacao()              
           
