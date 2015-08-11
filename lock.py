# Lock Maya files so only one person can use at a time.

import maya.cmds as cmds
import os, datetime, getpass, json

def getCurrentFile():
    return cmds.file(q=True, sn=True)

def getLock():
    f = getCurrentFile()
    if f:
        filename, ext = os.path.splitext(f)
        f = "%s.lock" % filename
    return f

def checkLock():
    return os.path.isfile(getLock())

def newLock():
    f = getLock()
    if f:
        with open(f, "w") as f:
            data = {
                "Locked on" : str(datetime.datetime.now()),
                "Locked by" : getpass.getuser()
                }
            json.dump(data, f, sort_keys=True)

def removeLock():
    if checkLock():
        f = getLock()
        os.remove(f)

if checkLock():
    answer = cmds.confirmDialog(
        button=["Override Lock","Leave"],
        title="File is Locked",
        message="Someone might be working on this file.\nDo you want to override?")
    if "Override" in answer:
        removeLock()
    else:
        cmds.file( force=True, new=True )
else:
    newLock()
