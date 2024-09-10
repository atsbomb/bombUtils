# 2 driver constraint
# -------------------
# sets up a constraint driven by 2 drivers and gives blend attr
# select 2 drivers then the driven object last

import maya.cmds as cmds

type = 'point'
# type
# - point
# - orient
# - scale
# - parent

sels = cmds.ls(sl=1)

if len(sels) >= 3:
    driverA = sels[0]
    driverB = sels[1]
    driven = sels[2]
    if len(sels) == 4:
        switch = sels[3]
    else:
        switch = sels[2]
    cb = mm.eval('global string $gChannelBoxName; $t=$gChannelBoxName')
    attrs = cmds.channelBox(cb, q=1, sma=1)
    if attrs: attr = attrs[0]
    else: attr = ''

    if cmds.objExists(switch+'.'+attr):
        if type == 'point':
            const = cmds.pointConstraint(driverA, driverB, driven, mo=0)[0]
        elif type == 'orient':
            const = cmds.orientConstraint(driverA, driverB, driven, mo=1)[0]
        elif type == 'scale':
            const = cmds.scaleConstraint(driverA, driverB, driven, mo=1)[0]
        elif type == 'parent':
            const = cmds.parentConstraint(driverA, driverB, driven, mo=1)[0]
        rev = cmds.createNode('reverse')

        cmds.connectAttr(switch+'.'+attr, rev+'.inputX')
        cmds.connectAttr(rev+'.outputX', const+'.'+driverA+'W0')
        cmds.connectAttr(switch+'.'+attr, const+'.'+driverB+'W1')
