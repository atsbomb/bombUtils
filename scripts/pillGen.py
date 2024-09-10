# Pill gen
# --------
# create pill shaped geometry from first 2 selections

import maya.cmds as cmds
import math

startObj, endObj = cmds.ls(sl=1)[0], cmds.ls(sl=1)[1]
posA, posB = cmds.xform(startObj, q=1, ws=1, t=1), cmds.xform(endObj, q=1, ws=1, t=1)
dist = math.sqrt( math.pow( posA[0]-posB[0] , 2 ) + math.pow( posA[1]-posB[1] , 2 ) + math.pow( posA[2]-posB[2] , 2 ) )
radius = dist / 5

mesh = cmds.polySphere(r=radius, sx=20, sy=20, ax=[0,1,0], cuv=2)[0]
cmds.polyDelEdge(mesh + '.e[180:199]', cv=1)
cmds.select(mesh + '.vtx[180:359]', mesh + '.vtx[361]')
cmds.move(0, dist, 0, r=1)
cmds.select(mesh)
cmds.delete( cmds.pointConstraint(startObj, mesh) )
cmds.delete( cmds.aimConstraint(endObj, mesh, aim=[0,1,0], u=[1,0,0]) )

cmds.addAttr(mesh, ln='source', dt='string')
cmds.setAttr(mesh + '.source', startObj, type='string')
