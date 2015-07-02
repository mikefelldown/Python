#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     18/04/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import socket

def main():
    s = socket.socket()

    host = socket.gethostname()
    port = 1234

    s.bind((host, port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        print 'Got connection from', addr
        c.send("Connection established with host")
        c.close()

if __name__ == '__main__':
    main()
