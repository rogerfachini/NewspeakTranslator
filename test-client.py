
import socket
import sys
import json, time, curses

from Client import GUI

HOST, PORT = "localhost", 9984
USERNAME = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)

#try:
    # Connect to server and send data
    
    

    # Receive data from the server and shut down
    #received = sock.recv(1024)
    #finally:
    #sock.close()

class SocketClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.setblocking(0)
        
    def connect(self):
        self.sendPacket('login', USERNAME)
        self.recvLoop()

    def sendPacket(self, pType, user, message=""):
        if pType == 'login':
            msg = {'type': pType, 'user':user}
        elif pType == 'message':
            msg = {'type': pType, 'user':user, 'message':message}
        else:
            print 'Bad packet type:', pType
            return
        mStr = json.dumps(msg)
        self.sock.sendall(mStr + "\n")

    def recvLoop(self):
        rBuffer = ''
        while True:
            time.sleep(0.5)
            try:
                received = self.sock.recv(4096)
                a = received.split('\n')
                for msg in a:
                    rData = json.loads(msg)
                    self.handlePacket(rData)
            except socket.error:
                continue
            except ValueError as er:
                #print 'Malformed Packet:', received
                continue
            

    def handlePacket(self, packet):
        print packet


class GUISocketClient(SocketClient):
    gui = None
    def setGui(self, guiOBJ):
        self.gui = guiOBJ

    def handlePacket(self, packet):
        if self.gui == None: 
            print 'NO GUI AVAILABLE'
            return
        self.gui.printGUIChatMessage('%s | %s' % (packet['user'], packet['message']))




if __name__ == '__main__':
    try:
        g = GUI()
        s = GUISocketClient(HOST, PORT)
        s.setGui(g)
        s.connect()
    except BaseException as er:
        print er
    finally:

        g.killGUI()
        print er
        s.sock.close()