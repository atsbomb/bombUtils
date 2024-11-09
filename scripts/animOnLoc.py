
import maya.cmds as cmds

def _getUniqueName(basename):
    num = 0

def _simplePrompt(message):
    ret = cmds.promptDialog(m=message, button=['OK', 'Cancel'], db='OK', cb='Cancel', ds='Cancel')
    if ret == 'OK': input = cmds.promptDialog(q=1, text=1)
    else: input = ''

    return input

def _simpleConfirm(message):
    ret = cmds.confirmDialog(m=message, button=['Yes', 'No'], db='Yes', cb='No', ds='No')
    if ret == 'Yes': return 1
    else: return 0

def _copyAnim(overwrite=0):
    sels = cmds.ls(sl=1)
    if len(sels) >= 2:
        source = sels[0]
        target = sels[1]

        # overwrite
        if overwrite:
            cmds.selectKey(target)
            cmds.cutKey(target)

        keyableAttrs = cmds.listAttr(source, k=1)
        for keyableAttr in keyableAttrs:
            value = cmds.getAttr(source+'.'+str(keyableAttr))
            # check if target has the attribute
            if cmds.objExists(target + '.' + str(keyableAttr)):
                # making sure it's either not locked or not having an input
                if cmds.getAttr(target+'.'+str(keyableAttr), l=1) != 1 and cmds.connectionInfo(target+'.'+keyableAttr, id=1) != 1:
                    try: cmds.setAttr(target + '.' + str(keyableAttr), value)
                    except: pass
        cmds.copyKey(source)
        try: cmds.pasteKey(target)
        except: pass
    else:
        print('Please select 2 objects to copy from and paste to.')

def storeAnimOnLoc():
    sels = cmds.ls(sl=1)
    animlocs = []

    for sel in sels:
        if cmds.nodeType(sel) == 'transform' or cmds.nodeType(sel) == 'joint':
            loc = _getUniqueName(sel + '_animloc')
            loc = cmds.spaceLocator(n = loc)[0]
            cmds.addAttr(loc, ln='target', dt='string', k=1)
            cmds.setAttr(loc+'.target', sel, type='string')
            animlocs.append(loc)

            # custom attributes
            attrs = cmds.listAttr(sel, k=1, ud=1)
            if attrs:
                for attr in attrs:
                    attrType = cmds.getAttr(sel + '.' + attr, type=1)
                    cmds.addAttr(loc, ln=attr, at=attrType, k=1)

            cmds.select(sel, loc)
            _copyAnim()

    cmds.select( animlocs )


def restoreAnimFromLoc():
    locs = cmds.ls( sl=1 )

    if locs:
        # obtain target list for dialog
        targets = []
        for loc in locs:
            if cmds.objExists(loc+'.target'):
                targets.append(cmds.getAttr(loc+'.target'))

        ret = cmds.confirmDialog(t='Search and Replace?', m='\n'.join(targets), button=['Yes', 'No', 'Cancel'], db='Yes', cb='Cancel', ds='Cancel')

        if ret == 'Cancel':
            pass

        else:
            if ret == 'Yes':
                sterm = _simplePrompt('Search for?')
                rterm = _simplePrompt('Replace with?')

            for loc in locs:
                if cmds.objExists(loc+'.target'):
                    if ret == 'Yes':
                        target = cmds.getAttr(loc+'.target').replace(sterm, rterm)
                    elif ret == 'No':
                        target = cmds.getAttr(loc+'.target')

                    if cmds.objExists(target):
                        cmds.select(loc, target) 
                        _copyAnim(overwrite=1)
                    
                    else:
                        cmds.warning('Skipping to apply animation for ' + target + '. No object matching with the name.')

            if _simpleConfirm('Delete source animlocs?'):
                cmds.delete(locs)

