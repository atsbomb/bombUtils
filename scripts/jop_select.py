import maya.cmds as mc
scriptVersion = 'v03'
scriptName = 'select'

'''
Copyright (c) <2025> <JesseOngPho>
jesseongpho@hotmail.com

DESCRIPTION:
Set keys on the children at the same frames as the master.

FEATURES:
- Work with multiple child selection 
- Work on selected curves in the graph editor
- Work on the current timeline
- Work on maya 2016, 2018, 2020, 2022 both Linux and Windows  (Did not try other version but it should work)

UPDATE 

HOW TO USE : 
1) Select Controller you want the keyframes to be copied
2) Then the children
3) Click the copyTiming icon

INSTALLATION:
To install, drag and drop the install.mel file onto the maya viewport
'''
constraint_types = [
    'parentConstraint', 'pointConstraint', 'orientConstraint',
    'scaleConstraint', 'aimConstraint', 'geometryConstraint',
    'normalConstraint', 'tangentConstraint']
    
def checkEmptySelection():
    myCtrlList = mc.ls(sl=True)
    if not myCtrlList :
        mc.confirmDialog( title='Selection Error', message='The selection is empty. Please select object(s) and try again', button=['ok'], defaultButton='ok')
        mc.error('The selection is empty. Please select an object')
    return myCtrlList
#=================END CHECK FUNCTIONS=================#
#=================GET FUNCTIONS=================#
def getTimelineRange():
    #GET MIN AND MAX OF TIMELINE
    minValue = mc.playbackOptions(q=1,min=1)
    maxValue = mc.playbackOptions(q=1,max=1)
    return minValue,  maxValue

#=================END GET FUNCTIONS=================#    

#=================LOOP FUNCTIONS=================#
def trace_driver_upstream(start_node_list, mySource=True, myTarget=False):
    result = []
    
    for start_node in start_node_list:
        visited = set()
        queue = [start_node]
        
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            visited.add(current)
            
            #If you selected a constraint and you look for drivers 
            if mySource and (mc.nodeType(current) in constraint_types): 
                sources = mc.listConnections(current+'.target', source=mySource, destination=myTarget)
            else : 
                sources = mc.listConnections(current, source=mySource, destination=myTarget) or []  

            filteredSources = mc.ls(sources, exactType='transform')
            for src in sources:
                if (src not in filteredSources):
                    queue.append(src)  # Keep walking up
                else:
                    if src!=start_node:
                        result.append(src)  # Found something meaningful

    return list(set(result))
#=================END LOOP FUNCTIONS=================#
    
    
def selectAllAnimatedInSelection():
    selected = checkEmptySelection()
    
    # Get all descendants of selected nodes
    all_nodes = mc.listRelatives(selected, allDescendents=True, fullPath=True) or []
    
    # Include selected objects themselves
    all_nodes.extend(selected)

    # Filter out nodes that have keyframes
    keyed_nodes = []
    for node in all_nodes:
        if mc.keyframe(node, query=True, keyframeCount=True) > 0:
            keyed_nodes.append(node)
    
    if keyed_nodes:    
        mc.select(keyed_nodes, replace=1)
    else:
        mc.warning("No animated nodes found in selection.")      

def selectAllAnimatedInScene():
    # find anim curves with input type time (keys on timeline), no SDK
    anim_curves = mc.ls(type=['animCurveTA', 'animCurveTL', 'animCurveTT', 'animCurveTU'])


    objects_with_anim_list = []
    for anim_curve in anim_curves:
        #print(anim_curve)
        objects = mc.listConnections(anim_curve, destination=1, shapes=0)
        if (objects):
            object = objects[0]
            if object not in objects_with_anim_list:
                objects_with_anim_list.append(object)
    
    
    
    if objects_with_anim_list:    
        mc.select(objects_with_anim_list, replace=1)
    else:
        mc.warning("No animated nodes found.")     

def selectAllKeys():
    #All keys
    checkEmptySelection()
    mc.selectKey(clear=True)
    mc.selectKey( )

    
def selectInnerKeys(): 
    checkEmptySelection()
    minValue,  maxValue =getTimelineRange()
    mc.selectKey(clear=True) 
    mc.selectKey(time = (minValue , maxValue) )


def selectOuterKeys(): 
    checkEmptySelection()
    minValue,  maxValue =getTimelineRange()
    
    mySelect = mc.ls(sl=True)
    
    mc.selectKey(clear=True) 
    mc.selectKey(time = ( ':%d' %minValue, ), includeUpperBound =False)
    maxValue+=1
    mc.selectKey(mySelect, addTo=True, time = ('%d:' %maxValue, ))

def selectBeforeKeys():
    checkEmptySelection()
    myCurrentTime = mc.currentTime(query = True)
    myRange = myCurrentTime-1
    
    mc.selectKey(clear=True) 
    mc.selectKey(time = (':%d' %myRange , ) )
    
    
def selectAfterKeys():    
    checkEmptySelection()
    myCurrentTime = mc.currentTime(query = True)
    myRange = myCurrentTime+1
    
    mc.selectKey(clear=True)
    mc.selectKey(time = ('%d:' %myRange , ) )

def SelectObjectsFromCurves():  
    checkEmptySelection()  
    mySelectedCurve = mc.keyframe(query=True, selected=True, name=True) or []
    if not mySelectedCurve :
        mc.warning("No keys or curves selected from Graph Editor.")    
    else:
        targets = []
        for mySel in mySelectedCurve:
            connections = mc.listConnections(mySel, source=False, destination=True) 
            if connections: 
                for obj in connections: 
                    obj_type = mc.nodeType(obj)
                    if obj_type =='pairBlend': 
                        obj = list(set(mc.listConnections(obj, source=False, destination=True)))[0]
                    if mc.objExists(obj):
                        targets.append(obj)
                        
        mc.select(targets)
    

def SelectDrivers(): 
    mySelection = checkEmptySelection()
    drivers = (trace_driver_upstream(mySelection, True, False))

    if drivers:
        mc.select(drivers)
        print("Selected drivers:", drivers)
    else:
        mc.warning("No drivers found.")      
    
def SelectTargets(): 
    mySelection = checkEmptySelection()

    targets = (trace_driver_upstream(mySelection, False, True))
    
    if targets:
        mc.select(targets)
        print("Selected targets:", targets)
    else:
        mc.warning("No targets found.")      
            
def SelectConstraints(): 
    mySelection = checkEmptySelection()

    constraints = []
    
    for mySel in mySelection : 
        connections = mc.listConnections(mySel, source=True, destination=False) or [] 
        connections = list(set(connections))
        
        for connect in connections : 
            connect_type = mc.nodeType(connect)
            if connect_type =='pairBlend': 
                cts = mc.listConnections(connect, source=True, destination=False) or [] 
                cts = list(set(cts))
                for ct in cts : 
                    ct_type = mc.nodeType(ct)
                    if ct_type in constraint_types:
                        constraints.append(ct)
            elif connect_type in constraint_types:
                constraints.append(connect)

    constraints = list(set(constraints))  # remove duplicates again

    if constraints:
        mc.select(constraints)
        print("Selected constraints:", constraints)
    else:
        mc.warning("No constraints found.")    

    
def noAction():    
    mc.confirmDialog( title='No Action', message="This button doesn't do anything, it is just to make the menu more readable =)", button=['ok'], defaultButton='ok')
    return
