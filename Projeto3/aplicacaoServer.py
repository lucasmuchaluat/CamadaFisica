
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
 #=======================================================
from math import ceil
 #=======================================================

serialName = "COM11"                  # Windows(variacao de)

def check (original, recebida):
	if original == recebida:
		return True
	return False

 #=======================================================
def head (payload, total_of_packages, current_package):
  txLen = len(payload)

  txLen_bytes = bytes([txLen])
  total_of_packages_bytes = total_of_packages.to_bytes(3, "big")
  current_package_bytes = current_package.to_bytes(3, "big")
#         size*1     + current package*3     + total packages*3        + null bytes*2    + response byte*1 = 10 bytes
  head = txLen_bytes + current_package_bytes + total_of_packages_bytes + bytes([0x00])*2 + bytes([0x00])
  package = head + payload # + barra

  packageLen = len(package)
  
  return package, txLen, packageLen
 #=======================================================



def payload_correction (file):
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
 #=======================================================
	data_stuffed_only_len = len(file)
	return buffer, data_stuffed_only_len
 #=======================================================


def add_eop (headfile):
	eop = b'eop'
	package = headfile + eop
	return package


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

	root = Tk()
	root.withdraw

	filename = filedialog.askopenfilename()

	with open (filename, "rb") as img:
		data = img.read()
	
	max_package_size = 128
	data_stuffed, data_stuffed_only_len = payload_correction(data)
	total_of_packages = ceil(data_stuffed_only_len/max_package_size)
	current_package = 1

	while current_package < total_of_packages:
		payload = data_stuffed[max_package_size*current_package:max_package_size*(current_package+1)]
		head_payload = head(payload, total_of_packages, current_package)
		package = add_eop(head_payload)
		com.sendData(package)
		while com.rx.getIsEmpty():
			pass

		response_head, head_size = com.getData(10) # read response head
		message = response_head[9]
		payload_size = response_head[0]
		payload, payload_size = com.getData(payload_size)
		# message interpreter
		if message == 0x01:
			print("0x01: EOP nao existe, por favor, revise o empacotamento!")
		if message == 0x02:
			print("0x02: EOP esta na posicao errada")		
		if message == 0x03:
			print("0x03: Payload não corresponde ao informado no head")
		if message == 0x04:
			print("0x04: Numero errado do pacote")
			package_number_read = int.from_bytes(response_head[1:4], "big")
			current_package = package_number_read
		if message == 0x05:
			print("0x05: Payload corresponde ao informado no head")
			current_package +=1 			
		if message == 0xff:
			print("0xff: sem mensagem")
		else:
			print("mensagem invalida")
 #=======================================================
	



	# data, data_stuffed_only_len = payload_correction(txBuffer)
	# data = eop(data)
	# data, txLen, totalLen = head(data)
	
	# Transmite dado
	# print("tentado transmitir .... {} bytes".format(txLen))
	# seconds = time.time()
	# com.sendData(data)
	

	# # espera o fim da transmissão
	# while(com.tx.getIsBussy()):
	#    pass
	
	
	# # Atualiza dados da transmissão
	# txSize = com.tx.getStatus()
	# print ("Transmitido       {} bytes ".format(txSize))
	# print("Buffer transmitido para o outro Arduino")
	# print("Aguardando a resposta do Client ....")
	# print ("Recebendo dados do Client .... ")

	# delta_t = time.time() - seconds

	# position_eop, nRx_position = com.getData(2)
	# len_payload, nRx_payload = com.getData(2)

	# position_eop_received = int.from_bytes(position_eop, "big")
	# payload_received = int.from_bytes(len_payload, "big")

	# print("Taxa de  envio: {} bytes/segundo".format(payload_only_len/delta_t))

	# overhead = 100*(totalLen/payload_only_len)
	# print("OVERHEAD: {} %".format(overhead))

	# if position_eop_received == 0:
	#   print("EOP nao existe, por favor, revise o empacotamento!")
	# elif position_eop_received == 1:
	#   print("EOP esta na posicao errada")
	# else:
	#   print("EOP beggining position: {}".format(position_eop_received))

	# if payload_received == 0:
	#   print("Payload não corresponde ao informado no head")
	# else:
	#   print("Payload corresponde com o informado no head")


	# Encerra comunicação
	print("-------------------------")
	print("Comunicação encerrada")
	print("-------------------------")
	com.disable()

	#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
	main()
