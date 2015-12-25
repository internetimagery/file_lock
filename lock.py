# Lock Maya files so only one person can use at a time.
import os
import uuid
import json
import os.path
import getpass
import datetime
import traceback
import maya.cmds as cmds

class Locker(object):
    def __init__(s):
        s.root = root = cmds.file(q=True, sn=True)
        timeFormat = "%Y-%m-%d %H:%M:%S"
        if root:
            cmds.scriptJob(e=["quitApplication", lambda: cmds.scriptNode("File_Locker", ea=True)], kws=True)
            try:
                with open("%s.lock" % root, "r") as f:
                    lockInfo = json.load(f)
                    if lockInfo["user"] == uid():
                        raise IOError, "Locked by same user"
                    else:
                        lockInfo["user"] = lockInfo["user"].split("-")[0]
                        past = datetime.datetime.utcnow() - datetime.datetime.strptime(lockInfo["time"], timeFormat)
                        seconds = past.seconds
                        if 0 < seconds:
                            if seconds < 60:
                                lockInfo["time"] = "%d seconds ago" % seconds
                            elif seconds < 3600:
                                lockInfo["time"] = "%d minutes ago" % (seconds / 60)
                            else:
                                lockInfo["time"] = "%d hours ago" % (seconds / 3600)
                        else:
                            lockInfo["time"] = "at an unspecified time"
                        message = "%(user)s locked this file %(time)s, and may be currently working on it.\nDo you wish to overide?" % lockInfo
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
                        "time" : datetime.datetime.strftime(datetime.datetime.utcnow(), timeFormat),
                        "user" : getpass.getuser()
                        }
                    json.dump(data, f)
                print "File locked."
        cmds.scriptJob(e=["SceneSaved", s.save_as_unlock], kws=True, ro=True)

    def uid(s): return "%s-%s" % (getpass.getuser(), uuid.uuid4())

    def save_as_unlock(s):
        try:
            lockFile = "%s.lock" % s.root
            if s.root and os.path.isfile(lockFile):
                os.remove(lockFile)
                print "Lock Released"
            cmds.scriptNode("File_Locker", eb=True)
        except Exception:
            print traceback.format_exc()
            raise

Locker()
