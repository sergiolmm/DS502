# projeto de emulação de um device upnp
#  by Turma INFO-2019 TI 502
#
#  criar dois servidores para tratar as chamadas
#  primeiro UDP para multicast
#  segundo  HTTP server para as requisições e controle
import socket
import struct
import _thread


from util import *
from multicastServer import *
from newclient import * 

print(socket.gethostbyname_ex(socket.gethostname()) )
print(socket.gethostbyname_ex(socket.gethostname())[2][0])

_thread.start_new_thread(multicastServer,())


# criar o servidor HTTP
sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockHttp.bind((get_ip2(),get_port()))
    print('porta '+str(get_port())+' ativa '+get_ip2())
except socket.error:
    sockHttp.bind(('',get_port()))
    print('local host porta '+str(get_port())+' ativa')
sockHttp.listen(1)

while True:
    client, addr = sockHttp.accept()
    _thread.start_new_thread(on_new_client,(client,addr))

