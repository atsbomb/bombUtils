import maya.cmds as cmds

def makeProxyFromSelection(mode=4):
    # Make proxy from selection
    # input geoms
    # mode 3: shrinkWrap vertex (cleaner topology)
    # mode 4: shrinkWrap closest (fill hole)

    sels = cmds.ls(sl=1)
    proxyGeoms = []

    for sel in sels:
        cmds.xform(sel, cpc=1)
        shape = cmds.listRelatives(sel, s=1)[0]
        bbmin = cmds.getAttr(shape + '.boundingBoxMin')[0]
        bbmax = cmds.getAttr(shape + '.boundingBoxMax')[0]

        radius = max(bbmin + bbmax)

        sphereGeom = cmds.polySphere(r = radius)[0]
        proxyGeoms.append(sphereGeom)

        cmds.delete(cmds.pointConstraint(sel, sphereGeom))
        cmds.delete(cmds.orientConstraint(sel, sphereGeom))

        swn = cmds.deformer(sphereGeom, type='shrinkWrap')[0]
        cmds.connectAttr(sel + '.worldMesh[0]', swn + '.targetGeom')
        cmds.setAttr(swn + '.projection', mode)

        cmds.delete(sphereGeom, ch=1)

    cmds.select(proxyGeoms)

