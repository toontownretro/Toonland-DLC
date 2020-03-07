########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedFFPicnicBasket.py
# Created by: Cody/Fd Green Cat Fd (August 2nd, 2013)
####
# Description:
#
# This is the server-side code for the picnic tables in Funny Farm.
####

from toontown.safezone import DistributedPicnicBasket
from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM, State
from toontown.toon.LocalToon import globalClockDelta

class DistributedFFPicnicBasket(DistributedPicnicBasket.DistributedPicnicBasket):

    def __init__(self, tlr):
        DistributedObject.DistributedObject.__init__(self, tlr)
        self.tlr = tlr
        self.cr = base.cr
        self.fullSeat2doId = ([0] * 4)
        self.gotClockTime = False
        self.localToonOnBoard = 0
        self.seed = 0
        self.random = None
        self.picnicCountdownTime = ToontownGlobals.PICNIC_COUNTDOWN_TIME
        self.picnicBasketTrack = None
        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolley', [
         State.State('off', self.enterOff, self.exitOff, ['waitEmpty', 'waitCountdown']),
         State.State('waitEmpty', self.enterWaitEmpty, self.exitWaitEmpty, ['waitCountdown']),
         State.State('waitCountdown', self.enterWaitCountdown, self.exitWaitCountdown, ['waitEmpty'])], 'off', 'off')
        self.fsm.enterInitialState()
        self._DistributedPicnicBasket__toonTracks = {}

    def sendUpdate(self, fieldName, args=[], sendToId=None):
        # This is needed in re-writes of Disney distributed objects.
        self.tlr.send(self.dclass.clientFormatUpdate(fieldName, sendToId or self.doId, args))

    def handleEnterPicnicTable(self, i):
        if not self.fullSeat2doId[i]:
            self.b_setAvatarState(i, 1)

    def handleExitButton(self):
        if base.localAvatar.doId in self.fullSeat2doId:
            self.b_setAvatarState(self.fullSeat2doId.index(base.localAvatar.doId), 0)
            self.clockNode.hide()

    def doneExit(self, avId):
        return None

    def d_setClockTime(self, receiverId, clockTime):
        self.sendUpdate('setClockTime', [base.localAvatar.doId, receiverId, clockTime])

    def setClockTime(self, senderId, receiverId, clockTime):
        if (not self.gotClockTime) and (senderId in self.fullSeat2doId) and (receiverId == base.localAvatar.doId):
            if not self.clockNode.currentTime:
                self.fsm.request('waitCountdown', [globalClockDelta.getFrameNetworkTime()])
            self.clockNode.countdown(clockTime, self.handleExitButton)
            self.gotClockTime = True

    def b_setAvatarState(self, slotIndex, isBoarded):
        self.setAvatarState(base.localAvatar.doId, slotIndex, isBoarded)
        self.d_setAvatarState(slotIndex, isBoarded)

    def d_setAvatarState(self, slotIndex, isBoarded):
        self.sendUpdate('setAvatarState', [base.localAvatar.doId, slotIndex, isBoarded])

    def setAvatarState(self, avId, slotIndex, isBoarded):
        if isBoarded:
            if self.fullSeat2doId[slotIndex]:
                return None
            if not self.clockNode.currentTime:
                self.fsm.request('waitCountdown', [globalClockDelta.getFrameNetworkTime()])
            if base.localAvatar.doId in self.fullSeat2doId:
                self.d_setClockTime(avId, self.clockNode.currentTime)
            self.fullSeat2doId[slotIndex] = avId
            self.fillSlot(slotIndex, avId)
        else:
            if self.fullSeat2doId[slotIndex] != avId:
                return None
            if avId == base.localAvatar.doId:
                base.cr.playGame.getPlace().trolley.disableExitButton()
            self.fullSeat2doId[slotIndex] = 0
            ts = globalClockDelta.getFrameNetworkTime()
            if self.fullSeat2doId == ([0] * 4):
                self.clockNode.stop()
                self.clockNode.reset()
                self.setState('waitEmpty', self.seed, ts)
            self.emptySlot(slotIndex, avId, ts)