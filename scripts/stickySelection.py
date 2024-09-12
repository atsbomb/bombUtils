import maya.cmds as cmds

def _getPos(targets):
    ret = []

    # objExist check
    for target in targets:
        if cmds.objExists(target) == 0:
            targets.remove(target)

    if targets:
        for target in targets:
            if cmds.ls(target, st=1) == 'transform':
                ret.append(cmds.xform(target, q=1, ws=1, t=1))
            else:
                cmds.setToolTo('moveSuperContext')
                cmds.select(target)
                ret.append(cmds.manipMoveContext('Move', q=1, p=1))

    return ret

def _getOri(targets):
    ret = []

    # objExist check
    for target in targets:
        if cmds.objExists(target) == 0:
            targets.remove(target)

    if targets:
        for target in targets:
            ret.append(cmds.xform(target, q=1, ws=1, ro=1))

    return ret

def stickySelection():
    sel = cmds.ls(sl=1, fl=1)[0]
    #locs = []

    pos = _getPos([sel])
    ori = _getOri([sel])

    cmds.currentTime(cmds.currentTime(q=1) + 1)

    cmds.xform(sel, ws=1, t=(pos[0][0], pos[0][1], pos[0][2]) )
    cmds.xform(sel, ws=1, ro=(ori[0][0], ori[0][1], ori[0][2]) )
    cmds.setKeyframe(sel + '.t')
    cmds.setKeyframe(sel + '.r')

    cmds.select(sel)
