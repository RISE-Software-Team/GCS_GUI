import os
import struct
from enum import Enum
from collections import namedtuple

class FlightStage(Enum):
    STANDBY   = 0
    LAUNCH    = 1
    ASCENT    = 2
    COAST     = 3
    DESCENT   = 4
    TOUCHDOWN = 5

TelemetryPacket = namedtuple(
    'TelemetryPacket',
    ['timestamp','pitch','roll','yaw','altitude','accelX','accelY','accelZ','stage']
)

class TelemetryReceiver:
    PACKET_SIZE = 9*4 + 1  # 9 floats x 4 bytes each, plus 1 byte

    def __init__(self, fd):
        self.fd = fd
        self.last = None

    def read(self):
        # Block until we have exactly PACKET_SIZE bytes, unpack, and return a TelemetryPacket.
        buf = bytearray()
        while len(buf) < self.PACKET_SIZE:
            chunk = os.read(self.fd, self.PACKET_SIZE - len(buf))
            if not chunk:
                raise IOError("No data received")
            buf.extend(chunk)

        # Unpack: '<' = little-endian; '9f' = nine floats; 'B' = one unsigned byte
        values = struct.unpack('<9fB', bytes(buf))
        stage = FlightStage(values[-1])           # last element is the enum byte
        pkt = TelemetryPacket(*values[:-1], stage)  
        self.last = pkt
        return pkt

    def get_acceleration(self):
        pkt = self.last or self.read()
        return (pkt.accelX, pkt.accelY, pkt.accelZ)

    def get_barometer(self):
        pkt = self.last or self.read()
        return pkt.altitude

    def get_attitude(self):
        pkt = self.last or self.read()
        return {'roll': pkt.roll, 'pitch': pkt.pitch, 'yaw': pkt.yaw}

    def get_stage(self):
        pkt = self.last or self.read()
        return pkt.stage.name
