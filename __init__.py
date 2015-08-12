# Lock maya file while in use

import maya.cmds as cmds
import os, time

root = os.path.dirname(os.path.realpath(__file__))

def injectCode():
    scriptID = "File_Locker"
    uid = time.time()
    if not cmds.objExists(scriptID):
        loadCode = "print \"hello\""
        openCode = convert(os.path.join(root, "lock.py"), uid)
        closeCode = convert(os.path.join(root, "unlock.py"), uid)
        cmds.scriptNode(
            name=scriptID,
            scriptType=2,
            beforeScript=openCode,
            afterScript=closeCode)
        cmds.fileInfo("FileUID", uid)
        print "Injecting Lock Code"

def removeLock():
    f = cmds.file(q=True, sn=True)
    if f:
        filename, ext = os.path.splitext(f)
        path = "%s.lock" % filename
        if os.path.isfile(path):
            os.remove(path)

def convert(filePath, uid):
    """
    Convert python to mel
    """
    def escape(text):
        return "\"%s\"" % text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "")
    result = []
    result.append(escape("import maya.cmds as cmds\n"))
    result.append(escape("fileID = cmds.fileInfo(\"FileUID\", q=True)\n"))
    result.append(escape("if fileID and fileID[0] == \"%s\":\n" % uid))
    if os.path.isfile(filePath):
        with open(filePath, "r") as f:
            for data in f.readlines():
                result.append(escape("    " + data))
    return "python(%s);" % " + \n".join(result)

import file_lock.lock
cmds.scriptJob(e=["PostSceneRead", injectCode])
cmds.scriptJob(e=["NewSceneOpened", injectCode])
injectCode()
