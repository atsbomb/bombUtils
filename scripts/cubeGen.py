# cubeGen
# -------
# create cube shaped geometry from first 2 selections

import maya.cmds as cmds
import math

startObj, endObj = cmds.ls(sl=1)[0], cmds.ls(sl=1)[1]
posA, posB = cmds.xform(startObj, q=1, ws=1, t=1), cmds.xform(endObj, q=1, ws=1, t=1)
dist = math.sqrt( math.pow( posA[0]-posB[0] , 2 ) + math.pow( posA[1]-posB[1] , 2 ) + math.pow( posA[2]-posB[2] , 2 ) )
width = dist / 5

mesh = cmds.polyCube(h=width, w=width, d=width, ax=[0,1,0])[0]
cmds.select(mesh + '.vtx[2:5]')
cmds.move(0, dist, 0, r=1)
cmds.select(mesh)
cmds.delete( cmds.pointConstraint(startObj, mesh) )
cmds.delete( cmds.aimConstraint(endObj, mesh, aim=[0,1,0], u=[1,0,0]) )

cmds.polyBevel(mesh, af=1, oaf=1, fraction=0.1, smoothingAngle=180, sg=4, r=1)

cmds.delete(mesh, ch=1)

cmds.addAttr(mesh, ln='source', dt='string')
cmds.setAttr(mesh + '.source', startObj, type='string')
