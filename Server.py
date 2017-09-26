#Newspeak Chat server (run one instance only)

import socket, logging, json


class ChatServer:
    def __init__(self):
        self.socket = None

    def handlePacket(self, message):
        #Handles a raw packet from a
        try:
            data = json.loads(message)
        except BaseException as er:
            print "JSON decode error: ", er
            return

        if not data.hasKey('type'): 
            raise BaseException("Invalid Packet Type")
        if data['type'] == 'message':
            self.recieveChatMessage(data['sender'], data['target'], data['message'])
        
    def recieveChatMessage(self, source, target, message):
        #Processes a given chat message. Performs translation and censoring

    def sendChatMessageTo(self, source, target, message):
        #Send chat message to destination


