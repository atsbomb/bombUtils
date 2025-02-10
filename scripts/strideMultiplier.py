# stride multiplier

import maya.cmds as cmds

sels = cmds.ls(sl=1)

root = sels[0]
footA = sels[1]
footB = sels[2]

minTime = cmds.playbackOptions(q=1, min=1)
maxTime = cmds.playbackOptions(q=1, max=1)

cmds.promptDialog(m='axis')
axis = cmds.promptDialog(q=1, t=1)

cmds.promptDialog(m='mult')
mult = float(cmds.promptDialog(q=1, t=1))

# foot loc in root space
locA, locB = cmds.spaceLocator(), cmds.spaceLocator()
cmds.parent(locA, locB, root)
footAPC = cmds.pointConstraint(footA, locA, mo=0)
footAOC = cmds.orientConstraint(footA, locA, mo=0)
footBPC = cmds.pointConstraint(footB, locB, mo=0)
footBOC = cmds.orientConstraint(footB, locB, mo=0)
cmds.bakeResults(locA, locB, time=(minTime, maxTime), sb=1, sm=0, pok=1)
cmds.delete(footAPC, footAOC, footBPC, footBOC)
cmds.pointConstraint(locA, footA, mo=0)
cmds.orientConstraint(locA, footA, mo=0)
cmds.pointConstraint(locB, footB, mo=0)
cmds.orientConstraint(locB, footB, mo=0)

# scale forward movement key from minTime
for obj in [root, locA, locB]:
    pivotValue = cmds.keyframe(obj, at=f't{axis}', q=1, vc=1, time=(minTime,))[0]
    cmds.scaleKey(obj, at=f't{axis}', vs=mult, fp=pivotValue)

# bake foot anim and delete locs
cmds.bakeResults(footA, footB, time=(minTime, maxTime), sb=1, sm=0, pok=1)
cmds.delete(locA, locB)

