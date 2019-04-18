# pylint: disable-all

import socket # Import socket module
import _thread as thread
import re


def on_new_client(clientsocket, addr):
    print(addr, ' Connected')
    while True:
        msg = clientsocket.recv(1024)
        msg = msg.decode()
        if re.match(r'.*(\r\n)|(\n)$', msg):
            break

    print(addr, ' >> ', msg)
    clientsocket.send(("Connecting To URL: " + msg if msg=="\r\n" else "brilacasck.ir" + " ...").encode())

    path = "/"
    requestHTTP("brilacasck.ir" if msg=="\r\n" else msg[:-2], path=path)
    clientsocket.send(("Data Is Saved In Path: " + path).encode())

    print(addr, 'X Connection Closed X')
    clientsocket.close()


def requestHTTP(host, path="/", port=80):
    target_host = host 
    target_port = port

    print(target_host, target_port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


    
    # connect the client 
    client.connect((target_host,target_port))  
    # send some data 
    request = "GET "+ path +" HTTP/1.0\r\nHost: %s\r\n\r\n" %target_host
    client.sendall(request.encode())


    # receive some data 
    header = client.recv(8192).decode()
    header_tmp = header.split("\r\n\r\n")
    body= ""
    if len(header_tmp)>1:
        body = header_tmp[1] if len(header_tmp)==2 else "\r\n\r\n".join(header_tmp[1:])
        header = header_tmp[0]

    header = header.splitlines()


    mime = ""
    for el in header:
        if "Content-Type" in str(el):
            mime = el.split(" ")[1]
            mime = mime if ";" not in mime else mime[:-1]

    PREV_RES = ""
    while True:
        res = client.recv(1024*8).decode()
        if res==PREV_RES:
            break
        body += res

    path = path[1:]
    path = path if path else "output"
    output_file = open(path+"."+mime.split("/")[1], "w", encoding="UTF-8")
    

    output_file.write(body)

def main():
    s = socket.socket()         # Create a socket object
    host = "127.0.0.1"          # localhost
    port = 80                # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        thread.start_new_thread(on_new_client, (c, addr))

    s.close()

main()