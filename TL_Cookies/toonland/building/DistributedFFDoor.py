from toontown.building import DistributedDoor
from toontown.building.DoorTypes import *

class DistributedFFDoor(DistributedDoor.DistributedDoor):

    def __init__(self, tlr):
        DistributedDoor.DistributedDoor.__init__(self, tlr)
        self.tlr = tlr
        self.cr = base.cr

    def sendUpdate(self, fieldName, args=[], sendToId=None):
        # This is needed in re-writes of Disney distributed objects.
        self.tlr.send(self.dclass.clientFormatUpdate(fieldName, sendToId or self.doId, args))