# Lock maya file while in use

import maya.cmds as cmds

scriptID = "File_Locker"
def insertCode():
    code = "print \"HEllo world!!\""
    job = cmds.scriptNode(n=scriptID, st=2, bs=code)


def run():
    """
    Run the script
    """
    process = cmds.scriptJob(e=["SceneSaved", insertCode])
    print "File Locker is running."

def convert(filePath):
    """
    Convert file to maya
    """
    result = []
    if os.path.isfile(filePath):
        with open(filePath, "r") as f:
            for data in f.readlines():
                result.append("\"%s\"\n" % data.replace("\"", "\\\"").replace("\n", "\\n"))
    return "python(%s);" % " + ".join(result)

root = os.path.dirname(os.path.realpath(__file__))
script = os.path.join(root, "lock.py")

print convert(script)
