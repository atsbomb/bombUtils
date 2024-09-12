import maya.cmds as mc

def interactiveSnapPress(snapTranslate=1, snapRotate=1, snapScale=0):
    sels = mc.ls(sl=1)

    if sels:
        driver = sels[0]
        if len(sels) == 1:
            loc = mc.spaceLocator(name='bombObjectInteractiveSnap_loc')[0]

            mc.delete(mc.pointConstraint(driver, loc))
            mc.delete(mc.orientConstraint(driver, loc))

            driver = loc
            drivens = [sels[0]]

            mc.select(sels[0])
        else:
            drivens = sels[1:]
        
        for driven in drivens:
            if snapTranslate:
                if (mc.getAttr(driven + '.tx', lock = 1) or 
                    mc.getAttr(driven + '.ty', lock = 1) or 
                    mc.getAttr(driven + '.tz', lock = 1)):
                    pass
                else:
                    mc.pointConstraint(driver, driven, name='bombObjectInteractiveSnap_pc')

            if snapRotate:
                if (mc.getAttr(driven + '.rx', lock = 1) or 
                    mc.getAttr(driven + '.ry', lock = 1) or 
                    mc.getAttr(driven + '.rz', lock = 1)):
                    pass
                else:
                    mc.orientConstraint(driver, driven, name='bombObjectInteractiveSnap_oc')

            if snapScale:
                if (mc.getAttr(driven + '.sx', lock = 1) or 
                    mc.getAttr(driven + '.sy', lock = 1) or 
                    mc.getAttr(driven + '.sz', lock = 1)):
                    pass
                else:
                    mc.scaleConstraint(driver, driven, name='bombObjectInteractiveSnap_sc')

            mc.expression(s='setKeyframe ' + driven, name='bombObjectInteractiveSnap_expr')

def interactiveSnapRelease(translate=1, rotate=1, scale=0):
    if mc.ls('bombObjectInteractiveSnap_pc*'):
        mc.delete('bombObjectInteractiveSnap_pc*')

    if mc.ls('bombObjectInteractiveSnap_oc*'):
        mc.delete('bombObjectInteractiveSnap_oc*')

    if mc.ls('bombObjectInteractiveSnap_sc*'):
        mc.delete('bombObjectInteractiveSnap_sc*')

    if mc.ls('bombObjectInteractiveSnap_loc*'):
        mc.delete('bombObjectInteractiveSnap_loc*')

    if mc.ls('bombObjectInteractiveSnap_expr*'):
        mc.delete('bombObjectInteractiveSnap_expr*')    