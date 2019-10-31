#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

# Importe todas as bibliotecas
from suaBibSignal import *
from scipy import signal as sig
import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import math
import peakutils
import itertools


# funcao para transformar intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

# converte o sinal de audio em um array
def oneDArray(x):
    return list(itertools.chain(*x))


def main():
    signal = signalMeu()
    freqDeAmostragem = 44100

    sd.default.samplerate = 44100  # taxa de amostragem
    sd.default.channels = 1
    n = 2

    print("Iniciando captação do áudio em {} segundos.".format(n))
    time.sleep(n)

    # Recebendo audio modulado
    print("Gravação iniciada!")

    audio, samplerate = sf.read('modulado.wav')  # Audio

    print("Gravação terminada!")

    audio_list = []
    for e in audio:
        audio_list.append(e)
    audio_list = np.array(audio_list)

    # Normalizando o sinal modulado recebido
    max_amplitude = max(abs(audio_list))
    data_normalized = audio_list/max_amplitude  # Normalizado

    # Demodulando o sinal normalizado
    t, portadora = signal.generateSin(
        14000, 1, len(audio_list)/freqDeAmostragem, freqDeAmostragem)  # portadora de 14000 Hz

    demodulado = data_normalized * portadora

    # Filtro passa baixa
    fc = 4000
    w = fc / (freqDeAmostragem / 2)
    b, a = sig.butter(5, w, 'low')
    tempf = sig.filtfilt(b, a, np.array(demodulado))  # Filtrado

    # Executando audio demodulado
    print("Aguarde a reprodução do áudio...")
    sd.play(tempf, freqDeAmostragem)
    sd.wait()

    print("Gerando gráficos...")

    # plot do gravico audio captado vs tempo
    plt.plot(t, audio_list)
    plt.title("captado x tempo")
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.show()

    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio_list, freqDeAmostragem)
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()

    # plot do gravico  demodulado vs tempo
    plt.plot(t, tempf)
    plt.title("demodulado x tempo")
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.show()

    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(tempf, freqDeAmostragem)
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()


if __name__ == "__main__":
    main()
