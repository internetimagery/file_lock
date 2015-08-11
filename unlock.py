# Remove the lock
import maya.cmds as cmds
import os

root = cmds.file(q=True, sn=True)
if root:
    filename, ext = os.path.splitext(root)
    lockPath = "%s.lock" % filename
    if os.path.isfile(lockPath):
        os.remove(lockPath)
        print "Unlocking File"
