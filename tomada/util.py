import struct
import socket

#import uuid
#print(uuid.uuid4())

def get_port():
    return 8083   # porta ip para servidor HTTP


def get_ip2():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))    
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    return IP

def urn():
    msg = ( 'urn:Slmm:service:evento:1')
    return msg

def urnId():
    msg = ( 'urn:Slmm:serviceId:evento1')
    return msg

def urn2():
    msg = ( 'urn:Slmm:device:controllee:1')
    return msg

def serviceType():
    return urn()

def servicdId():
    return urnId()    

def controlURL():
    return "/controle/evento"
def eventSubURL():
    return "/evento/evento"
def SCPDURL():
    return "/eventoservice.xml"

def slmm_uuid():
    msg = ('481bed27-e778-412a-bb09-36c26c3d7c10')
    return msg    