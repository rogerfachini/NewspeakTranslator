
import SocketServer, time, json

MESSAGE_BUFFER = []

class MyTCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        bufLength = 0
        while True:
            self.data = self.rfile.readline().strip()
            if self.data == '': 
                time.sleep(0.5)
                continue
            print "{} wrote: {}".format(self.client_address[0], self.data)
            try:
                jData = json.loads(self.data)
            except ValueError as er:
                print 'Malformed Packet:', self.data
                continue
            if jData['type'] == 'login':
                #print 'login type'
                self.writeMessage(jData['user'], '<-- %s has Logged In -->' % jData['user'])
            
            if not len(MESSAGE_BUFFER) == bufLength:
                bufDiff = len(MESSAGE_BUFFER) - bufLength
                bufLength = len(MESSAGE_BUFFER)
                for msg in MESSAGE_BUFFER[-bufDiff:]:
                    data = json.dumps(msg)
                    data = data + '\n'
                    print 'written to output: %s' %data
                    self.wfile.write(data)

            time.sleep(0.5)

    def writeMessage(self, user, message):
        MESSAGE_BUFFER.append({'user':user, 'message':message})


if __name__ == "__main__":
    HOST, PORT = "localhost", 9984

    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT),
                                            RequestHandlerClass=MyTCPHandler,
                                            bind_and_activate=False)
 
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
 
    server.serve_forever()
