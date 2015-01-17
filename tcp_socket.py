#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     16/01/2015
# Copyright:   (c) mfell 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket, threading
bind_ip = "0.0.0.0"
bind_port = 9999

def handle_client(client_socket):
    request = client_socket.recv(1024)

    print "[*] Reveived %s" % request
    client_socket.send("ACK!")
    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    print"[*] listening on %s, %d" % (bind_ip, bind_port)

    while True:
        client, addr = server.accept()

        print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])

        client_handler = threading.Thread(target = handle_client, args=(client,))
        client_handler.start()



if __name__ == '__main__':
    main()
