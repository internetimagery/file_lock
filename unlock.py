# Remove the lock
import os
import os.path
import maya.cmds as cmds
lockFile = "%s.lock" % cmds.file(q=True, sn=True)
if os.path.isfile(lockFile):
    os.remove(lockFile)
    print "File unlocked."
