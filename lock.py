# Lock Maya files so only one person can use at a time. Use when working with dropbox etc...

import maya.cmds as cmds
import os, datetime, getpass, json

class Lock(object):
    """
    Lock file for a single user
    """
    def __init__(s):
        s.setRoot()

    def setRoot(s):
        s.root = cmds.file(q=True, sn=True)

    def getLock(s):
        if s.root:
            filename, ext = os.path.splitext(s.root)
            return os.path.join("%s.lock" % filename)
        return None

    def check(s):
        """
        Check if file is locked
        """
        return os.path.isfile(s.getLock())

    def lock(s):
        """
        Lock the file
        """
        lockPath = s.getLock()
        if lockPath and not os.path.isfile(lockPath):
            data = {
                "Locked on" : str(datetime.datetime.now()),
                "Locked by" : getpass.getuser()
            }
            with open(lockPath, "w") as f:
                json.dump(data, f, sort_keys=True)


l = Lock()
