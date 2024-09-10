# zero out selected object's keyable attributes

import maya.cmds as cmds
import maya.mel as mm

def _getTime(type):
    timeSlider = mm.eval('$tmp = $gPlayBackSlider')

    if type == 'playbackMin':
        return cmds.playbackOptions(q=1, min=1)
    elif type == 'playbackMax':
        return cmds.playbackOptions(q=1, max=1)
    elif type == 'rangeSelected':
        return cmds.timeControl(timeSlider, q=1, rv=1)
    elif type == 'rangeMin':
        return cmds.timeControl(timeSlider, q=1, ra=1)[0]
    elif type == 'rangeMax':
        return cmds.timeControl(timeSlider, q=1, ra=1)[1]

def zeroOut():
    if _getTime('rangeSelected'):
        selectRange()

    # Obtain selected keyframes if there's any.
    selCurves = cmds.keyframe(q=1, sl=1, name=1)
    # Obtain selected channel list from channelBox.
    gChannelBoxName = mm.eval('$temp=$gChannelBoxName')
    chList = cmds.channelBox (gChannelBoxName, q=True, sma = True)

    if selCurves:
        cmds.keyframe(a=1, vc=0)
        cmds.keyTangent(itt='flat', ott='flat')
    
    if chList:
        sels = cmds.ls(sl=1)
        for sel in sels:
            for ch in chList:
                if (cmds.objExists(sel + '.' + ch) & cmds.getAttr(sel + '.' + ch, l=1) != 1 ):
                    if ch == 'sx' or ch == 'sy' or ch == 'sz':
                        cmds.setAttr(sel + '.' + ch, 1)
                    else:
                        cmds.setAttr(sel + '.' + ch, 0)

    if not chList and not selCurves:
        sels = cmds.ls(sl=1)
        for sel in sels:
            if ( cmds.objExists(sel+'.translateX') & cmds.getAttr(sel+'.translateX', l=1) != 1 ):
                cmds.setAttr(sel+'.translateX', 0)
            if ( cmds.objExists(sel+'.translateY') & cmds.getAttr(sel+'.translateY', l=1) != 1 ):
                cmds.setAttr(sel+'.translateY', 0)
            if ( cmds.objExists(sel+'.translateZ') & cmds.getAttr(sel+'.translateZ', l=1) != 1 ):
                cmds.setAttr(sel+'.translateZ', 0)
            if ( cmds.objExists(sel+'.rotateX') & cmds.getAttr(sel+'.rotateX', l=1) != 1 ):
                cmds.setAttr(sel+'.rotateX', 0)
            if ( cmds.objExists(sel+'.rotateY') & cmds.getAttr(sel+'.rotateY', l=1) != 1 ):
                cmds.setAttr(sel+'.rotateY', 0)
            if ( cmds.objExists(sel+'.rotateZ') & cmds.getAttr(sel+'.rotateZ', l=1) != 1 ):
                cmds.setAttr(sel+'.rotateZ', 0)
            if ( cmds.objExists(sel+'.scaleX') & cmds.getAttr(sel+'.scaleX', l=1) != 1 ):
                cmds.setAttr(sel+'.scaleX', 1)
            if ( cmds.objExists(sel+'.scaleY') & cmds.getAttr(sel+'.scaleY', l=1) != 1 ):
                cmds.setAttr(sel+'.scaleY', 1)
            if ( cmds.objExists(sel+'.scaleZ') & cmds.getAttr(sel+'.scaleZ', l=1) != 1 ):
                cmds.setAttr(sel+'.scaleZ', 1)

