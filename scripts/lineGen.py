# lineGen
# -------
# Generate line between first 2 selections, and attach both ends

import maya.cmds as cmds

sels = cmds.ls(sl=1)

if len(sels) >= 2:
    start = sels[0]
    end = sels[1]
    line = cmds.curve(d=1, p=[[0,0,0], [0,0,0]])

    clusterA = cmds.cluster(line+'.cv[0]')[1]
    clusterB = cmds.cluster(line+'.cv[1]')[1]

    cmds.loadPlugin('matrixNodes')
    dmatStart = cmds.createNode('decomposeMatrix')
    dmatEnd = cmds.createNode('decomposeMatrix')

    cmds.connectAttr(start+'.worldMatrix', dmatStart+'.inputMatrix')
    cmds.connectAttr(end+'.worldMatrix', dmatEnd+'.inputMatrix')
    cmds.connectAttr(dmatStart+'.outputTranslate', clusterA+'.t')
    cmds.connectAttr(dmatEnd+'.outputTranslate', clusterB+'.t')

else:
    cmds.warning('Not enough or too much objects are selected. Please select 2 objects to set up a line between them.')

