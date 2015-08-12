# Lock maya file while in use

import maya.cmds as cmds
import os

root = os.path.dirname(os.path.realpath(__file__))

def injectCode():
    scriptID = "File_Locker"
    if not cmds.objExists(scriptID):
        loadCode = "print \"hello\""
        openCode = convert(os.path.join(root, "lock.py"))
        closeCode = convert(os.path.join(root, "unlock.py"))
        cmds.scriptNode(
            name=scriptID,
            scriptType=2,
            beforeScript=openCode,
            afterScript=closeCode)

def removeLock():
    f = cmds.file(q=True, sn=True)
    if f:
        filename, ext = os.path.splitext(f)
        path = "%s.lock" % filename
        if os.path.isfile(path):
            os.remove(path)

def convert(filePath):
    """
    Convert python to mel
    """
    result = []
    if os.path.isfile(filePath):
        with open(filePath, "r") as f:
            for data in f.readlines():
                result.append("\"%s\"\n" % data.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n"))
    return "python(%s);" % " + ".join(result)

import file_lock.lock
injectCode()
cmds.scriptJob(e=["PostSceneRead", injectCode])
cmds.scriptJob(e=["NewSceneOpened", injectCode])
