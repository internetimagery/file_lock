# Remove the lock
import maya.cmds as cmds
from os.path import isfile
lockFile = "%s.lock" % cmds.fileInfo(q=True, sn=True)
if isfile(lockFile):
    os.remove(lockFile)
    print "File unlocked."
