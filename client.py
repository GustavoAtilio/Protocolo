#!/usr/bin/python3

import socket

host = "localhost" #Nome ou endereço IP da máquina servidora
port = 3000 #Porta que o servidor vai aguardar conexões 
 
soc = socket.socket() #Cria o socket
soc.connect((host,port)) 

while True:

   msg = input(">>> ")
   
   if msg == "quit":
      soc.close
      break
   if len(msg) <= 0:
      continue
   else:
      espaco = 0
      for i in msg:
         if i == " ":
            espaco = espaco + 1
      if len(msg) == espaco:
         continue

   soc.sendall(msg.encode())

   rec = soc.recv(1024).decode()

   print (rec)

soc.close()

