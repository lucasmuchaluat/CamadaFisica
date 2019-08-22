
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


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)
print("abriu com")

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





 
    print ("Recebendo dados .... ")
    
    # head = bytearray()
    # should_stop = False
    # while not should_stop:
    #     rxBuffer, nRx = com.getData(1)
    #     if bytes([3]) in buffer: # b'barra'
    #         should_stop = True
    #     else:
    #         buffer += rxBuffer

    # buffer = buffer[:-5]
        

    rxBuffer, nRx = com.getData(3) #vai ler 10 dps, por enquanto deixa 3 pra testar

    print("Tamanho:")
    print(int.from_bytes(rxBuffer, "big"))

    

    rxBuffer, nRx = com.getData(int.from_bytes(rxBuffer, "big"))

    with open("img_received.jpg", "wb") as image:
        image.write(rxBuffer)

    # log
    print ("Lido              {} bytes ".format(nRx))
    
    print (rxBuffer)

    rxLen_bytes = nRx.to_bytes(length=2,byteorder='big')
    # barra = bytearray(b'barra')
    

    print("Transmitido o tamanho {} para o Server".format(nRx))
    com.sendData(rxLen_bytes)
    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
       pass

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
