########################## THE TOON LAND DLC ##########################
# Filename: FFTownLoader.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# The Funny Farm town loader module. This handles all of the street loading.
####

from direct.task.Task import Task
from toontown.town import TownLoader
from toontown.suit import Suit

class FFTownLoader(TownLoader.TownLoader):

    def __loadPythonImplementation(self, task):
        town = render.find('**/town_top_level')
        townId = (base.localAvatar.getZoneId() % PlaygroundGlobals.FUNNY_FARM)
        townId -= (townId % 100)
        if town and (0 <= townId < 1000):
            filepath = '%s/playground/funnyfarm/maps/' % __modulebase__
            sidewalkTexture = loader.loadTexture(filepath + 'sidewalkyellow.jpg')
            for tunnelNode in render.findAllMatches('**/linktunnel*'):
                tunnelNode.find('**/tunnel_floor*').setTexture(sidewalkTexture, 1)
        if town and (townId == 100):
            toonHq = render.find('**/tb42:toon_landmark_hqFF_DNARoot')
            if toonHq:
                for doorFrameHole in toonHq.findAllMatches('**/doorFrameHole*'):
                    doorFrameHole.hide()
            return Task.done
        taskMgr.doMethodLater(0.2, self._FFTownLoader__loadPythonImplementation, 'FF-LPI')

    def __init__(self, hood, parentFSM, doneEvent):
        TownLoader.TownLoader.__init__(self, hood, parentFSM, doneEvent)
        self.streetClass = FFStreet.FFStreet
        filepath = '%s/playground/funnyfarm/bgm' % __modulebase__.replace('\\', '/')
        self.musicFile = '%s/FF_SZ.mp3' % filepath
        self.activityMusicFile = '%s/FF_SZ_activity.mp3' % filepath
        filepath = '%s/playground/funnyfarm/dna' % __modulebase__.replace('\\', '/')
        self.townStorageDNAFile = '%s/storage_FF_town.dna' % filepath

    def load(self, zoneId):
        TownLoader.TownLoader.load(self, zoneId)
        Suit.loadSuits(1)
        filepath = '%s/playground/funnyfarm/dna' % __modulebase__.replace('\\', '/')
        dnaFile = ('%s/funny_farm_' % filepath) + str(self.canonicalBranchZone) + '.dna'
        self.createHood(dnaFile)
        taskMgr.doMethodLater(0.2, self._FFTownLoader__loadPythonImplementation, 'FF-LPI')

    def unload(self):
        Suit.unloadSuits(1)
        TownLoader.TownLoader.unload(self)