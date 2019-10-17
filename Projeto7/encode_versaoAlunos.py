

#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import time


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    signal = signalMeu()

    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freq_amostra = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao os seguintes parametros devem ser setados:
    
    duration = 3 #tempo em segundos que ira emitir o sinal acustico

    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    #nao aceite outro valor de entrada.

    valid_number = False
    while valid_number == False:
        char = input("Qual é o simbolo desejado?")
        if char == "1":
            freq_1 = 1209
            freq_2 = 697
            valid_number = True
        elif char == "2":
            freq_1 = 1336
            freq_2 = 697
            valid_number = True
        elif char == "3":
            freq_1 = 1477
            freq_2 = 697
            valid_number = True
        elif char == "a" or char == "A":
            freq_1 = 1633
            freq_2 = 697
            valid_number = True
        elif char == "4":
            freq_1 = 1209
            freq_2 = 770
            valid_number = True
        elif char == "5":
            freq_1 = 1336
            freq_2 = 770
            valid_number = True
        elif char == "6":
            freq_1 = 1477
            freq_2 = 770
            valid_number = True
        elif char == "b" or char == "B":
            freq_1 = 1633
            freq_2 = 770
            valid_number = True
        elif char == "7":
            freq_1 = 1209
            freq_2 = 852
            valid_number = True
        elif char == "8":
            freq_1 = 1336
            freq_2 = 852
            valid_number = True
        elif char == "9":
            freq_1 = 1477
            freq_2 = 852
            valid_number = True
        elif char == "c" or char == "C":
            freq_1 = 1633
            freq_2 = 852
            valid_number = True
        elif char == "x" or char == "X":
            freq_1 = 1209
            freq_2 = 941
            valid_number = True
        elif char == "0":
            freq_1 = 1336
            freq_2 = 941
            valid_number = True
        elif char == "#":
            freq_1 = 1477
            freq_2 = 941
            valid_number = True
        elif char == "d" or char == "D":
            freq_1 = 1633
            freq_2 = 941
            valid_number = True
        else:
            valid_number = False

    time.sleep(3)
    print("Iniciando o áudio em 3 segundos")

    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array
        
    tb_x, sen_x = signal.generateSin(freq_1, 0.5, duration, freq_amostra)
    tb_y, sen_y = signal.generateSin(freq_2, 0.5, duration, freq_amostra)

    print("Gerando Tom referente ao símbolo : {}".format(char))
    print("Frequencias: {0} + {1}".format(freq_1,freq_2))
    
    
    #construa o sinal a ser reproduzido. nao se esqueca de que é a soma das senoides
    tone = sen_x + sen_y

    #printe o grafico no tempo do sinal a ser reproduzido
    plt.plot(tb_y, tone)
    plt.axis([0.16,0.195,-2,2])
    plt.title("Gráfico de sinal por tempo")

    # reproduz o som
    sd.play(tone, freq_amostra)

    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
