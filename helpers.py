import sys
import os

def getArgument(num):
    if len(sys.argv) < (num+1):
        print('>> Argument {} not found'.format(num))
        exit()

    return str(sys.argv[num])


def getFolder(folderName):
    if not os.path.exists(folderName):
        print('>> Folder {} not found'.format(folderName))
        exit()

    return folderName


def checkInputFile(file):
    if not os.path.isfile(file):
        print('>> File', file, 'not found')
        exit()

    return file
    

def writeLine(line, file):   
    file.write(line)
    print(line)


def printErrors(errors):
    if not len(errors):
        print('>> No errors found')
    else:
        for error in errors:
            print('>>', error)


def createFile(folder, filename):   
    file = open("{}/{}".format(folder, filename), 'w')
    print('>> Created file', filename)
    return file


def deleteFolder(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    
    os.rmdir(folder)
    print('>> Temporary files removed')