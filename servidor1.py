# Servidor básico em python para escutar porta 80 
#
#  7eAo1200000010173XXXXIIIIIIIIIXXXX7E
#


import socket

HOST = ''
PORT = 81 # porta que escuta http

def sendHTTP(msg):
   resp = ('HTTP/1.1 404 OK\r\n'
           'Content-Type: text/html\r\n'
           'Connection: Close\r\n'  
           '\r\n' 
           '\r\n <html><head><title>'+msg+'</title></head><body><h1>' + msg + '</h1></body></html>\r\n\r\n')
   return resp 


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    
    s.bind((HOST,PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print('Endereco '+ str(addr)+ '\n')
        while True:
            data = conn.recv(1024)    # recebe os dados da conexao 

            if data: 
                msg1 = data.decode()
                if msg1.__contains__('quit'):              # se nao tem mais dados termina                  
                    break

                print('recebendo os dados \n')        
                print(data.decode())
                msg = sendHTTP('OK')
                conn.send(msg.encode())

        conn.close()              