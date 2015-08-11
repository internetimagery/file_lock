# Lock Maya files so only one person can use at a time. Use when working with dropbox etc...

import maya.cmds as cmds
import os, datetime, getpass, json

def getCurrentFile():
    return cmds.file(q=True, sn=True)

def getLock():
    f = getCurrentFile()
    if f:
        filename, ext = os.path.splitext(f)
        f = "%s.lock" % f
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



# cmds.scriptJob(e=["PostSceneRead", s.test])
# cmds.scriptJob(e=["NewSceneOpened", s.test])
