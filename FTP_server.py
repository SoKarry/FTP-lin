import socket
import file_manager as fm


def process(req):
    if req == 'pwd':
        return 's'
    return 'bad request'


PORT = 6666
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("Прослушиваем порт", PORT)
conn, addr = sock.accept()

while True:
    send_fl = False
    command = conn.recv(1024).decode()
    size = conn.recv(1024).decode()
    file = conn.recv(int(size))
    if command.split()[0] == "get_from_server":
        response = fm.manage(command)
        if isinstance(response, (bytes, bytearray)):
            conn.send(str(len(response)).encode())
            conn.send(response)
            continue
        else:
            conn.send("-1".encode())
            conn.send(response.encode())
            continue
    print(f"request {command}")
    if file:
        response = fm.manage(command, file)
    else:
        response = fm.manage(command)
    if not response:
        response = "ok"
    conn.send(response.encode())
    conn.send(fm.inp_check().encode())

conn.close()