########################## THE TOON LAND DLC ##########################
# Filename: TTRecvBuffer.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# Handles the receiving of messages. We must prioritize both speed,
# and security in this communication system.
#
# Note: This is not where you should handle datagram receives. To handle
#       datagram receives, go to ./ToonLandRepository.py
####

from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed import DistributedNode
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from toontown.speedchat import TTSCDecoders

class TTRecvBuffer:

    def __init__(self):
        self._setParentStr = DistributedNode.DistributedNode.setParentStr
        DistributedNode.DistributedNode.setParentStr = lambda *x:self.setParentStr(*x)
        self._decodeTTSCToontaskMsg = TTSCDecoders.decodeTTSCToontaskMsg
        TTSCDecoders.decodeTTSCToontaskMsg = lambda *x:self.decodeTTSCToontaskMsg(*x)

    def setParentStr(self, newSelf, parentTokenStr):
        if not self.recv(newSelf.doId, parentTokenStr):
            return self._setParentStr(newSelf, parentTokenStr)

    def decodeTTSCToontaskMsg(self, taskId, toNpcId, toonProgress, msgIndex):
        # This is our alternative communication system. Primarily, it is used for sending messages
        # to clients that aren't in the area.
        return self._decodeTTSCToontaskMsg(taskId, toNpcId, toonProgress, msgIndex)

    def recv(self, senderId, message):
        if not message.startswith(TTSendBuffer.TTSendBuffer._TTSendBuffer__ClientHeader):
            return False
        message = message[len(TTSendBuffer.TTSendBuffer._TTSendBuffer__ClientHeader):]
        try:
            a, b = HackerCrypt.decrypt(zlib.decompress(message)).split('|', 1)
            exec(a) # This will be something like 'a=timestamp'.
            b = b[(b.index('=') + 1):] # This is our datagram net string.
        except:
            return True
        if (a - globalClockDelta.getRealNetworkTime()) > 400:
            return True # Why has this message been re-sent? It's old.
        # We still have to be pretty careful. This message might be corrupt?
        try:
            datagram = PyDatagram(b)
            dgi = PyDatagramIterator(datagram)
            # This will verify that the sender IS the sender.
            if dgi.getUint32() != senderId:
                return True
            ToonLandRepository.ToonLandRepository.handleDatagram(senderId, dgi)
        except:
            return True
        return True