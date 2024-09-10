# create a new scene for bunch of testing

import maya.cmds as mc
import random

def newSceneWithSphereAnimated(pos=1, rot=0, scl=0):
    mc.file(f=1, new=1)
    sph = mc.polySphere(r=1, sx=20, sh=20)[0]

    if pos == 1:
        for t in range(0, 201, 10):
            mc.currentTime(t)
            mc.xform(sph, t=[random.random()*10, random.random()*10, random.random()*10])
            mc.setKeyframe(sph)
    if rot == 1:
        for t in range(0, 201, 10):
            mc.currentTime(t)
            mc.xform(sph, ro=[random.random()*100, random.random()*100, random.random()*100])
            mc.setKeyframe(sph)
    if scl == 1:
        for t in range(0, 201, 10):
            mc.currentTime(t)
            mc.xform(sph, s=[random.random()*10, random.random()*10, random.random()*10])
            mc.setKeyframe(sph)

def newSceneForBulletSim():
    mc.file(f=1, new=1)
    #mc.loadPlugin('bullet')
    sph = mc.polySphere(r=1, sx=20, sh=20)[0]
    mc.xform(sph, t=[0, 5, 0])
    import maya.app.mayabullet.BulletUtils as BulletUtils
    BulletUtils.checkPluginLoaded()
    import maya.app.mayabullet.RigidBody as RigidBody
    ret = RigidBody.CreateRigidBody(True).executeCommandCB()
    mc.setAttr(ret[1] + '.colliderShapeType', 2)
    mc.setAttr('bulletSolverShape1.groundPlane', 1)

    cube = mc.polyCube(w=3, h=1, d=6)[0]
    mc.xform(cube, t=[-1, 8, 0], ro=[-20, 0, 10])
    ret = RigidBody.CreateRigidBody(True).executeCommandCB()
    mc.setAttr(ret[1] + '.colliderShapeType', 1)

