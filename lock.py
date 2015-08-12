# Lock Maya files so only one person can use at a time.

import maya.cmds as cmds
from datetime import datetime
from getpass import getuser
from json import load, dump

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
