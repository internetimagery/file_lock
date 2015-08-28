# Remove the lock
import maya.cmds as cmds
from os.path import isfile
from os import remove
lockFile = "%s.lock" % cmds.file(q=True, sn=True)
if isfile(lockFile):
    remove(lockFile)
    print "File unlocked."
