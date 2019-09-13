
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################
from enlace import *
import time
import datetime


#timer
time_init = time.time()
timer = time.time() - time_init


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)



 #=======================================================
def add_head (type_msg, payload, total_of_packages, current_package, server_id):
  txLen = len(bytes([payload]))
  txLen_bytes = bytes([txLen])

  total_of_packages_bytes = total_of_packages.to_bytes(3, "big")
  current_package_bytes = current_package.to_bytes(3, "big")

  server_id_bytes = bytes([server_id])

  type_msg_bytes = bytes([type_msg])

#          tipo*1       +   server_id*1   +  size*1     +   current package*3   + total packages*3        + null bytes*2 = 11 bytes
  head = type_msg_bytes + server_id_bytes + txLen_bytes + current_package_bytes + total_of_packages_bytes + bytes([0x00])*2
  
  package = head + bytes([payload])
  
  return package


def add_eop (headfile):
	eop = b'eop'
	package = headfile + eop
	return package
 #=======================================================


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

	#=======================================================
	#Define variables

	serverNumber = 1
	clientNumber = 1
	ocioso = True
	finish = False
	
	#=======================================================
	log = open("log_server.txt", "w")
	#=======================================================
	#Define functions
#  def add_head (type_msg, payload, total_of_packages, current_package, server_id
# 
#  ):
	def send_message_2 ():
		headfile = add_head(2,0,0,0,0)
		message_2 = add_eop(headfile)
		print("enviando mensagem 2")
		com.sendData(message_2)
		datetime_object = datetime.datetime.now()
		log.write(f"Msg: tipo 2 -- enviada: {datetime_object} –- destinatário: {clientNumber}\n")
		

	def send_message_4 (current_package):
		headfile = add_head(4,0,0,current_package,0)
		message_4 = add_eop(headfile)
		print("enviando mensagem 4")
		com.sendData(message_4)
		datetime_object = datetime.datetime.now()
		log.write(f"Msg: tipo 4 -- enviada: {datetime_object} –- destinatário: {clientNumber}\n")

	def send_message_5 ():
		headfile = add_head(5,0,0,0,0)
		message_5 = add_eop(headfile)
		print("enviando mensagem 5")
		com.sendData(message_5)
		datetime_object = datetime.datetime.now()
		log.write(f"Msg: tipo 5 -- enviada: {datetime_object} –- destinatário: {clientNumber}\n")

	def send_message_6 (expected_package):
		headfile = add_head(6,0,0,expected_package,0)
		message_6 = add_eop(headfile)
		print("enviando mensagem 6")
		com.sendData(message_6)
		datetime_object = datetime.datetime.now()
		log.write(f"Msg: tipo 6 -- enviada: {datetime_object} –- destinatário: {clientNumber}\n")
	
	#=======================================================

	while finish == False:
		while ocioso == True:
			while com.rx.getIsEmpty():
				pass
			head, head_size = com.getData(15)
			msg_type = head[0]
			identifier = head[1]
			total_of_packages = int.from_bytes(head[6:9], "big")

			datetime_object = datetime.datetime.now()
			log.write(f"Msg: tipo {msg_type} -- recebida: {datetime_object} –- remetente: {clientNumber}\n")

			if msg_type == 0x01:
				if identifier == serverNumber:
					ocioso = False
				else:
					print("esta mensagem não era para mim!")
			else:
				print("não esperava esse tipo de mensagem")
		send_message_2()
		while ocioso == False:

			current_package = 0

			data = bytearray()
			
			time_init1 = time.time()
			time_init2 = time.time()

			while current_package < total_of_packages:
				while com.rx.getIsEmpty():
					timer2 = time.time() - time_init2
					if timer2 > 20:
						ocioso = True
						send_message_5()
						finish = True
					else:
						timer1 = time.time() - time_init1
						if timer1 > 2:
							print("ENVIANDO MENSAGEM 4 DO WHILE EMPTY")
							send_message_4(current_package)
							time_init1 = time.time()
					pass

				print("recebeu alguma mensagem")
		# tipo*1   +   server_id*1   +  size*1   +   current package*3   + total packages*3 + null bytes*2 = 11 bytes
				head, head_size = com.getData(11)
				msg_type = head[0]

				datetime_object = datetime.datetime.now()
				log.write(f"Msg: tipo {msg_type} -- recebida: {datetime_object} –- remetente: {clientNumber}\n")

				if msg_type == 3:
					print('processando mensagem tipo 3')
					payload_size = head[2]
					new_current_package = int.from_bytes(head[3:6], "big")
					total_of_packages = int.from_bytes(head[6:9], "big")
					if new_current_package == current_package+1:
						current_package = new_current_package

						payload_eop, payload_size = com.getData(payload_size+3)
						eop_position = payload_eop.find(b'eop')
						if eop_position == payload_size-3:
							send_message_4(current_package)
						elif eop_position == -1:
							send_message_6(current_package+1)
						else:
							send_message_6(current_package+1)

						payload_eop = payload_eop.replace(b'0e0o0p', b'eop')
						payload = payload_eop[:-3]
						data += payload

						print(f"DATA {current_package}: {data}")
						print(f"pacote {current_package} de {total_of_packages} recebido e processado! Aguardando o próximo...")

					else:
						print(current_package)
						send_message_6(current_package+1)
			print("SUCESSO!")
			ocioso = True
			finish = True
			log.close()

		with open("data_received.txt", "wb") as info:
			info.write(data)

	# Encerra comunicação
	print("-------------------------")
	print("Comunicação encerrada")
	print("-------------------------")
	com.disable()

if __name__ == "__main__":
	main()
