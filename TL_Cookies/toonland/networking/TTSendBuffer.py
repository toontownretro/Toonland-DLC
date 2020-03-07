########################## THE TOON LAND DLC ##########################
# Filename: TTSendBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the sending of messages to all clients "interested" in this
# client's location. We must prioritize both speed, and security in this
# communication system.
####

import struct
import zlib
from types import StringType
from direct.distributed.ClockDelta import globalClockDelta
from toontown.toon import LocalToon

class TTSendBuffer:

    __ClientHeader = '\xe4'
    __FormatMessage = 'a=%d|b=%s'

    def __init__(self):
        self._d_setParent = LocalToon.LocalToon.d_setParent
        LocalToon.LocalToon.d_setParent = lambda *x:self.d_setParent(*x)

    def d_setParent(self, newSelf, parentToken):
        if type(parentToken) != StringType:
            return self._d_setParent(newSelf, parentToken)
        self._d_setParent(newSelf, parentToken)
        self._d_setParent(newSelf, 2)

    def sendDatagram(self, datagram):
        base.localAvatar.d_setParent(self.__ClientHeader + zlib.compress(
         HackerCrypt.encrypt(self.__FormatMessage % (globalClockDelta.getRealNetworkTime(),
         (struct.pack('I', base.localAvatar.doId) + datagram.getMessage())))))