########################## THE TOON LAND PROJECT ##########################
# Filename: DistributedGeyserFountain.py
# Created by: Cody/Fd Green Cat Fd (August 2nd, 2013)
####
# Description:
#
# This is the fountain in Funny Farm that emits a geyser animation
# when approached.
####

import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed import DistributedNode
from direct.actor.Actor import Actor
from otp.otpbase import OTPGlobals

class DistributedGeyserFountain(DistributedNode.DistributedNode):

    def __init__(self, tlr):
        DistributedNode.DistributedNode.__init__(self, tlr)
        NodePath.__init__(self, 'dgaFountain')
        self.geyserEffectPlaying = False
        self.geyserTrack = None

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        self.geyserModel = loader.loadModel('phase_6/models/golf/golf_geyser_model')
        self.geyserSound = loader.loadSfx('phase_6/audio/sfx/OZ_Geyser_No_Toon.mp3')
        self.fountainModel = loader.loadModel('phase_8/models/props/tt_m_ara_dga_fountain')
        self.fountainModel.reparentTo(self)
        self.fountainModel.find('**/fountainHead_dga').removeNode()
        geyserPlacer = self.attachNewNode('geyserPlacer')
        geyserPlacer.setPos(0, 0, 4)
        self.geyserSoundInterval = SoundInterval(self.geyserSound, node=geyserPlacer,
         listenerNode=base.camera, seamlessLoop=False, volume=0.6, cutOff=120)
        self.geyserActor = Actor(self.geyserModel)
        self.geyserActor.loadAnims({'idle':'phase_6/models/golf/golf_geyser'})
        self.geyserActor.reparentTo(geyserPlacer)
        self.geyserActor.setScale(0.01)
        self.geyserActor.setPlayRate(8.6, 'idle')
        self.geyserActor.loop('idle')
        self.geyserActor.setDepthWrite(0)
        self.geyserActor.setTwoSided(True, 11)
        self.geyserActor.setColorScale(1)
        self.geyserActor.setBin('fixed', 0)
        mesh = self.geyserActor.find('**/mesh_tide1')
        joint = self.geyserActor.find('**/uvj_WakeWhiteTide1')
        mesh.setTexProjector(mesh.findTextureStage('default'), joint, self.geyserActor)
        self.geyserActor.setZ(geyserPlacer.getZ() - 10.0)
        self.geyserPos = geyserPlacer.getPos()
        self.geyserPlacer = geyserPlacer
        self.triggerName = self.uniqueName('trigger')
        cs = CollisionSphere(0, 0, -1.4, 4)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        trigger = self.attachNewNode(cn)
        self.accept('enter%s' % self.triggerName, self.handleEnterSphere)

    def handleEnterSphere(self, collisionEntry):
        self.b_playGeyserEffect()

    def toggleGeyserEffectPlaying(self):
        self.geyserEffectPlaying = not self.geyserEffectPlaying

    def b_playGeyserEffect(self):
        self.playGeyserEffect()
        self.d_playGeyserEffect()

    def d_playGeyserEffect(self):
        self.sendUpdate('playGeyserEffect')

    def playGeyserEffect(self):
        if self.geyserEffectPlaying:
            return None
        self.toggleGeyserEffectPlaying()
        time, maxSize = 1, 0.12
        self.geyserTrack = Sequence()
        upPos = Vec3(self.geyserPos[0], self.geyserPos[1], (self.geyserPos[2] - 8.0))
        downPos = Vec3(self.geyserPos[0], self.geyserPos[1], (self.geyserPos[2] - 8.0))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2 * time), 0.1, 0.01),
         LerpPosInterval(self.geyserActor, (2 * time), pos=downPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2 * time), 0.1, maxSize),
         LerpPosInterval(self.geyserActor, (2 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (2 * time), 0.1, maxSize),
         LerpPosInterval(self.geyserActor, (2 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, time, maxSize, 0.1),
         LerpPosInterval(self.geyserActor, time, pos=upPos, startPos=downPos)))
        self.geyserTrack.append(Parallel(LerpScaleInterval(self.geyserActor, (4 * time), 0.01, maxSize),
         LerpPosInterval(self.geyserActor, (4 * time), pos=downPos, startPos=upPos)))
        self.geyserTrack.append(Func(self.toggleGeyserEffectPlaying))
        self.geyserTrack.start()
        self.geyserSoundInterval.start()