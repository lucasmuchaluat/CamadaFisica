
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time
from tkinter import filedialog, Tk



# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM10"                  # Windows(variacao de)
print("abriu com")

def check (original, recebida):
  if original == recebida:
    return True
  else:
    return False

def head (file):
  txLen = len(file)
  print(txLen)

  txLen_bytes = txLen.to_bytes(length=3,byteorder='big')

  head = txLen_bytes # + bytes(7)
  # barra = bytearray(b'barra')
  data = head + file # + barra
  
  return data, txLen

def payload_correction (headfile, len_data):
  buffer = bytearray()
  eop = b'eop'
  for i in headfile:
  # for contador in range (len_data + 10): # head tem 10 bytes
  #   rxBuffer, nRx = com.getData(1) # aqui n faz sentido ser getData pq n tem nd no arduino ainda
    if eop in buffer: # b'barra' ou bytes([3])
        #BYTE STUFFING
        buffer = buffer[:-3]
        buffer.append(b'0e0o0p')
        buffer.append(i)
    else:
        buffer.append(i)

  return buffer

def eop (headfile):
  eop = b'eop'
  data = headfile + eop
  return data
    

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

   

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("gerando dados para transmissao :")
  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
    #exemplo 1
    #ListTxBuffer =list()
    #for x in range(1,10):
    #    ListTxBuffer.append(x)
    #txBuffer = bytes(ListTxBuffer)
    
    #exemplo2
    #txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')

    root = Tk()
    root.withdraw

    filename = filedialog.askopenfilename()

    with open (filename, "rb") as img:
      txBuffer = img.read()
    
    
    # txLen    = len(txBuffer)
    # print(txLen)

    # txLen_bytes = txLen.to_bytes(length=3,byteorder='big')

    # head = txLen_bytes + bytes(7)
    # # barra = bytearray(b'barra')
    # data = head + txBuffer # + barra 

    data, txLen = head(txBuffer)
    data = payload_correction(data, txLen)
    data = eop(data)
    
    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    com.sendData(data)
    seconds = time.time()

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
       pass
    
    
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))

    # Faz a recepção dos dados
    # print ("Recebendo dados .... ")
    
    #repare que o tamanho da mensagem a ser lida é conhecida!     
    # rxBuffer, nRx = com.getData(txLen)

    # log
    # print ("Lido              {} bytes ".format(nRx))
    
    # print (rxBuffer)
    print("Buffer transmitido para o outro Arduino")


    # with open ("insper_after.jpg", "wb") as img_final:
    #   img_final.write(txBuffer)

    print("Aguardando a resposta do Client ....")

    # Faz a recepção dos dados
    print ("Recebendo dados do Client .... ")

    rxBuffer_check, nRx_check = com.getData(2)

    delta_time = time.time() - seconds

    received = int.from_bytes(rxBuffer_check, "big")

    print("check: {}".format(check(txLen,received)))
    
    print("taxa: {} bytes/sec".format(received/delta_time))



    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
