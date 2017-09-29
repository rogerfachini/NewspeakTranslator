import curses, time, threading


class GUI:
    MSG_BUFFER = []
    CMD_BUFFER = []
    def __init__(self):
        self.guiThread = threading.Thread(target=self.runGUI, args=(()))
        self.guiThread.setDaemon(True)
        self.guiThread.start()

    def runGUI(self):
        try:
            win = curses.initscr()
            win.nodelay(1)
            curses.noecho()
            mY, mX = win.getmaxyx()
            bufferLength = len(self.MSG_BUFFER)
            while True: 
                i = 0
                for message in self.MSG_BUFFER[-mY+1:]:
                    #print message, bufferLength - bufferDiff + i
                    win.addstr(i, 0, str(message).ljust(mX))
                    win.refresh()
                    i += 1
                win.addstr(mY-1, 0, str('>' + ''.join(self.CMD_BUFFER)).ljust(mX-1))
                ch = win.getch()
                if ch == 10:
                    self.handleCommand(''.join(self.CMD_BUFFER))
                    self.CMD_BUFFER = []
                elif ch == 127:
                    try:
                        self.CMD_BUFFER.pop(-1)
                    except IndexError: pass
                elif not ch == -1:
                    self.CMD_BUFFER.append(chr(ch))
                    
                time.sleep(0.05)
        finally:
            curses.endwin()

    def printGUIChatMessage(self, message):
        self.MSG_BUFFER.append(message)

    def handleCommand(self, command):
        self.printGUIChatMessage(command)

    def killGUI(self):
        curses.endwin()

class Client:
    def __init__(self):
        pass


if __name__ == '__main__':
        c = GUI()