
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
import datetime
 #=======================================================
from math import ceil
from PyCRC.CRC16 import CRC16
 #=======================================================

##   python -m serial.tools.list_ports
serialName = "COM13"                  # Windows(variacao de)

def check (original, recebida):
	if original == recebida:
		return True
	return False

 #=======================================================
def head (payload, total_of_packages, current_package, type_msg, server_id, CRC):
  txLen = len(payload)


  type_msg_bytes = type_msg.to_bytes(1, "big")
  server_id_bytes = server_id.to_bytes(1, "big")

  txLen_bytes = bytes([txLen])
  total_of_packages_bytes = total_of_packages.to_bytes(3, "big")
  current_package_bytes = current_package.to_bytes(3, "big")
  CRC_bytes = CRC.to_bytes(2, "big")
#         	tipo*1			server_id*1  	size*1     + current package*3     + total packages*3         + crc * 2   + response byte*6 = 17 bytes
  head = type_msg_bytes + server_id_bytes + txLen_bytes + current_package_bytes + total_of_packages_bytes + CRC_bytes + bytes([0x00])*6
  package = head + payload # + barra

  packageLen = len(package)
  
  return package #, txLen, packageLen
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

	

	

	server_id = 1




	def type1(server_id, total_of_packages):
		
		type_msg = 1

		payload = bytes([0])
		
		current_package = 1

		crc = 0

		head_payload = head(payload, total_of_packages, current_package, type_msg, server_id, crc)
		package = add_eop(head_payload)
		com.sendData(package)
		return package



	def type3(data, total_of_packages, data_stuffed, max_package_size, current_package):

		type_msg = 3
		server_id = 1
		



		#while current_package <= total_of_packages:
		payload = data_stuffed[max_package_size*(current_package-1):max_package_size*(current_package)]
		payload = bytes(payload)

		crc = CRC16().calculate(payload)

		head_payload = head(payload, total_of_packages, current_package, type_msg, server_id, crc)

		package = add_eop(head_payload)

		

		com.sendData(package)
		
		# print(f"package: {package}")
		# while com.rx.getIsEmpty():
		# 	pass

		# response_head, head_size = com.getData(10) # read response head
		# message = response_head[9]

		# #type_msg = response_head[7]

		# payload_size = response_head[2]

		# print(f"response head: {response_head}")
		# print(f"payload size: {payload_size}")

		# payload, payload_size = com.getData(payload_size)
		# eop_read, eop_size = com.getData(3)

		# print(f"current package: {current_package}")
		# print(f"total of package: {total_of_packages}")




	def type5():
		message = total_of_packages
		type_msg = 5

		payload = bytes([0])
		total_of_packages = 0
		current_package = 0
		crc = 0

		head_payload = head(payload, total_of_packages, current_package, type_msg, server_id, crc)
		package = add_eop(head_payload)
		return package



###############################################################################

	inicia = False

	max_package_size = 128
	data_stuffed, data_stuffed_only_len = payload_correction(data)
	total_of_packages = ceil(data_stuffed_only_len/max_package_size)
	current_package = 0

	
	




	log = open("log_client.txt", "w")

	

	#Primeiro bloco
	while not inicia:

		datetime_object = datetime.datetime.now()
		
		log.write(f'Msg: mensagem tipo 1 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
		print(f'Msg: mensagem tipo 1 – enviada: {datetime_object}  – destinatário: Servidor 1\n')

		

		type1(server_id, total_of_packages)
		time.sleep(5)


		response_head, head_size = com.getData(21)
		type_msg = response_head[0]
		com.rx.clearBuffer()


		if type_msg == 0x02:
			inicia = True

			datetime_object = datetime.datetime.now()
			log.write(f'Msg: mensagem tipo 2 – recebida: {datetime_object}  – remetente: Servidor 1\n')
			print(f'Msg: mensagem tipo 2 – recebida: {datetime_object}  – remetente: Servidor 1\n')

	current_package = 1


	#Segundo bloco
	while current_package <= total_of_packages:
		type3(data, total_of_packages, data_stuffed, max_package_size, current_package)
		
		datetime_object = datetime.datetime.now()
		log.write(f'Msg: mensagem tipo 3 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
		print(f'Msg: mensagem tipo 3 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
	

		time_init1 = time.time()
		time_init2 = time.time()

		response_head, head_size = com.getData(15)
		type_msg = response_head[0]
		com.rx.clearBuffer()

		if type_msg == 0x04:
			datetime_object = datetime.datetime.now()
			log.write(f'Msg: mensagem tipo 4 – recebida: {datetime_object}  – remetente: Servidor 1\n')
			print(f'Msg: mensagem tipo 4 – recebida: {datetime_object}  – remetente: Servidor 1\n')
			current_package = int.from_bytes(response_head[3:6], "big")
			current_package += 1
			
			
			
			

		elif type_msg == 0x06:
			datetime_object = datetime.datetime.now()
			log.write(f'Msg: mensagem tipo 6 – recebida: {datetime_object}  – remetente: Servidor 1\n')
			print(f'Msg: mensagem tipo 6 – recebida: {datetime_object}  – remetente: Servidor 1\n')
			right_package_bytes = response_head[3:6]
			right_package = int.from_bytes(right_package_bytes, "big")

			type3(data, total_of_packages, data_stuffed, max_package_size, right_package)
			time_init1 = time.time()
			time_init2 = time.time()
		
		else:
			timer1 = time.time() - time_init1
			print("Não recebeu mensagem tipo 4 ou 6")
			if timer1 > 5:
				datetime_object = datetime.datetime.now()
				log.write(f'Msg: mensagem tipo 3 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
				print(f'Msg: mensagem tipo 3 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
				type3(data, total_of_packages, data_stuffed, max_package_size, current_package)

				print("Timer 1 resetado e enviando mensagem tipo 3 novamente...")
				time_init1 = time.time()
				

			timer2 = time.time() - time_init2
			if timer2 > 20:
				type5()
				datetime_object = datetime.datetime.now()
				log.write(f'Msg: mensagem tipo 5 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
				print(f'Msg: mensagem tipo 5 – enviada: {datetime_object}  – destinatário: Servidor 1\n')
				print("Conexão finalizada por timeout")
				print("Timer 2 resetado")
				print("variável total of packages recebe zero")
				com.disable()
				
				time_init2 = time.time()
				total_of_packages = 0

		


	log.close()
	print("Sucesso!!")
	






###############################################################################
		




		



	






# 	while current_package <= total_of_packages:
# 		payload = data_stuffed[max_package_size*(current_package-1):max_package_size*(current_package)]


# 		if type_msg == 0x01:

# 			com.sendData(package)
			
# 			print(f"package: {package}")
# 			while com.rx.getIsEmpty():
# 				pass


# 			time.sleep(5)



# 		if delta_t1 == 5:
# 			if type_msg == 0x02:
# 				type_msg = 3
# 				head_payload = head(payload, total_of_packages, current_package, type_msg, server_id)
# 				print("Servidor pronto para receber payload")
# 				continue

# 		if type_msg == 0x04: #and current_round == 4:
# 			if #timer > 20:
# 				type_msg = 5
# 				#TODO: colocar numero 5 no lugar da mensagem e finalizar conexao
# 				print("Excedeu tempo limite de espera")
# 		elif type_msg == 0x06:
# 			print("Erro no pacote (verifique quantidade de bytes, formato, pacote correto")
# 			#TODO: colocar numero 6 no lugar da mensagem e o numero correto do pacote esperado pelo servidor
# 		elif type_msg == 0x05:
# 			pass

# 		if type_msg == 0x03:

			
			
		
		


		
# 			package = add_eop(head_payload)
# 			com.sendData(package)
			
# 			print(f"package: {package}")
# 			while com.rx.getIsEmpty():
# 				pass

# 			response_head, head_size = com.getData(10) # read response head
# 			message = response_head[9]

# 			type_msg = response_head[7]

# 			payload_size = response_head[0]
# 			print(f"response head: {response_head}")
# 			print(f"payload size: {payload_size}")
# 			payload, payload_size = com.getData(payload_size)
# 			eop_read, eop_size = com.getData(3)
# 			print(f"current package: {current_package}")
# 			print(f"total of package: {total_of_packages}")
# 			# message interpreter
# 			print("Interpreting message")
# 			if message == 0x01:
# 				print("0x01: EOP nao existe, por favor, revise o empacotamento!")
# 			elif message == 0x02:
# 				print("0x02: EOP esta na posicao errada")		
# 			elif message == 0x03:
# 				print("0x03: Payload não corresponde ao informado no head")
# 			elif message == 0x04:
# 				print("0x04: Numero errado do pacote")
# 				package_number_read = int.from_bytes(response_head[1:4], "big")
# 				current_package = package_number_read
# 			elif message == 0x05:
# 				print("0x05: Payload corresponde ao informado no head")
# 				current_package +=1 			
# 			elif message == 0xff:
# 				print("0xff: sem mensagem")
# 			else:
# 				print("mensagem invalida")
# 			print("")
#  #=======================================================
	




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