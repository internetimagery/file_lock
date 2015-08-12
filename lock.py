# Lock Maya files so only one person can use at a time.

import maya.cmds as cmds
# import maya.api.OpenMaya as om
from datetime import datetime
from getpass import getuser
from json import load, dump
from os.path import isfile
import __main__

# if not hasattr(__main__, "FileLockCallbacks"):
#     __main__.FileLockCallbacks = []
#     __main__.FileLockCallbacks.append(om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave, lambda x: cmds.scriptNode("File_Locker", ea=True)))
#     __main__.FileLockCallbacks.append(om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave,  lambda x: cmds.scriptNode("File_Locker", eb=True)))
# else:
#     print "CAllbacks already set"

def SaveAsCheck():
    lockDir = "%s.lock" % root
    if root and isfile(lockDir):
        print "We should be removing the lock here"
    else:
        print "Do not remove lock!"
    cmds.scriptNode("File_Locker", eb=True)

cmds.scriptJob(e=["SceneSaved", SaveAsCheck], kws=True, ro=True)

root = cmds.file(q=True, sn=True)
if root:
    cmds.scriptJob(e=["quitApplication", lambda: cmds.scriptNode("File_Locker", ea=True)], kws=True)
    try:
        with open("%s.lock" % root, "r") as f:
            lockInfo = load(f)
            if lockInfo["user"] == getuser():
                raise IOError, "Locked by same user"
            else:
                message = "%(user)s locked this file at %(time)s and may be currently working on it.\nDo you wish to overide?" % lockInfo
                answer = cmds.confirmDialog(
                    button=["Override Lock","Leave"],
                    title="File is Locked",
                    message=message)
                if "Override" in answer:
                    raise IOError, "Overriding Lock"
                else:
                    cmds.fileInfo("FileUID", "Not even oww")
                    cmds.file( force=True, new=True )
    except IOError, ValueError:
        with open("%s.lock" % root, "w") as f:
            data = {
                "time" : str(datetime.now()),
                "user" : getuser()
                }
            dump(data, f)
        print "File locked."
