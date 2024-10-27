# anim clean up


import maya.cmds as cmds
import maya.mel as mel

def mergeAllAnimLayer():
    animLayers = cmds.ls(type='animLayer')
    if len(animLayers) == 0:
        cmds.warning('No Animation Layer found.')
        return 1
    mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))

def bakeAllNonReferencedConstraint():
    consts = cmds.ls(dag=1, ap=1, type='constraint')
    nonRefConsts = [x for x in consts if cmds.referenceQuery(x, isNodeReferenced=1) != 1]

    if len(nonRefConsts):
        cmds.select(nonRefConsts)
        cmds.pickWalk(d='up')
        cmds.refresh(suspend=1)
        cmds.bakeResults(time=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)), sb=1, sm=0, pok=1)
        cmds.refresh(suspend=0)

    cmds.delete(nonRefConsts)

def deleteStaticChannelAllCons():
    mel.eval('DeleteAllStaticChannels')

def deleteUnknownNodes():
    unknownNodes = cmds.ls(type="unknown")
    unknownNodes += cmds.ls(type="unknownDag")
    
    for node in unknownNodes:
        if cmds.objExists(node):
            cmds.lockNode(node, lock=False)
            cmds.delete(node)

def run():
    boolMergeAnimLayer = cmds.confirmDialog(m='Merge all Animation Layer?', button=['Yes', 'No'], db='Yes', cb='No')
    boolBakeNonReferencedConstraints = cmds.confirmDialog(m='Bake and delete all non referenced constraints?', button=['Yes', 'No'], db='Yes', cb='No')
    boolDeleteStaticChannels = cmds.confirmDialog(m='Delete all static channels?', button=['Yes', 'No'], db='Yes', cb='No')
    boolDeleteUnknownNodes = cmds.confirmDialog(m='Delete all unknown nodes?', button=['Yes', 'No'], db='Yes', cb='No')

    if boolMergeAnimLayer:
        print('Merging all animation layer')
        mergeAllAnimLayer()
    if boolBakeNonReferencedConstraints:
        print('Bake and deleting all non referenced constraints')
        bakeAllNonReferencedConstraint()
    if boolDeleteStaticChannels:
        print('Deleting all static channels')
        deleteStaticChannelAllCons()
    if boolDeleteUnknownNodes:
        print('Deleting unknown nodes')
        deleteUnknownNodes()

run()
