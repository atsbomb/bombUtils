import maya.cmds as cmds
import maya.mel as mel

def remove_redundant_keyframes():
    selection = cmds.ls(selection=True)
    if not selection:
        cmds.warning("Please select at least one object.")
        return

    for obj in selection:
        keyable_attrs = cmds.listAttr(obj, keyable=True)
        
        for attr in keyable_attrs:
            # Get all keyframes for the attribute
            keyframes = cmds.keyframe(obj, query=True, attribute=attr)
            if not keyframes:
                continue
            
            # Get values for the keyframes
            values = [cmds.getAttr(f"{obj}.{attr}", time=kf) for kf in keyframes]
            keys_to_delete = []

            # Check for redundant keys
            for i in range(1, len(keyframes) - 1):
                if values[i] == values[i - 1] == values[i + 1]:
                    keys_to_delete.append(keyframes[i])

            # Check for stepped tangents and remove last key before them
            for i in range(1, len(keyframes)):
                if values[i] == values[i - 1]:
                    tangent_type = cmds.keyTangent(obj, attribute=attr, time=(keyframes[i], keyframes[i]), query=True, outTangentType=True)[0]
                    if tangent_type == 'step':
                        keys_to_delete.append(keyframes[i])

            # Remove duplicate entries and sort
            keys_to_delete = sorted(set(keys_to_delete))

            # Delete the identified keys
            if keys_to_delete:
                for t in keys_to_delete:
                    cmds.cutKey(obj, attribute=attr, time=(t, t))

def run():
    activePanel = cmds.getPanel(wf=1)

    if 'graphEditor' in activePanel:
        curves = cmds.keyframe(q=1, sl=1, name=1)
        if curves:
            cmds.cutKey(animation='keys', cl=1)
        else:
            # delete static value if no keyframe is selected
            cmds.delete(staticChannels=1, unitlessAnimationCurves=0, hierarchy='below', controlPoints=0, shape=1)
            remove_redundant_keyframes()

    else:
        # delete keyframe at current time (or selected range) on Time Slider
        mel.eval('timeSliderClearKey()')
