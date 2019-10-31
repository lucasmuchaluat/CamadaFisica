# importe as bibliotecas
from suaBibSignal import *
from scipy import signal as sig
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import time
import soundfile as sf
from pydub import AudioSegment
from scipy import signal as sig
import itertools


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

# converte intensidade em Db
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

# converte o sinal de audio em um array
def oneDArray(x):
    return list(itertools.chain(*x))


def main():
    print("Inicializando encoder")

    signal = signalMeu()
    freq = 44100

    # Leitura de um arquivo de áudio
    data, samplerate = sf.read('audio.wav')  # Audio

    print("samplerate de ", samplerate)

    data = oneDArray(data)
    data = np.array(data)

    # Normalizando esse sinal
    max_amplitude = max(abs(data))
    data_normalized = data/max_amplitude  # Normalizado

    # Filtrando as altas frequências do sinal (acima de 4000 Hz)
    fc = 4000
    w = fc / (samplerate / 2)
    b, a = sig.butter(5, w, 'low')
    tempf = sig.filtfilt(b, a, np.array(data_normalized))  # Filtrado

    # Codificando esse sinal de áudio em AM (portadora de 14000 Hz)
    nyq_rate = freq/2
    width = 5.0/nyq_rate
    ripple_db = 60.0  # dB
    N, beta = sig.kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = sig.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = sig.lfilter(taps, 1.0, data_normalized)

    tempo, sinall = signal.generateSin(14000, 1, len(yFiltrado)/freq, freq) # Portadora

    modulated = sinall * yFiltrado  # AM modulado
    
    # Reproduzindo audio modulado
    print("Iniciando a reprodução do audio modulado...")
    sd.play(modulated, freq)
    sd.wait()

    # Salvando o áudio modulado
    sf.write('modulado.wav', modulated, 44100)

    # Frequencia e amplitude audio original
    xf, yf = signal.calcFFT(np.array(data), 44100)

    # lista tempo
    numPontos = len(data)
    t = np.linspace(0, 3, numPontos)

    # Grafico no dominio do tempo do audio original
    plt.plot(t, data)
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.title('Audio original')
    plt.show()

    # Grafico domínio da frequencia do audio original
    plt.figure("F(y)")
    plt.plot(xf, yf)
    plt.grid()
    plt.title('Fourier audio original')
    plt.show()

    # Grafico no dominio do tempo do audio normalizado
    plt.plot(t, data_normalized)
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.title('Audio normalizado')
    plt.show()

    # frequencia e amplitude audio normalizado
    xf_n, yf_n = signal.calcFFT(np.array(data_normalized), 44100)

    # Grafico domínio da frequencia do audio normalizado
    plt.figure("F(y)")
    plt.plot(xf_n, yf_n)
    plt.grid()
    plt.title('Fourier audio normalizado')
    plt.show()

    # Grafico no dominio do tempo do audio filtrado
    plt.plot(t, tempf)
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.title('Audio filtrado')
    plt.show()

    # frequencia e amplitude audio filtrado
    xf_f, yf_f = signal.calcFFT(np.array(tempf), 44100)

    # Grafico domínio da frequencia do audio filtrado
    plt.figure("F(y)")
    plt.plot(xf_f, yf_f)
    plt.grid()
    plt.title('Fourier audio filtrado')
    plt.show()

    # Grafico no dominio do tempo do audio modulado
    plt.plot(t, modulated)
    plt.xlabel('Tempo')
    plt.ylabel('Áudio')
    plt.title('Audio modulado')
    plt.show()

    # frequencia e amplitude audio modulado
    xf_m, yf_m = signal.calcFFT(np.array(modulated), 44100)

    # Grafico domínio da frequencia do audio modulado
    plt.figure("F(y)")
    plt.plot(xf_m, yf_m)
    plt.grid()
    plt.title('Fourier audio modulado')
    plt.show()

if __name__ == "__main__":
    main()
