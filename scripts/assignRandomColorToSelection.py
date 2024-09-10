import maya.cmds as cmds
import random

def assignRandomColorMaterial():
    sels = cmds.ls(sl=1)
    minRandom, maxRandom = 0.4, 1.0

    for sel in sels:
        shader = cmds.shadingNode('lambert', asShader=1)
        cmds.setAttr(shader+'.color', random.uniform(minRandom, maxRandom), random.uniform(minRandom, maxRandom), random.uniform(minRandom, maxRandom))
        cmds.select(sel)
        cmds.hyperShade(a=shader)

    cmds.select(sels)

