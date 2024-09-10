# motionSketch
# lets user to record mouse motion as a keyframe animation

import maya.cmds as cmds

def motionSketch():
    sels = cmds.ls(sl=1)
    if sels:
        ret = cmds.confirmDialog(t='Motion Sketch', m='Press OK when you are ready to start recording', b=['OK', 'Cancel'])
        if ret == 'OK':
            cmds.currentTime(cmds.playbackOptions(q=1, min=1))
            cmds.select(sels[0])
            cmds.cutKey(sels[0])
            cmds.recordAttr(at = ['translate'])
            cmds.play(rec = 1)
        else:
            pass
    else:
        cmds.confirmDialog(t='Motion Sketch', m='Nothing is selected', b=['OK'])

