Python 3.10.6 (v3.10.6:9c7b4bd164, Aug  1 2022, 17:13:48) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
import maya.cmds as cmds
import random

#here we define the variable for road/river width and divisions
RoadWD=0
RoadDV=1

def MakeUI(): #we make a function to make wndows
    winname="CityBuilder"
    if (cmds.window(winname,q=True,ex=True)):
        cmds.deleteUI(winname)
    cmds.window(winname,t="Making City Block",s=False,w=400,h=400)
    cmds.columnLayout()
    cmds.text(l="select all of the objects you may want to populate and add to the list")
    cmds.rowColumnLayout(nc=2,cw=[(1,100),(2,100)])
    cmds.button(l="Add",c="addSelection()")
    cmds.button(l="Remove",c="RemSelection()")
    cmds.setParent("..")
    MakeUI.SLObjList=cmds.textScrollList(sc="makeSelection()",ams=True)
    cmds.columnLayout(cal="center")
    MakeUI.selectedCurve=cmds.textFieldButtonGrp(l="Select the Curve:",ed=False,bl="Select",bc="SelectCRV()")
    cmds.separator(w=400,bgc=(1,1,1))
    MakeUI.NumofCopies=cmds.intSliderGrp(l="number of copies:",v=10,f=True,min=2,max=100)
    MakeUI.OfXV=cmds.floatSliderGrp(l="X Offset",v=0,f=True,min=0)
    MakeUI.OfYV=cmds.floatSliderGrp(l="Y Offset",v=0,f=True,min=0)
    MakeUI.OfZV=cmds.floatSliderGrp(l="Z Offset",v=0,f=True,min=0)
    MakeUI.ScaleRndMin=cmds.floatSliderGrp(l="Scale min",v=1,f=True,min=0.1,max=10)
    MakeUI.ScaleRndMax=cmds.floatSliderGrp(l="Scale max",v=1,f=True,min=0.1,max=10)
    cmds.button(l="Populate",c="MultiplyObj()")
    cmds.button(l="Undo",c="UndoFunc()")
    cmds.button(l="Finalize",c="FinalizeFun()")
    cmds.separator(w=400,bgc=(1,1,1))
    cmds.showWindow()

MakeUI()
        
#start of the functions
def addSelection():
    selectedOBJs=cmds.ls(sl=True,o=True)
    for i in selectedOBJs:
        cmds.textScrollList(MakeUI.SLObjList,e=True,a=i)
        print ("the selected objs are:"+ str(selectedOBJs))
    cmds.select(cl=True)
    
def RemSelection():
    selectedItem=cmds.textScrollList(MakeUI.SLObjList,q=True,si=1)
    cmds.textScrollList(MakeUI.SLObjList,e=True,ri=selectedItem)

def makeSelection():
    global selectedItem
    selectedItem=cmds.textScrollList(MakeUI.SLObjList,q=True,si=1)
    print ("user selected this object: "+selectedItem[0])
    return selectedItem
    
def SelectCRV():
    SelectCRV.selectedCV=cmds.ls(sl=True,o=True)
    print (SelectCRV.selectedCV)
    cmds.textFieldButtonGrp(MakeUI.selectedCurve,e=True,tx=SelectCRV.selectedCV[0])
    
def MultiplyObj():
    cmds.spaceLocator(n="MainLoc")
    cmds.select(SelectCRV.selectedCV[0],add=True)
    #here we get all the user entered data such as offset and rand scale
    DupNum=cmds.intSliderGrp(MakeUI.NumofCopies,q=True,v=True)
    OffXVal=cmds.floatSliderGrp(MakeUI.OfXV,q=True,v=True)
    OffYVal=cmds.floatSliderGrp(MakeUI.OfYV,q=True,v=True)
    OffZVal=cmds.floatSliderGrp(MakeUI.OfZV,q=True,v=True)
    RndMinScale=cmds.floatSliderGrp(MakeUI.ScaleRndMin,q=True,v=True)
    RndMaxScale=cmds.floatSliderGrp(MakeUI.ScaleRndMax,q=True,v=True)
    cmds.pathAnimation(fm=True,f=True,fa="x",ua="y",inverseFront=False,stu=0,etu=DupNum)
    cmds.selectKey("motionPath1_uValue")
    cmds.keyTangent(itt="linear",ott="linear")
    #let's multiply
    ParentGroup=cmds.group(em=True,n="Blocks")
    for obj in range(0,DupNum):
        RandomScaling=random.uniform(RndMinScale,RndMaxScale)
        cmds.currentTime(obj,e=True)
        CurX=cmds.getAttr("MainLoc.tx")
        CurY=cmds.getAttr("MainLoc.ty")
        CurZ=cmds.getAttr("MainLoc.tz")
        CurRotY=cmds.getAttr("MainLoc.ry")
        cmds.select(random.choices(selectedItem))
        #cmds.select(selectedItem,r=True)
        tempObj=cmds.duplicate()
        cmds.setAttr(tempObj[0]+".tx",CurX+OffXVal)
        cmds.setAttr(tempObj[0]+".ty",CurY+OffYVal)
        cmds.setAttr(tempObj[0]+".tz",CurZ+OffZVal)
        cmds.setAttr(tempObj[0]+".ry",CurRotY)
        cmds.scale(RandomScaling,RandomScaling,RandomScaling)
        cmds.parent(tempObj[0],"Blocks",r=False)
        
def UndoFunc():
    cmds.select("MainLoc")
    cmds.delete()
    cmds.select("Blocks")
    cmds.delete()
    
def FinalizeFun():
    cmds.select("MainLoc")
    cmds.delete()
    cmds.select("Blocks")
    cmds.rename("Blocks","Fblocks")


    

    