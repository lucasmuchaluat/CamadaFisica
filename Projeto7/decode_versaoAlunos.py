#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import math
import peakutils
import itertools

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def oneDArray(x):
    return list(itertools.chain(*x))


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    signal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    freqDeAmostragem = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = 3 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    n = 2

    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera

    print("Iniciando captação do áudio em {} segundos.".format(n))
    time.sleep(n)
    
   
    #faca um print informando que a gravacao foi inicializada

    print("Gravação iniciada!")
   
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
   
    
    
    numAmostras = freqDeAmostragem * duration
   
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    
    audio_list = oneDArray(audio)
    
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    inicio = 0
    fim = 3 
    numPontos = len(audio_list)
    t = np.linspace(inicio,fim,numPontos)

    # plot do gravico  áudio vs tempo!

    plt.plot(audio_list, t)
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.show()
    
   
    
    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio_list, sd.default.samplerate)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    indexes = peakutils.indexes(yf, thres=0.2, min_dist=100)
    
    #printe os picos encontrados!

    print(xf[indexes[0]], xf[indexes[1]])
    
    def calcFreq(index, freq):
        dif = math.fabs(freq - index)
        return dif

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla

    
    if calcFreq(xf[indexes[1]], 1209) <= 10 and calcFreq(xf[indexes[0]], 697) <= 10:
        char = "1"
    elif calcFreq(xf[indexes[1]], 1336) <= 10 and calcFreq(xf[indexes[0]], 697) <= 10:
        char = "2"
    elif calcFreq(xf[indexes[1]], 1477) <= 10 and calcFreq(xf[indexes[0]], 697) <= 10:
        char = "3"
    elif calcFreq(xf[indexes[1]], 1633) <= 10 and calcFreq(xf[indexes[0]], 697) <= 10:
        char = "A"
    elif calcFreq(xf[indexes[1]], 1209) <= 10 and calcFreq(xf[indexes[0]], 770) <= 10:
        char = "4"
    elif calcFreq(xf[indexes[1]], 1336) <= 10 and calcFreq(xf[indexes[0]], 770) <= 10:
        char = "5"
    elif calcFreq(xf[indexes[1]], 1477) <= 10 and calcFreq(xf[indexes[0]], 770) <= 10:
        char = "6"
    elif calcFreq(xf[indexes[1]], 1633) <= 10 and calcFreq(xf[indexes[0]], 770) <= 10:
        char = "B"
    elif calcFreq(xf[indexes[1]], 1209) <= 10 and calcFreq(xf[indexes[0]], 852) <= 10:
        char = "7"
    elif calcFreq(xf[indexes[1]], 1336) <= 10 and calcFreq(xf[indexes[0]], 852) <= 10:
        char = "8"
    elif calcFreq(xf[indexes[1]], 1477) <= 10 and calcFreq(xf[indexes[0]], 852) <= 10:
        char = "9"
    elif calcFreq(xf[indexes[1]], 1633) <= 10 and calcFreq(xf[indexes[0]], 852) <= 10:
        char = "C"
    elif calcFreq(xf[indexes[1]], 1209) <= 10 and calcFreq(xf[indexes[0]], 941) <= 10:
        char = "X"
    elif calcFreq(xf[indexes[1]], 1336) <= 10 and calcFreq(xf[indexes[0]], 941) <= 10:
        char = "0"
    elif calcFreq(xf[indexes[1]], 1477) <= 10 and calcFreq(xf[indexes[0]], 941) <= 10:
        char = "#"
    elif calcFreq(xf[indexes[1]], 1633) <= 10 and calcFreq(xf[indexes[0]], 941) <= 10:
        char = "D"
    else:
        char = "Nenhum"

    #print a tecla.
    print(f"O número captado foi {char}")
    
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
