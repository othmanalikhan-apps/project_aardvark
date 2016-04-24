import sys
import os

def loadPaths():
    """
    Inserts the project paths into system path so that imports and running
    scripts from other scripts does not result in import errors.
    """
    rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pathList = [os.path.join(rootPath, 'src')]
    for path in pathList:
        sys.path.append(path)

loadPaths()
