########################## THE TOON LAND PROJECT ##########################
# Filename: FFPicnicBasket.py
# Created by: Cody/Fd Green Cat Fd (February 12th, 2013)
####
# Description:
#
# This is the client-side code for the picnic tables in Funny Farm.
####

from toontown.safezone import PicnicBasket

class FFPicnicBasket(PicnicBasket.PicnicBasket):

    def enter(self):
        self.fsm.enterInitialState()
        if base.localAvatar.hp > 0:
            self.fsm.request('requestBoard')
            messenger.send('enterPicnicTableOK_%d_%d' % (self.tableNumber, self.seatNumber))
        else:
            self.fsm.request('trolleyHFA')