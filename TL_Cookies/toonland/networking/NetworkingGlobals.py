########################## THE TOON LAND DLC ##########################
# Filename: NetworkingGlobals.py
# Created by: Cody/Fd Green Cat Fd (August 2nd, 2013)
####
# Description:
#
# The main purpose of this file is to store static distributed object IDs.
####

Name2doId = {
    'DISTRIBUTED_GEYSER_FOUNTAIN_ID':          100000001,
    'DISTRIBUTED_HICCUP_TRASH_CAN_ID':         100000002,
    'DISTRIBUTED_FF_PICNIC_BASKET_1':          100000003,
    'DISTRIBUTED_FF_PICNIC_BASKET_2':          100000004,
    'DISTRIBUTED_FF_PICNIC_BASKET_3':          100000005,
    'DISTRIBUTED_FF_HOUSE_1':                  100000006,
    'DISTRIBUTED_FF_HOUSE_2':                  100000007,
    'DISTRIBUTED_FF_HOUSE_3':                  100000008,
    'DISTRIBUTED_DOOR_TOON_HQ_1':              100000009,
    'DISTRIBUTED_DOOR_TOON_HQ_2':              100000010
}

DoId2name = invertDictLossless(Name2doId)

for name, value in Name2doId.items():
    exec '%s = %s' % (name, value)