# create a new scene for bunch of testing

import maya.cmds as cmds
import random

def newSceneWithSphereAnimated(pos=1, rot=0, scl=0):
    cmds.file(f=1, new=1)
    sph = cmds.polySphere(r=1, sx=20, sh=20)[0]

    if pos == 1:
        for t in range(0, 201, 10):
            cmds.currentTime(t)
            cmds.xform(sph, t=[random.random()*10, random.random()*10, random.random()*10])
            cmds.setKeyframe(sph)
    if rot == 1:
        for t in range(0, 201, 10):
            cmds.currentTime(t)
            cmds.xform(sph, ro=[random.random()*100, random.random()*100, random.random()*100])
            cmds.setKeyframe(sph)
    if scl == 1:
        for t in range(0, 201, 10):
            cmds.currentTime(t)
            cmds.xform(sph, s=[random.random()*10, random.random()*10, random.random()*10])
            cmds.setKeyframe(sph)

def newSceneForBulletSim():
    cmds.file(f=1, new=1)
    #cmds.loadPlugin('bullet')
    sph = cmds.polySphere(r=1, sx=20, sh=20)[0]
    cmds.xform(sph, t=[0, 5, 0])
    import maya.app.mayabullet.BulletUtils as BulletUtils
    BulletUtils.checkPluginLoaded()
    import maya.app.mayabullet.RigidBody as RigidBody
    ret = RigidBody.CreateRigidBody(True).executeCommandCB()
    cmds.setAttr(ret[1] + '.colliderShapeType', 2)
    cmds.setAttr('bulletSolverShape1.groundPlane', 1)

    cube = cmds.polyCube(w=3, h=1, d=6)[0]
    cmds.xform(cube, t=[-1, 8, 0], ro=[-20, 0, 10])
    ret = RigidBody.CreateRigidBody(True).executeCommandCB()
    cmds.setAttr(ret[1] + '.colliderShapeType', 1)

