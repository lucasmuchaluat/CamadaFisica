
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
serialName = "COM11"                  # Windows(variacao de)
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

  head = txLen_bytes + bytes(7)
  # barra = bytearray(b'barra')
  data = head + file # + barra

  totalLen = len(data)
  
  return data, txLen, totalLen

def payload_correction (file):
  payload_only_len = len(file)
  buffer = bytearray()
  eop = b'eop'
  for i in file:
  # for contador in range (len_data + 10): # head tem 10 bytes
  #   rxBuffer, nRx = com.getData(1) # aqui n faz sentido ser getData pq n tem nd no arduino ainda
    if eop in buffer: # b'barra' ou bytes([3])
        #BYTE STUFFING
        buffer = buffer[:-3]
        buffer += b'0e0o0p'
        buffer.append(i)
    else:
        buffer.append(i)

  return buffer, payload_only_len

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

    data, payload_only_len = payload_correction(txBuffer)
    data = eop(data)
    data, txLen, totalLen = head(data)

    print(data.decode("latin-1"))
    
    # Transmite dado
    print("tentado transmitir .... {} bytes".format(txLen))
    seconds = time.time()
    com.sendData(data)
    

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


    delta_t = time.time() - seconds

    position_eop, nRx_position = com.getData(2)
    len_payload, nRx_payload = com.getData(2)

    position_eop_received = int.from_bytes(position_eop, "big")
    payload_received = int.from_bytes(len_payload, "big")

    print("Taxa de  envio: {} bytes/segundo".format(payload_only_len/delta_t))

    overhead = 100*(totalLen/payload_only_len)
    print("OVERHEAD: {} %".format(overhead))

    if position_eop_received == 0:
      print("EOP nao existe, por favor, revise o empacotamento!")
    elif position_eop_received == 1:
      print("EOP esta na posicao errada")
    else:
      print("EOP beggining position: {}".format(position_eop_received))

    if payload_received == 0:
      print("Payload não corresponde ao informado no head")
    else:
      print("Payload corresponde com o informado no head")





    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
