# anim clean up GUI

import maya.cmds as cmds
import maya.mel as mel

def mergeAllAnimLayer():
    animLayers = cmds.ls(type='animLayer')
    if len(animLayers) == 0:
        cmds.warning('No Animation Layer found.')
        return 1
    mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))
    
    # delete BaseAnimation layer if there is.
    if cmds.objExists('BaseAnimation'): cmds.delete('BaseAnimation')

def bakeAllNonReferencedConstraint():
    consts = cmds.ls(dag=1, ap=1, type='constraint')
    nonRefConsts = [x for x in consts if cmds.referenceQuery(x, isNodeReferenced=1) != 1]

    if nonRefConsts:
        if len(nonRefConsts):
            cmds.select(nonRefConsts)
            cmds.pickWalk(d='up')
            cmds.refresh(suspend=1)
            cmds.bakeResults(time=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)), sb=1, sm=0, pok=1)
            cmds.refresh(suspend=0)

        cmds.delete(nonRefConsts)
    else:
        cmds.warning('No non referenced constraints found.')

def deleteStaticChannelAllCons():
    mel.eval('DeleteAllStaticChannels')
    cmds.warning('Deleted All Static Channels.')

def deleteUnknownNodes():
    unknownNodes = cmds.ls(type="unknown")
    unknownNodes += cmds.ls(type="unknownDag")

    if unknownNodes:
        cmds.warning(f'{len(unknownNodes)} unknown node(s) found. Deleting.')
    else:
        cmds.warning('No unknown node found.')

    for node in unknownNodes:
        if cmds.objExists(node):
            cmds.lockNode(node, lock=False)
            cmds.delete(node)

def deleteNonDefaultCamera():
    # Delete all the camera that's not a part of default camera set (persp, top, front and side)
    # It won't delete if the camera was referenced.

    allCameras = [cmds.listRelatives(shape, p=1)[0] for shape in cmds.ls(type='camera')]

    if 'persp' in allCameras: allCameras.remove('persp')
    if 'front' in allCameras: allCameras.remove('front')
    if 'side' in allCameras: allCameras.remove('side')
    if 'top' in allCameras: allCameras.remove('top')

    if allCameras:
        for cam in allCameras:
            if not cmds.referenceQuery(cam, isNodeReferenced=1):
                cmds.delete(cam)
                cmds.warning(f'Deleted a non default camera: {cam}.')
    else:
        cmds.warning('No non default camera found.')


def unlockLockedNode():
    sels = cmds.ls(sl=1)
    
    if sels:
        for sel in sels:
            if cmds.objExists(sel):
                cmds.lockNode(sel, lock=0)
                cmds.warning(f'Unlocked locked node: {sel}')
    else:
        cmds.warning('No object selected. Skipping.')

def optimizeSceneOptions():
    mel.eval('OptimizeSceneOptions;')

def fixCameraClip():
    curPanel = cmds.getPanel(withFocus=1)
    cam = cmds.modelPanel(curPanel, q=1, camera=1)

    if cmds.nodeType(cam) == 'camera':
        camShape = cam
    else:
        camShape = cmds.listRelatives(cam, s=1)[0]

    cmds.setAttr(f'{camShape}.nearClipPlane', 5)
    cmds.setAttr(f'{camShape}.farClipPlane', 10000000)

def run():
    win = cmds.window(t='Handy Man')

    cmds.columnLayout()

    cmds.rowLayout(numberOfColumns=5)
    cmds.text(l='Grid')
    cmds.button(l='1cm', c='import maya.cmds as cmds; cmds.grid(spacing=1, divisions=0, size=10)')
    cmds.button(l='10cm', c='import maya.cmds as cmds; cmds.grid(spacing=10, divisions=0, size=100)')
    cmds.button(l='1m', c='import maya.cmds as cmds; cmds.grid(spacing=100, divisions=0, size=1000)')
    cmds.button(l='10m', c='import maya.cmds as cmds; cmds.grid(spacing=1000, divisions=0, size=10000)')
    cmds.setParent('..')
    cmds.separator()

    cmds.button(l='Fix Clipping', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.fixCameraClip()')
    cmds.separator()

    cmds.button(l='Delete Unknown Nodes', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.deleteUnknownNodes()')
    cmds.button(l='Delete Static Channels', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.deleteStaticChannelAllCons()')
    cmds.button(l='Delete Non Default Cameras', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.deleteNonDefaultCamera()')
    cmds.separator()
    cmds.button(l='Merge and Delete AnimLayer', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.mergeAllAnimLayer()')
    cmds.button(l='Bake and Delete Non Ref Constraints', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.bakeAllNonReferencedConstraint()')
    cmds.separator()
    cmds.button(l='Unlock Locked Nodes', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.unlockLockedNode()')
    cmds.separator()
    cmds.button(l='Optimize Scene', c='import handyMan; import importlib; importlib.reload(handyMan); handyMan.optimizeSceneOptions()')
    cmds.separator()
    cmds.button(l='Suspended Viewport Fix', c='import maya.cmds as cmds; cmds.refresh(suspend=0)')

    cmds.showWindow(win)

