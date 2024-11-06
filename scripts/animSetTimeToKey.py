import maya.cmds as cmds

def run():
    times = cmds.keyframe(q=1, sl=1)
    curTime = cmds.currentTime(q=1)

    if not times: return 0

    if curTime in times:
        index = times.index(curTime)
        if index == len(times) - 1:
            index = 0
        else:
            index = index + 1
        cmds.currentTime(times[index], e=1)
    else:
        cmds.currentTime(times[0], e=1)


