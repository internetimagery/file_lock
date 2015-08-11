# Lock maya file while in use

import maya.cmds as cmds

root = os.path.dirname(os.path.realpath(__file__))

def injectCode():
    scriptID = "File_Locker"
    if not cmds.objExists(scriptID):
        loadCode = "print \"hello\""
        closeCode = convert(os.path.join(root, "unlock.py"))
        cmds.scriptNode(
            name=scriptID,
            scriptType=2,
            afterScript=closeCode)


def run():
    """
    Run the script
    """
    process = cmds.scriptJob(e=["SceneSaved", insertCode])
    print "File Locker is running."

def convert(filePath):
    """
    Convert python to mel
    """
    result = []
    if os.path.isfile(filePath):
        with open(filePath, "r") as f:
            for data in f.readlines():
                result.append("\"%s\"\n" % data.replace("\"", "\\\"").replace("\n", "\\n"))
    return "python(%s);" % " + ".join(result)

injectCode()
