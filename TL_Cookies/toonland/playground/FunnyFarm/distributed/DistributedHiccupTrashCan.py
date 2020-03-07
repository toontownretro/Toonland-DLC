########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedHiccupTrashCan.py
# Created by: Cody/Fd Green Cat Fd (August 2nd, 2013)
####
# Description:
#
# This is the trash can in Funny Farm that plays a hiccup animation
# when approached.
####

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from direct.distributed import DistributedNode
from otp.otpbase import OTPGlobals

class DistributedHiccupTrashCan(Actor, DistributedNode.DistributedNode):

    def __init__(self, tlr):
        DistributedNode.DistributedNode.__init__(self, tlr)
        Actor.__init__(self, 'phase_5/models/char/tt_r_ara_ttc_trashcan',
                      {'hiccup':'phase_5/models/char/tt_a_ara_ttc_trashcan_idleHiccup0'})
        self.waitDuration = self.getDuration('hiccup')
        self.hiccupPlaying = False

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        self.triggerName = self.uniqueName('trigger')
        cs = CollisionSphere(0.0, 0.0, -1.4, 3.0)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        trigger = self.attachNewNode(cn)
        self.accept('enter%s' % self.triggerName, self.handleEnterSphere)

    def handleEnterSphere(self, collisionEntry):
        self.b_requestHiccup()

    def toggleHiccupPlaying(self):
        self.hiccupPlaying = not self.hiccupPlaying

    def b_requestHiccup(self):
        self.requestHiccup()
        self.d_requestHiccup()

    def d_requestHiccup(self):
        self.sendUpdate('requestHiccup')

    def requestHiccup(self):
        if self.hiccupPlaying:
            return None
        self.toggleHiccupPlaying()
        self.hiccupTrack = Sequence(Func(self.play, 'hiccup'),
         Wait(self.waitDuration), Func(self.toggleHiccupPlaying))
        self.hiccupTrack.start()