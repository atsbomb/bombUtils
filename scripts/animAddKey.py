import maya.cmds as cmds

def run():
    selCurves = cmds.keyframe(q=1, sl=1, name=1)
    cmds.setKeyframe( selCurves, insert=1, time=( cmds.currentTime(q=1) ) )
    # select generated keyframes
    cmds.selectKey(selCurves, time=(cmds.currentTime(q=1),))
    cmds.keyTangent(itt='auto', ott='auto')

