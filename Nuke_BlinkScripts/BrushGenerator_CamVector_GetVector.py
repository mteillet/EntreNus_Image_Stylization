import maya.cmds as cmds

selectedCam = cmds.ls(selection = True)
print(selectedCam)

cameraVectorInverted = cmds.xform(selectedCam, q=True,m=True, ws=True)[8:11]
cameraVector = [i * -1 for i in cameraVectorInverted]
print(cameraVector)