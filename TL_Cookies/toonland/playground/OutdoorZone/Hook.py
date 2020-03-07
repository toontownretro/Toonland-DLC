########################## THE TOON LAND DLC ##########################
# Filename: Hook.py
# Created by: Cody/Fd Green Cat Fd (February 4th, 2013)
####
# Description:
#
# Creates some hooks in the Outdoor Zone safezone modules to
# use our modified DNA file.
####

from direct.task.Task import Task
from toontown.safezone import OZSafeZoneLoader
from toontown.hood import OZHood
from toontown.shtiker import MapPage

def _OZSafeZoneLoader__loadPythonImplementation(task):
    safezone = render.find('**/%d:safe_zone' % PlaygroundGlobals.OUTDOOR_ZONE)
    if safezone:
        filepath = '%s/playground/OutdoorZone/maps' % __modulebase__.replace('\\', '/')
        alphaPath = 'phase_4/maps/tt_t_ara_gen_tunnelAheadSign_a.rgb'
        signTexture = '%s/tt_t_ara_gen_tunnelAheadSign.jpg' % filepath
        tunnelAheadSign = loader.loadTexture(signTexture, alphaPath)
        sign = safezone.find('**/prop_tunnel_ahead_OZ_DNARoot')
        sign.setTexture(tunnelAheadSign, 1)
        return Task.done
    taskMgr.doMethodLater(0.2, _OZSafeZoneLoader__loadPythonImplementation, 'OZ-LPI')

_Hook = OZSafeZoneLoader.OZSafeZoneLoader.__init__

def __init__(self, hood, parentFSM, doneEvent):
    returnCode = _Hook(self, hood, parentFSM, doneEvent)
    filepath = '%s/playground/OutdoorZone/dna' % __modulebase__.replace('\\', '/')
    self.dnaFile = '%s/outdoor_zone_sz.dna' % filepath
    self.safeZoneStorageDNAFile = '%s/storage_OZ_sz.dna' % filepath
    return returnCode

OZSafeZoneLoader.OZSafeZoneLoader.__init__ = __init__
_load = OZSafeZoneLoader.OZSafeZoneLoader.load

def load(self):
    returnCode = _load(self)
    taskMgr.doMethodLater(0.2, _OZSafeZoneLoader__loadPythonImplementation, 'OZ-LPI')
    return returnCode

OZSafeZoneLoader.OZSafeZoneLoader.load = load
__Hook = OZHood.OZHood.__init__

def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
    returnCode = __Hook(self, parentFSM, doneEvent, dnaStore, hoodId)
    self.townLoaderClass = OZTownLoader.OZTownLoader
    return returnCode

OZHood.OZHood.__init__ = __init__
_enter = MapPage.MapPage.enter

def enter(self):
    returnCode = _enter(self)
    if base.localAvatar.getZoneId() == 6101:
        self.hoodLabel['text'] = 'You are in: Chip \'n Dale\'s Acorn Acres Nutty Place'
    return returnCode

MapPage.MapPage.enter = enter