from UDP_unpacker import unpackUDPpacket
import threading

class visualiser(threading.Thread):
    def __init__(self):
        super().__init__(name="visualiser")
        self.packet = None
        self.unpacked = None
    def accept_packet(self, packet):
        self.packet = packet
        self.unpacked = unpackUDPpacket(self.packet)
    def type(self):
        print(self.unpacked.header.sessionUID)
