import struct 
import socket
import sys
import _thread
import xml.etree.ElementTree as ET
from util import *



def sendXML(msg):
   resp = ('HTTP/1.1 200 OK\r\n'
           'Content-Type: text/xml\r\n'
           'Connection: close\r\n'  
           '\r\n' + msg)
   return resp 

def deviceXml():
    msg = (
        '<?xml version=\"1.0\"?>'
        '<root>'
                '<device>'
                '<deviceType>'+urn2()+'</deviceType>' #urn:schemas-upnp-org:device:BinaryLight:1
                '<friendlyName>Slmm tomada</friendlyName>'
                '<manufacturer>Slmm Sistemas</manufacturer>'
                '<modelName>tomada virtual</modelName>'
                '<modelNumber>3.1415</modelNumber>'
                '<UDN>uuid:'+slmm_uuid()+'</UDN>'           
                '<serviceList>'
                    '<service>'
                        '<serviceType>'+urn()+'</serviceType>' #schemas-upnp-org:service:SwitchPower:1
                        '<serviceId>'+urnId()+'</serviceId>' #
                        '<SCPDURL>'+SCPDURL()+'</SCPDURL>'
                        '<controlURL>'+controlURL()+'</controlURL>'
                        '<eventSubURL>'+eventSubURL()+'</eventSubURL>'
                    '</service>'
                '</serviceList>'
            '</device>'
        '</root>')
    return msg


eventservice_xml = (
   '<scpd xmlns=\"urn:Slmm:service-1-0\">'
    '<specVersion>'
       '<major>1</major>'
       '<minor>0</minor>'
    '</specVersion>'
    '<actionList>'
      '<action>'
       '<name>SetEstado</name>'
       '<argumentList>'
        '<argument>'
            '<retval />'
            '<name>Estado</name>'
            '<relatedStateVariable>Estado</relatedStateVariable>'
            '<direction>in</direction>'
        '</argument>'
       '</argumentList>'
      '</action>'
    '<action>'
        '<name>GetEstado</name>'
        '<argumentList>'
         '<argument>'
            '<retval/>'
            '<name>Estado</name>'
            '<relatedStateVariable>Estado</relatedStateVariable>'
            '<direction>out</direction>'
         '</argument>'
        '</argumentList>'
     '</action>'
    '<action>'
        '<name>GetLevel</name>'
        '<argumentList>'
         '<argument>'
            '<retval/>'
            '<name>Level</name>'
            '<relatedStateVariable>Level</relatedStateVariable>'
            '<direction>out</direction>'
         '</argument>'
        '</argumentList>'
     '</action>'     
    '</actionList>'
    '<serviceStateTable>'
        '<stateVariable sendEvents=\'yes\'>'
            '<name>Estado</name>'
            '<dataType>Boolean</dataType>'
            '<defaultValue>0</defaultValue>'
        '</stateVariable>'
        '<stateVariable sendEvents=\'yes\'>'
            '<name>Level</name>'
            '<dataType>string</dataType>'
            '<defaultValue>"alo"</defaultValue>'
        '</stateVariable>'
    '</serviceStateTable>'
   '</scpd>')


def statusResponse(Status): 
    return (
    '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
    '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
    '<s:Body>'
    '<u:GetEstadoResponse xmlns:u=\"'+urn()+'\">'
    '<Estado>'+Status+'</Estado>'
    '</u:GetEstadoResponse>'
    '</s:Body>'
    '</s:Envelope>')

def LevelResponse(Status): 
    return (
    '<?xml version=\"1.0\" encoding=\"utf-8\"?>'
    '<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">'
    '<s:Body>'
    '<u:GetLevelResponse xmlns:u=\"'+urn()+'\">'
    '<Level>'+Status+'</Level>'
    '</u:GetLevelResponse>'
    '</s:Body>'
    '</s:Envelope>')


# Estado dispositivo 
#  Ligado True
#  Desligado False
estado_dispotivo = False 


# definir o procedimento que será usado para tratar
# uma chamda socket na porta 8080 ( servidor http)
def on_new_client(clientsocket, addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg:
            print ('porta '+str(get_port())+' ->'+str(addr) + ' >>' + msg.decode() )
            break;
        else:
            break;
    msg1 = msg.decode()
    print(msg1)
    if msg1.find('/setup.xml') > 0:
        msgToSend = sendXML(deviceXml())    
        clientsocket.send(msgToSend.encode())
        print('\r\n'+msgToSend)
        print('\r\n Terminado o setup.xml')

    if msg1.find('/eventoservice.xml') > 0:
                msg = sendXML(eventservice_xml)    
                clientsocket.send(msg.encode())
                print(msg)
            
    if msg1.find('/controle/evento') > 0:
        global estado_dispotivo
        pos = msg1.find('s:encodingStyle')
        msg1 = msg1[:pos] + ' ' + msg1[pos:]
        inicio = msg1.find('<?xml')
        resp = msg1[inicio:1000]
        root = ET.fromstring(resp)
        root_tag = root.tag
        achei = False
        for child in root:
            for ch2 in child:
                str4 = ch2.tag
                if str4.find('SetEstado') > 0:
                    for ch3 in ch2:
                        valor = int(ch3.text)
                        if valor == 1:
                            estado_dispotivo = True
                        else:
                            estado_dispotivo = False  
                if str4.find('GetLevel') > 0:                            
                    achei = True                    
            # decodifica a msg e liga ou deliga o led
            # retorna o status de ligado ou nao 
        if not achei:    
            if (estado_dispotivo):
                msg = sendXML(statusResponse("1"))    
                print('\nTurn On -> tomada\n')
            else:
                msg = sendXML(statusResponse("0"))        
                print('\nTorn Off -> tomada\n')
        else:
            msg = sendXML(LevelResponse("Certo"))        
            print('\nGet Level acionada -> tomada\n')


        clientsocket.send(msg.encode())
        

    clientsocket.close()
    return
