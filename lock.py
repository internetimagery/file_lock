# Lock Maya files so only one person can use at a time.

import maya.cmds as cmds
import os, datetime, getpass, json
import __main__

class FileLock(object):
    def __init__(s):
        s.setRoot()
        s.user = getpass.getuser()
        s.version = 0.3

    def setRoot(s):
        s.root = cmds.file(q=True, sn=True)
        if s.root:
            s.lockDir = "%s.lock" % s.root
            s.locked = os.path.isfile(s.lockDir)
        else:
            s.lockDir = None
            s.locked = False

    def lock(s):
        if s.lockDir:
            with open(s.lockDir, "w") as f:
                data = {
                    "time" : str(datetime.datetime.now()),
                    "user" : s.user
                    }
                json.dump(data, f, sort_keys=True)
            s.locked = True
            print "File locked. ( File Locker Version %s)" % s.version

    def unlock(s):
        if s.locked and s.lockDir and os.path.isfile(s.lockDir):
            os.remove(s.lockDir)
            s.locked = False
            print "File unlocked. ( File Locker Version %s)" % s.version

__main__.FileLock = FileLock()
cmds.scriptJob(e=["quitApplication", __main__.FileLock.unlock], kws=True)

try:
    with open(__main__.FileLock.lockDir, "r") as f:
        lockInfo = json.load(f)
        if lockInfo["user"] == __main__.FileLock.user:
            __main__.FileLock.lock()
        else:
            message = "%(user)s locked this file at %(time)s and may be currently working on it.\nDo you wish to overide?" % lockInfo
            answer = cmds.confirmDialog(
                button=["Override Lock","Leave"],
                title="File is Locked",
                message=message)
            if "Override" in answer:
                __main__.FileLock.lock()
            else:
                __main__.FileLock.locked = False
                cmds.file( force=True, new=True )
except:
    __main__.FileLock.lock()
