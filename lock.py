# Lock Maya files so only one person can use at a time.

import maya.cmds as cmds
import os, datetime, getpass, json
import __main__

class FileLock(object):
    def __init__(s):
        s.setRoot()

    def setRoot(s):
        s.root = cmds.file(q=True, sn=True)
        if s.root:
            filename, ext = os.path.splitext(s.root)
            s.lockDir = "%s.lock" % filename
            s.locked = os.path.isfile(s.lockDir)
        else:
            s.lockDir = None
            s.locked = False

    def lock(s):
        if not s.locked and s.lockDir:
            with open(s.lockDir, "w") as f:
                data = {
                    "Locked on" : str(datetime.datetime.now()),
                    "Locked by" : getpass.getuser()
                    }
                json.dump(data, f, sort_keys=True)
            s.locked = True
            print "File locked."

    def unlock(s):
        if s.locked and s.lockDir and os.path.isfile(s.lockDir):
            os.remove(s.lockDir)
            s.locked = False
            print "File unlocked."

__main__.FileLock = FileLock()
cmds.scriptjob(e=["quitApplication", __main__.FileLock.unlock])
cmds.scriptJob(e=["SceneSaved", __main.FileLock.lock], kws=True)


if __main__.FileLock.locked:
    try:
        with open(__main__.FileLock.lockDir, "r") as f:
            details = json.load(f)
            message = "%(user)s locked this file at %(time)s and may be currently working on it.\nDo you wish to overide?" % {"user" : details["Locked by"], "time" : details["Locked on"]}
    except ValueError:
        message = "Someone might be working on this file.\nDo you want to override?"
    answer = cmds.confirmDialog(
        button=["Override Lock","Leave"],
        title="File is Locked",
        message=message)
    if "Override" in answer:
        __main__.FileLock.lock() # relock file
    else:
        __main__.FileLock.locked = False
        cmds.file( force=True, new=True )
else:
    __main__.FileLock.lock()
