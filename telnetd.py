from twisted.internet import protocol, reactor, endpoints
import logging
import random

class Telnetd(protocol.Protocol):
    logging.basicConfig(filename='telnetd_honeypot.log',level=logging.DEBUG,format='%(message)s')
    PROMPT = "/ # "
    BANNER = "\n\nBusyBox v1.15.3 (2013-04-03 20:26:55 CST) built-in shell (ash)\nEnter 'help' for a list of built-in commands.\n\n/ # "
    def dataReceived(self, data):
        data = data.strip()
        if data == "id":
            self.transport.write("uid=0(root) gid=0(root) groups=0(root)\n")
        elif data.split(" ")[0] == "wget":
            self.transport.write("wget: missing URL\nUsage: wget [OPTION]... [URL]...\nTry `wget --help' for more options.\n")
        elif data.split(" ")[0] == "/bin/busybox":
            self.transport.write(data.split(" ")[1] + " applet not found\n")
        elif data.split(" ")[0] == "echo":
            self.transport.write(data.split(" ")[1] + "\n")
        elif data == "uname -a":
            self.transport.write("Linux DreamBox 2.6.32.59 #2 Mon Jul 2 18:37:44 CST 2012 mips GNU/Linux\n")
        elif data == "uname":
            self.transport.write("Linux\n")
        elif data == "uname -r":
            self.transport.write("2.6.32.59\n")
        elif data == "exit":
            self.transport.loseConnection()
        elif data.split(" ")[0] == "ls":
            self.transport.write("bin    etc    media  proc   sys    usr    www\ndev    lib    mnt    sbin   tmp    var\n")
        else:

        self.transport.write(Telnetd.PROMPT)

        if data != "":
           logging.info(data)



    def connectionMade(self):
        self.transport.write(Telnetd.BANNER)
class TelnetdFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Telnetd()

print("Listening...")
endpoints.serverFromString(reactor, "tcp:8023").listen(TelnetdFactory())
reactor.run()
