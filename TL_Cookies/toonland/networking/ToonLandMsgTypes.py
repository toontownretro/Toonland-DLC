########################## THE TOON LAND DLC ##########################
# Filename: ToonLandMsgTypes.py
# Created by: Cody/Fd Green Cat Fd (August 1st, 2013)
####
# Description:
#
# Defines all required datagram message types for use with the send
# and receive buffers.
####

from toontown.distributed.ToontownMsgTypes import *

TLMsgName2Id = {
}

MsgName2Id.update(TLMsgName2Id)
MsgId2Names.update(invertDictLossless(TLMsgName2Id))

for name, value in TLMsgName2Id.items():
    exec '%s = %s' % (name, value)