import os
import json


# 获取文件夹路径下的所有文件和文件夹路径并打印
def traversalDirectory(directoryPath, print_Str=False):
    # 获取当前文件夹路径
    directoryPath_ = directoryPath
    if os.path.isfile(directoryPath):
        directoryPath_ = os.path.dirname(directoryPath)
    # 获取当前文件夹下的所有文件和目录
    fileAndDirectoryList = os.listdir(directoryPath_)
    # 将当前文件夹下的文件路径加入到文件路径列表
    # 将当前文件夹下的文件夹路径加入到文件夹路径列表
    fileList = []
    dirList = []
    for fileOrDirectory in fileAndDirectoryList:
        if os.path.isfile(os.path.join(directoryPath_, fileOrDirectory)):
            fileList.append(os.path.join(directoryPath_, fileOrDirectory))
        else:
            dirList.append(os.path.join(directoryPath_, fileOrDirectory))
            dir_fileOrDirectory_ = traversalDirectory(os.path.join(directoryPath_, fileOrDirectory))
            fileList = fileList + dir_fileOrDirectory_["fileList"]
            dirList = dirList + dir_fileOrDirectory_["dirList"]
    if print_Str:
        for filePath in fileList:
            print("文件：", filePath)
        for dirPath in dirList:
            print("文件夹：", dirPath)
    fileOrDirectory_ = {"fileList": fileList, "dirList": dirList}
    return fileOrDirectory_


# 获取文件夹路径下的所有文件夹路径并打印
def traversalDirectory_file(directoyrPath, print_Str=False):
    # 获取文件夹路径
    directoyrPath_ = directoyrPath
    if os.path.isfile(directoyrPath):
        directoyrPath_ = os.path.dirname(directoyrPath)
    # 获取当前文件夹下的所有文件和目录
    fileAndDirectoyrList = os.listdir(directoyrPath_)
    # 将当前文件夹下的文件路径加入到文件路径列表
    fileList = []
    for fileOrDirectoyr in fileAndDirectoyrList:
        if os.path.isfile(os.path.join(directoyrPath_, fileOrDirectoyr)):
            fileList.append(os.path.join(directoyrPath_, fileOrDirectoyr))
    if print_Str:
        for filePath in fileList:
            print("文件：", filePath)
    return fileList


# 获取文件夹路径下的所有文件夹路径
def traversalDirectory_dir(directoyrPath, print_Str=False):
    # 获取当前文件夹下的所有文件和目录
    fileAndDirectoyrList, directoyrPath_ = getFiles(directoyrPath, True)
    # 将当前文件夹下的文件夹路径加入到文件夹路径列表
    dirList = []
    for fileOrDirectoyr in fileAndDirectoyrList:
        if not os.path.isfile(os.path.join(directoyrPath_, fileOrDirectoyr)):
            dirList.append(os.path.join(directoyrPath_, fileOrDirectoyr))
    if print_Str:
        for dirPath in dirList:
            print("文件夹：", dirPath)
    return dirList


# 获取文件夹路径下的所有文件的类型（后缀名）
def traversalDirectory_fileType(directoyrPath, print_Str=False):
    fileList = traversalDirectory_file(directoyrPath)
    fileTypeLsit = {}
    for file in fileList:
        fileTypeLsit[getFileName(file)] = getFileType(file)
    if print_Str:
        for key, value in fileTypeLsit.items():
            print("文件名：" + key, "类型：" + value)
    return fileTypeLsit


# 获取路径下的所有文件和文件夹
def getFiles(directoyrPath, returenPath=False):
    # 获取当前文件夹路径
    directoyrPath_ = directoyrPath
    if os.path.isfile(directoyrPath):
        directoyrPath_ = os.path.dirname(directoyrPath)
    # 获取当前文件夹下的所有文件和目录
    if not returenPath:
        return os.listdir(directoyrPath_)
    else:
        return os.listdir(directoyrPath_), directoyrPath_


# 获取文件类型
def getFileType(filePath):
    if os.path.exists(filePath):
        if os.path.isfile(filePath):
            return os.path.splitext(filePath)[1].split(".")[1]
        else:
            return ""
    else:
        print(filePath, "不存在")
        return ""


# 获取文件名称
def getFileName(filePath, extensionName=True):
    if os.path.exists(filePath):
        if os.path.isfile(filePath):
            if extensionName:
                return os.path.basename(filePath)
            else:
                return os.path.splitext(os.path.basename(filePath))[0]
        else:
            return ""
    else:
        print(filePath, "不存在")
        return ""


# 检查路径是否存在根据参数创建
def checkDir(path, make=False, print_Str=False):
    if not os.path.exists(path) and make:
        os.makedirs(path)
        if print_Str:
            print(path, "不存在，但已创建")
        return True
    if os.path.exists(path) and os.path.isdir(path):
        return True
    else:
        if print_Str:
            print(path, "不存在或不是文件夹")
        return False


# 检查路径列表，返回True 表示所有路径均正确且存在
def checkDirs(paths, make=False, print_Str=False):
    returnBool = True
    for path in paths:
        if not os.path.exists(path) and make:
            os.makedirs(path)
            if print_Str:
                print(path, "不存在，但已创建")
        if not (os.path.exists(path) and os.path.isdir(path)):
            returnBool = False
            if print_Str:
                print(path, "不存在或不是文件夹")
    return returnBool


# 检查路径
def checkDir(path, make=False, print_Str=False):
    returnBool = True
    if not os.path.exists(path) and make:
        os.makedirs(path)
        if print_Str:
            print(path, "不存在，但已创建")
    if not (os.path.exists(path) and os.path.isdir(path)):
        returnBool = False
        if print_Str:
            print(path, "不存在或不是文件夹")
    return returnBool


# 获取绝对路径
def getDirPath(filePath):
    print(os.path.abspath(filePath))


# 将数据写入文件
def writeData(filePath, data, wordWrap=True):
    f = open(filePath, "w")
    if type(data) is list:
        if wordWrap:
            for linData in data:
                f.write(linData)
                f.write("\n")
        else:
            f.writelines(data)
    elif type(data) is dict:
        json.dump(data, f)
    else:
        f.write(data)
    f.close()


# 测试
if __name__ == '__main__':
    # print("文件和文件夹：")
    # traversalDirectory(".\path\Android.Adware.Dowgin.a.txt")
    # print("文件夹：")
    # traversalDirectory_file(".\path", True)
    # print("文件：")
    # traversalDirectory_file(".\path\Android.Adware.Dowgin.a.txt")
    # print("文件类型：")
    # traversalDirectory_fileType(".\path\Android.Adware.Dowgin.a.txt")
    print(getFileName("D:\\项目\\测黑脚本\\4-8\\#Smoke #Ursnif (2020-03-19).rar", False))
