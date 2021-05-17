import socket
import os
HOST = 'localhost'
PORT = 6666
sock = socket.socket()
sock.connect((HOST, PORT))
inp = "~$: "
try:
    os.mkdir("ftp_cl_downloads")
except:
    pass
while True:
    get_fl = False
    request = input(inp)
    if "send_to_server" == request.split()[0]:
        try:
            with open(request.split()[1], 'rb') as f:
                file = f.read()
        except:
            print('Такого файла не существует!')
    else:
        file = b''
    if "get_from_server" == request.split()[0]:
        get_fl = True
    sock.send(request.encode())
    print(f"send1: {len(file)}")
    sock.send(str(len(file)).encode())
    print(f"send2: {file}")
    sock.send(file)
    if get_fl:
        size = sock.recv(1024).decode()
        if size == "-1":
            print(sock.recv(1024).decode())
        file = sock.recv(int(size))
        with open("ftp_cl_downloads\\"+request.split()[1].split("\\")[-1], "wb") as f:
            f.write(file)
        continue
    response = sock.recv(1024).decode()
    if response != "ok":
        print(response)
    inp = sock.recv(1024).decode()
sock.close()