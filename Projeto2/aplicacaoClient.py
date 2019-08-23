
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
serialName = "COM16"                  # Windows(variacao de)
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


    rxBuffer_len, nRx = com.getData(3) #vai ler 10 dps, por enquanto deixa 3 pra testar

    print("Tamanho:")
    print(int.from_bytes(rxBuffer_len, "big"))

    
    rxBuffer, nRx = com.getData(7)

    seconds = time.time()
    rxBuffer_eop, nRx = com.getData(int.from_bytes(rxBuffer_len, "big"))

    



    buffer_len = 0
    begin_position = 0
    buffer = bytearray()
    #Verificar se o EOP existe
    if b'eop' in rxBuffer_eop:
        #Verificar se o EOP está na posição correta
        if b'eop' in rxBuffer_eop[-3:]:
            #Localizar a posição do EOP
            for i in rxBuffer_eop:
                buffer_len += 1
                if b'eop' in buffer:
                    begin_position -= 2
                    


                else:
                    buffer.append(i)
                    begin_position += 1
        else:
            begin_position = 1
    else:
        begin_position = 0

    
    buffer_len = buffer_len - 3

    rxBuffer_len = int.from_bytes(rxBuffer_len, "big") - 3

    if buffer_len != rxBuffer_len:
        len_payload = 0
    else:
        len_payload = 1




    #Desprezar o byte stuffing
    if b'0e0o0p' in rxBuffer_eop:
        rxBuffer_eop.replace(b'0e0o0p', b'eop')



        



    






    

    




    




    # barra = bytearray(b'barra')
    
    delta_t = time.time() - seconds
    


    with open("file_received.txt", "wb") as info:
        info.write(rxBuffer)

    # log
    print ("Lido              {} bytes ".format(nRx))
    
    print (rxBuffer)

    print("EOP localizado na posição {}".format(begin_position))


    

    position_eop = begin_position.to_bytes(length=2,byteorder='big')

    len_payload = len_payload.to_bytes(length=2,byteorder='big')

    data = bytearray()




    data += position_eop
    data += len_payload



    print("Taxa de download: ", rxBuffer_len/delta_t)




    # barra = bytearray(b'barra')


    

    print("Transmitido o tamanho {} para o Server".format(nRx))


    com.sendData(data)

    

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
