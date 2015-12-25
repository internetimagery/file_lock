# Lock maya file while in use

import maya.cmds as cmds
import os, time, traceback

root = os.path.dirname(os.path.realpath(__file__))
scriptID = "File_Locker"

def injectCode():
    cmds.undoInfo(swf=False)
    try:
        uid = time.time()
        if not cmds.objExists(scriptID):
            cmds.fileInfo("FileUID", uid)
            openCode = convert(os.path.join(root, "lock.py"))
            closeCode = convert(os.path.join(root, "unlock.py"))
            cmds.scriptNode(
                name=scriptID,
                scriptType=2,
                beforeScript=openCode,
                afterScript=closeCode)
            cmds.scriptNode(scriptID, eb=True)
            print "Injecting Lock Code"
        cmds.file(mf=False)
    except Exception:
        print traceback.format_exc()
        raise
    finally:
        cmds.undoInfo(swf=True)

def removeLock():
    f = cmds.file(q=True, sn=True)
    if f:
        filename, ext = os.path.splitext(f)
        path = "%s.lock" % filename
        if os.path.isfile(path):
            os.remove(path)

def convert(filePath):
    """ Convert python to mel """
    def escape(text):
        return "\"%s\"" % text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "")
    uid = cmds.fileInfo("FileUID", q=True)
    uid = uid[0] if uid else "UID ERROR"
    result = []
    result.append(escape("import maya.cmds as cmds\n"))
    result.append(escape("fileID = cmds.fileInfo(\"FileUID\", q=True)\n"))
    result.append(escape("if fileID and fileID[0] == \"%s\":\n" % uid))
    if os.path.isfile(filePath):
        with open(filePath, "r") as f:
            for data in f.readlines():
                result.append(escape("    " + data))
    return "python(%s);" % " + \n".join(result)

cmds.scriptJob(e=("PostSceneRead", injectCode))
cmds.scriptJob(e=("NewSceneOpened", injectCode))
injectCode()
