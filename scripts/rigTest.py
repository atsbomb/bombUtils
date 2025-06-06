# anim clean up GUI

import maya.cmds as cmds
import maya.mel as mel

def rotateTest():
    RX = 40
    RY = 40
    RZ = 40

    sel = cmds.ls(sl=1)[0]
    curTime = cmds.currentTime(q=1)

    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 10)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 20)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 30)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 40)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 50)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 60)
    cmds.setKeyframe(f'{sel}.r')

    cmds.currentTime(curTime + 5)
    cmds.rotate(RX, 0, 0, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 15)
    cmds.rotate(RX * -1, 0, 0, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')

    cmds.currentTime(curTime + 25)
    cmds.rotate(0, RY, 0, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 35)
    cmds.rotate(0, RY * -1, 0, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')

    cmds.currentTime(curTime + 45)
    cmds.rotate(0, 0, RZ, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')
    cmds.currentTime(curTime + 55)
    cmds.rotate(0, 0, RZ * -1, sel, r=1)
    cmds.setKeyframe(f'{sel}.r')

    cmds.playbackOptions(min=curTime, max=curTime + 60)
    cmds.currentTime(curTime)


def run():
    win = cmds.window(t='Rig Tester')

    cmds.columnLayout()

    cmds.button(l='Rotate', c='import rigTest; import importlib; importlib.reload(rigTest); rigTest.rotateTest()')
    cmds.button(l='Translate', c='')
    cmds.setParent('..')


    cmds.showWindow(win)

