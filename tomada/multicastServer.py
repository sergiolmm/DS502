import struct 
import socket

# para o random delay
import random
from time import sleep
import time

from util import *

group = '239.255.255.250'
mport = 1900

def retornaPesquisa(_host,_port,_page):
    msg = (
      'HTTP/1.1 200 OK\r\n'
      'CACHE-CONTROL: max-age=86400\r\n'
      'DATE: '+time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())+'\r\n'
      'EXT:\r\n'
      'LOCATION: http://'+_host+':'+_port+'/'+_page+'\r\n'
      'OPT: \"http://schemas.upnp.org/upnp/1/0/\"; ns=01\r\n'
     # '01-NLS: Socket-1_0-'+slmm_uuid()+'\r\n'      #36be2d5a-b318-40e2-90ae-a9d5414e74d9
      'SERVER: Unspecified, UPnP/1.0, Unspecified\r\n'
     # 'X-User-Agent: redsonic\r\n'
      'ST: '+urn()+'\r\n'
      'USN: uuid:Socket-1_0-'+slmm_uuid()+'::'+urn()+'\r\n'
     # 'Content-length: 0\r\n'
         
      '\r\n'
    )
    return msg

def brokeHttp2(str):
    lista = {}
    while True:
        x = str.find('\r\n')
        if x < 2:
            break
        if str.__contains__('M-SEARCH'):
            lista['M-SEARCH'] = str[len('M-SEARCH'):x].lstrip()
        if str.__contains__('NOTIFY'):
            lista['NOTIFY'] = str[len('NOTIFY'):x].lstrip()            
        else:
           pos = str.find(':')                
           lista[str[:pos].upper()] = str[pos+1:x].lstrip()
        str = str[x+2:]

    return lista   



def multicastServer():

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.bind((group,mport))
        print('bind '+group+ ' \n')
    except socket.error as e:
        print("Couldnt connect with the socket-server: %s\n terminating program" % e)
        sock.bind(('0.0.0.0', mport))
        print('bind local 0.0.0.0\n') 
    
    print('Pronto para escutar na porta '+ str(mport)+'\n')

    mreq = struct.pack("4sl",  socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    
    tentativas =0;    
    while True:
        (data, address) = sock.recvfrom(2000)
        if data:
           # print(str(address) + ' >>'+'\n')           
            httpRequesDecode = brokeHttp2(data.decode())
            #print(httpRequesDecode)
            achou = False
            for x in httpRequesDecode:
                if (x == 'M-SEARCH'):
                   achou = True
            #       print('achou\n')
            if achou:
                if (httpRequesDecode['M-SEARCH'] =='* HTTP/1.1'):
             #       print('ok1')
                    if (httpRequesDecode['MAN'] =='"ssdp:discover"'):
             #           print('ok2 -> ' + httpRequesDecode['ST'])
                        if (httpRequesDecode['ST'] =='ssdp:all') or (httpRequesDecode['ST'] =='upnp:rootdevice'):
              #             print('ok3') 
                           time_to_wait = float(httpRequesDecode['MX'])
                           delay = random.uniform(0.0, time_to_wait)
                           sleep(delay)
                           msgPesq = retornaPesquisa(get_ip2(), str(get_port()),'setup.xml')
                           sock.sendto( msgPesq.encode(), address)
                           tentativas = tentativas + 1
                           print('enviando dados '+str(tentativas)+ ' - '+address[0] + '\r\n'+msgPesq)
