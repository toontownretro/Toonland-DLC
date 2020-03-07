########################## THE TOON LAND DLC ##########################
# Filename: FFSafeZoneLoader.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm safe zone loader. This is where any music, or models are loaded.
####

from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from toontown.safezone import SafeZoneLoader
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from toontown.estate import HouseGlobals
from toontown.estate import DistributedHouse
from toontown.toon.LocalToon import globalClockDelta

CollisionSphereBlockers = [
    ((113.921, 82.753, 10.026), (0, 0, 3, 8)),
    ((64.083, 120.748, 10.026), (0, 0, 3, 17)),
    ((49.946, 132.416, 10.026), (0, 0, 3, 10)),
    ((-90, 62, 10), (0.0, 0.0, 3.0, 5.0))
]
PicnicTablePositions = [
    (81, 7, 10.026, 0, 0, 0),
    (52, 46, 10.026, 40, 0, 0),
    (45, -8, 10.026, 60, 0, 0)
]

HouseGlobals.houseColors.extend([HouseGlobals.houseColors[2], (0.78, 0.52, 0.42), (1.0, 0.453, 0.4)])
HouseGlobals.houseColors2.extend([HouseGlobals.houseColors2[2], (0.58, 0.37, 0.27), (0.9, 0.353, 0.3)])
HouseIndex2Pos = [(-82, 78, 10, -59, 0, 0), (-35, 79, 10, -52, 0, 0), (41, 92, 10, -118, 0, 0)]
HouseIndex2HouseName = ['Doctor Leroy', 'Fluffy', 'Evil Blinky']
HouseIndex2NameText = ["Doctor Leroy's\nLabratory", "Fluffy's Dog\nHouse", "Evil Blinky's\nDen"]

class FFSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __loadPythonImplementation(self, task):
        safeZone = render.find('**/%d:safe_zone' % PlaygroundGlobals.FUNNY_FARM)
        if safeZone:
            toonHq = render.find('**/sz20:toon_landmark_hqFF_DNARoot')
            for doorFrameHole in toonHq.findAllMatches('**/doorFrameHole*'):
                doorFrameHole.hide()
            for houseIndex in range(len(HouseIndex2Pos)):
                self.createDistributedHouse(houseIndex)
            safeZone.find('**/*statue*').removeNode()
            safeZone.find('**/wheelbarrel').find('**/shadow').setDepthWrite(0)
            tunnelNp = safeZone.find('**/linktunnel_ff_19201_DNARoot')
            tunnelNp.find('**/sign').hide()
            tunnelNp.find('**/chip_dale').hide()
            tunnelOrigin = tunnelNp.find('**/tunnel_origin')
            POS = tunnelOrigin.getPos(safeZone)
            HPR = tunnelOrigin.getHpr(safeZone)
            birdNp = safeZone.attachNewNode('linktunnel_ff_19201_DNARoot_bird')
            birdNp.setPosHpr((POS[0] + 5), (POS[1] - 5), POS[2], (HPR[0] - 180), HPR[1], HPR[2])
            birdNp.setScale(350)
            birdNp.setZ(45)
            loader.loadModel('phase_5/models/props/bird').reparentTo(birdNp)
            for collisionBlockerIndex in range(len(CollisionSphereBlockers)):
                collisionBlocker = safeZone.attachNewNode('C.Blocker-' + `collisionBlockerIndex`)
                collisionBlocker.setPos(*CollisionSphereBlockers[collisionBlockerIndex][0])
                cs = CollisionSphere(*CollisionSphereBlockers[collisionBlockerIndex][1])
                cn = CollisionNode('C.Blocker-' + `collisionBlockerIndex`)
                cn.addSolid(cs)
                cn.setIntoCollideMask(OTPGlobals.WallBitmask)
                collisionBlocker.attachNewNode(cn)
            deviceA = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
            deviceA.reparentTo(safeZone)
            deviceA.setPos(-81.5, 61.4, 17.8)
            deviceA.setScale(2.1)
            deviceA.hprInterval(8.0, Vec3(0, 270, 0), Vec3(360, 270, 0)).loop()
            deviceA.find('**/sillyReader').setX(1.4)
            deviceB = loader.loadModel('phase_4/models/props/tt_m_prp_acs_sillyReader')
            deviceB.reparentTo(safeZone)
            deviceB.setPos(-68, 70, 17.8)
            deviceB.setScale(2.1)
            deviceB.hprInterval(8.0, Vec3(0, 270, 0), Vec3(360, 270, 0)).loop()
            deviceB.find('**/sillyReader').setX(1.4)
            toonHall = loader.loadModel('phase_3.5/models/modules/tt_m_ara_int_toonhall')
            tallSpaceLamp = toonHall.find('**/prop_tallLamp_space').copyTo(safeZone)
            for nodePath in (tallSpaceLamp.findAllMatches('**/tallLamp') + tallSpaceLamp.findAllMatches('**/collision')):
                nodePath.setPos(76, -22, 0)
            tallSpaceLamp.setPos(-75, 74, 12)
            tallSpaceLamp.setScale(1.2)
            spaceLamp = toonHall.find('**/prop_lamp_space').copyTo(safeZone)
            for nodePath in (spaceLamp.findAllMatches('**/lamp') + spaceLamp.findAllMatches('**/collision')):
                nodePath.setPos(76.6, -36, -2.45)
            spaceLamp.setPos(-86.5, 67.5, 15.8)
            spaceLamp.setH(180)
            collisionBlocker = safeZone.attachNewNode('collision_blocker_1')
            fountainMickey = safeZone.find('**/prop_garden_mickey_shovel_FF_DNARoot')
            fountainMickey.find('**/fountain_mickey_v1s1:mickey').setP(270)
            self.setupFountainSplash()
            dgaFountain = ToonLandRepository.ToonLandRepository.createDistributedObject(
             className='DistributedGeyserFountain', parentId=base.localAvatar.defaultShard,
             zoneId=PlaygroundGlobals.FUNNY_FARM, doId=NetworkingGlobals.DISTRIBUTED_GEYSER_FOUNTAIN_ID,
             sendFormatGenerate=False)
            dgaFountain.reparentTo(safeZone)
            dgaFountain.setPosHpr(41, 12, 10.026, 0, 0, 0)
            dgaFountain.setScale(1.2)
            trashCan = ToonLandRepository.ToonLandRepository.createDistributedObject(
             className='DistributedHiccupTrashCan', parentId=base.localAvatar.defaultShard,
             zoneId=PlaygroundGlobals.FUNNY_FARM, doId=NetworkingGlobals.DISTRIBUTED_HICCUP_TRASH_CAN_ID,
             sendFormatGenerate=False)
            trashCan.reparentTo(safeZone)
            trashCan.setPosHpr(72, 30, 10.025, -812, 0, 0)
            trashCan.setScale(1.1)
            for tn in range(1, 4): # This actually returns [1, 2, 3], which are the picnic table numbers in the safe zone DNA.
                self.createDistributedPicnicBasket(tn)
            self.makeGoldenBean(safeZone)
            return Task.done
        taskMgr.doMethodLater(0.2, self._FFSafeZoneLoader__loadPythonImplementation, 'FF-LPI')
 
    def makeGoldenBean(self, parentId):
        facade = loader.loadModel("phase_3.5/models/modules/facade_bN.bam")
        facade.reparentTo(parentId)
        facade.setPosHpr(130, -56 ,10, -95, 0, 0)
        facade.find('**/showcase').setTwoSided(True)
        goldenbean = loader.loadModel("phase_4/models/props/jellybean4.bam")
        goldenbean.reparentTo(facade)
        goldenbean.setPos(0, -1.5, 4)
        goldenbean.setH(90)
        goldenbean.setScale(5)
        goldenbean.setBillboardAxis(1.5)
        goldenbean.setColor(1,0.9,0)
        glow = loader.loadModel("phase_3.5/models/props/glow.bam")
        glow.reparentTo(facade)
        glow.setPos(0,-1.37,4.1)
        glow.setScale(3)
        glow.setBillboardAxis(1.65)
        glow.setColor(1,0.9,0)
        goldenbean.hprInterval(3,Point3(0,0,0),startHpr=Point3(360,0,0)).loop()

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = FFPlayground.FFPlayground
        filepath = '%s/playground/funnyfarm/bgm' % __modulebase__.replace('\\', '/')
        self.musicFile = '%s/FF_nbrhood.mp3' % filepath
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        filepath = '%s/playground/funnyfarm/dna' % __modulebase__.replace('\\', '/')
        self.dnaFile = '%s/funny_farm_sz.dna' % filepath
        self.safeZoneStorageDNAFile = '%s/storage_FF_sz.dna' % filepath

    def enter(self, requestStatus):
        SafeZoneLoader.SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.SafeZoneLoader.exit(self)

    def load(self):
        SafeZoneLoader.SafeZoneLoader.load(self)
        self.birdSound = map(base.loadSfx, ['phase_4/audio/sfx/SZ_TC_bird1.mp3',
         'phase_4/audio/sfx/SZ_TC_bird2.mp3', 'phase_4/audio/sfx/SZ_TC_bird3.mp3'])
        self.houseModels = [loader.loadModel('phase_5.5/models/estate/houseB')]
        self.houseNode = []
        for houseIndex in range(len(HouseIndex2Pos)):
            nodePath = render.attachNewNode('esHouse_%d' % houseIndex)
            nodePath.setPosHpr(*HouseIndex2Pos[houseIndex])
            self.houseNode.append(nodePath)
        self.houseId2house = {}
        taskMgr.doMethodLater(0.2, self._FFSafeZoneLoader__loadPythonImplementation, 'FF-LPI')

    def unload(self):
        del self.birdSound
        SafeZoneLoader.SafeZoneLoader.unload(self)

    def createDistributedHouse(self, houseIndex):
        # This isn't a real DistributedHouse object, we only use this for creating
        # the house models easier.
        distObj = DistributedHouse.DistributedHouse(ToonLandRepository.ToonLandRepository)
        distObj.setHousePos(houseIndex)
        distObj.setHouseType(0)
        distObj.setAvatarId(0)
        distObj.setName(HouseIndex2HouseName[houseIndex])
        distObj.setColor((len(HouseGlobals.houseColors) - 3) + houseIndex)
        ToonLandRepository.ToonLandRepository.createDistributedObject(distObj=distObj,
         parentId=base.localAvatar.defaultShard, zoneId=PlaygroundGlobals.FUNNY_FARM,
         doId=((houseIndex + 1) << 20), sendFormatGenerate=False)
        distObj.load()
        distObj.nameText.setText(HouseIndex2NameText[houseIndex])
        distObj.house.setScale(choice(houseIndex, 1, 1.1))

    def createDistributedPicnicBasket(self, tn):
        distObj = DistributedFFPicnicBasket.DistributedFFPicnicBasket(ToonLandRepository.ToonLandRepository)
        distObj.setTableNumber(tn)
        distObj.setPosHpr(*PicnicTablePositions[(tn - 1)])
        ToonLandRepository.ToonLandRepository.createDistributedObject(distObj=distObj,
         parentId=base.localAvatar.defaultShard, zoneId=PlaygroundGlobals.FUNNY_FARM,
         doId=eval('NetworkingGlobals.DISTRIBUTED_FF_PICNIC_BASKET_%d' % tn), sendFormatGenerate=False)
        distObj.setState('waitEmpty', tn, globalClockDelta.getFrameNetworkTime())

    def setupFountainSplash(self):
        # This was added as a just-for-fun sort of thing. Whenever the Toon enters this
        # (rather large) collision sphere, a splash is emitted. Feel free to re-code this
        # if you have a better way of doing so. ~ Cody
        triggerName = 'fountainSplash_trigger'
        fountain = render.find('**/prop_funny_farm_fountain_DNARoot')
        cs = CollisionSphere(-33.0, 12.0, -27, 39.5)
        cs.setTangible(0)
        cn = CollisionNode(triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        trigger = fountain.attachNewNode(cn)
        base.localAvatar.accept(('enter%s' % triggerName), self.handleSplashEffect)

    def handleSplashEffect(self, collisionEntry):
        X, Y = base.localAvatar.getX(), base.localAvatar.getY()
        base.localAvatar.playSplashEffect(X, Y, 10)
        base.localAvatar.d_playSplashEffect(X, Y, 10)