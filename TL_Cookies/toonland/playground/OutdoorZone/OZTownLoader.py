########################## THE TOON LAND DLC ##########################
# Filename: OZTownLoader.py
# Created by: Cody/Fd Green Cat Fd (February 10th, 2013)
####
# Description:
#
# The Outdoor Zone town loader module. This handles all of the street loading.
####

from pandac.PandaModules import *
from direct.task.Task import Task
from toontown.town import TownLoader
from toontown.suit import Suit

class OZTownLoader(TownLoader.TownLoader):

    __TreeTransforms = (
        (12, 2, 20, 0.6), (-12, -16, 20, 0.7), (-8, 6, 20, 0.5),
        (0, -10, 20, 0.4, 0.4, 0.5), (52, 35, 20, 0.8), (-28, -22.5, 20, 0.8),
        (-24, 0, 20, 0.4), (-8, -3, 20, 0.4), (-36, -101, 20, 0.8),
        (-66, -66, 20, 0.8), (-76, -30, 20, 1.0), (-62, -84, 20, 0.6),
        (15, -50, 20, 0.5, 0.5, 0.6), (75, -15, 20, 0.9), (8, 70, 20, 1.0),
        (75, 15, 20, 0.7), (-10, -130, 20, 1.0), (25, -122, 20, 0.8)
    )
    __TreeCollisions = (((2, 0, 20), (0, 0, 0, 15)), ((-4, 0, 20), (0, 0, 0, 15)),
        ((-12, 0, 20), (0, 0, 0, 15)), ((-20, -4, 20), (0, 0, 0, 15)),
        ((-28, -10, 20), (0, 0, 0, 15)), ((-36, -12, 20), (0, 0, 0, 15)),
        ((-44, -12, 20), (0, 0, 0, 15)), ((50, 45, 20), (0, 0, 0, 15)),
        ((-45, -100, 20), (0, 0, 0, 15))
    )

    def __loadPythonImplementation(self, task):
        town = render.find('**/town_top_level')
        if town and (base.localAvatar.getZoneId() in (6101,)):
            z = 40
            parentNp = loader.loadModel('phase_6/models/golf/golf_hub2')
            for background in parentNp.findAllMatches('**/*background*'):
                background.reparentTo(town)
                background.setZ(z)
                z += 20
            for transform in self._OZTownLoader__TreeTransforms:
                self.loadPineTree(town, *transform)
            for collision in self._OZTownLoader__TreeCollisions:
                dummyNp = town.attachNewNode('prop_outdoor_zone_tree_collision')
                dummyNp.setPos(*collision[0])
                treeSphereNode = dummyNp.attachNewNode(CollisionNode('tree_sphere'))
                treeSphereNode.node().addSolid(CollisionSphere(*collision[1]))
            for picnicTable in town.findAllMatches('**/prop_picnic_table_OZ_DNARoot'):
                tableCloth = picnicTable.find('**/basket_locator')
                tableClothSphereNode = tableCloth.attachNewNode(CollisionNode('tablecloth_sphere'))
                tableClothSphereNode.node().addSolid(CollisionSphere(0, 0, 0, 5.5))
            return Task.done
        taskMgr.doMethodLater(0.2, self._OZTownLoader__loadPythonImplementation, 'OZ-LPI')

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = OZStreet.OZStreet
        filepath = '%s/playground/OutdoorZone/bgm' % __modulebase__.replace('\\', '/')
        self.musicFile = '%s/OZ_SZ.mp3' % filepath
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.mid'
        filepath = '%s/playground/OutdoorZone/dna' % __modulebase__.replace('\\', '/')
        self.townStorageDNAFile = '%s/storage_OZ_town.dna' % filepath

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        filepath = '%s/playground/OutdoorZone/dna' % __modulebase__.replace('\\', '/')
        dnaFile = ('%s/outdoor_zone_' % filepath) + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)
        taskMgr.doMethodLater(0.2, self._OZTownLoader__loadPythonImplementation, 'OZ-LPI')

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)

    def loadPineTree(self, parent, x, y, z, *scale):
        parentNp = loader.loadModel('phase_6/models/golf/outdoor_zone_entrance')
        treeNp = parentNp.find('**/outdoor_zone_entrance_tree1')
        if not scale:
            treeNp.setScale(0.5)
        else:
            treeNp.setScale(*scale)
        dummyNp = parent.attachNewNode('prop_outdoor_zone_tree')
        dummyNp.setPos((x + 10), (y - 5), z)
        treeNp.reparentTo(dummyNp)