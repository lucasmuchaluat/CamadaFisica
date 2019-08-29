
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
serialName = "COM16"                  # Windows(variacao de)

 #=======================================================
def add_head (payload, total_of_packages, current_package, message):
  txLen = len(payload)

  txLen_bytes = bytes([txLen])
  total_of_packages_bytes = total_of_packages.to_bytes(3, "big")
  current_package_bytes = current_package.to_bytes(3, "big")
#         size*1     + current package*3     + total packages*3        + null bytes*2    + response byte*1 = 10 bytes
  head = txLen_bytes + current_package_bytes + total_of_packages_bytes + bytes([0x00])*2 + bytes([message])
  package = head + payload # + barra

  packageLen = len(package)
  
  return package, txLen, packageLen


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

	current_package = 1
	total_of_packages = 1

	data = bytearray()

	while current_package <= total_of_packages:
		while com.rx.getIsEmpty():
			pass
# size*1 + current package*3 + total packages*3 + null bytes*2 + response byte*1 = 10 bytes
		head, head_size = com.getData(10)
		payload_size = head[0]
		new_current_package = int.from_bytes(head[1:4], "big")
		total_of_packages = int.from_bytes(head[4:7], "big")
		if new_current_package == current_package+1:
			current_package = new_current_package
		else:
			message = bytes([0x04])
		payload_eop, payload_size = com.getData(payload_size+3)
		eop_position = payload_eop.find(b'eop')
		if eop_position == payload_size[0]:
			message = bytes([0x05])
		elif eop_position == -1:
			message = bytes([0x01])
		else:
			message = bytes([0x02])

		payload_eop = payload_eop.replace(b'0e0o0p', b'eop')
		payload = payload_eop[:-3]
		data += payload

		response_head = add_head(bytes([0x00]), total_of_packages, current_package, message)
		response_package = add_eop(response_head)
		com.sendData(response_package)

	# Encerra comunicação
	print("-------------------------")
	print("Comunicação encerrada")
	print("-------------------------")
	com.disable()

if __name__ == "__main__":
	main()
