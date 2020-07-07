import os
import json
import pathlib
import shutil
import hashlib


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
def traversalDirectory_file(directoryPath, print_Str=False):
    # 获取文件夹路径
    directoryPath_ = directoryPath
    if os.path.isfile(directoryPath):
        directoryPath_ = os.path.dirname(directoryPath)
    # 获取当前文件夹下的所有文件和目录
    fileAndDirectoryList = os.listdir(directoryPath_)
    # 将当前文件夹下的文件路径加入到文件路径列表
    fileList = []
    for fileOrDirectory in fileAndDirectoryList:
        if os.path.isfile(os.path.join(directoryPath_, fileOrDirectory)):
            fileList.append(os.path.join(directoryPath_, fileOrDirectory))
    if print_Str:
        for filePath in fileList:
            print("文件：", filePath)
    return fileList


# 获取文件夹路径下的所有文件夹路径
def traversalDirectory_dir(directoryPath, print_Str=False):
    # 获取当前文件夹下的所有文件和目录
    fileAndDirectoryList, directoryPath_ = getFiles(directoryPath, True)
    # 将当前文件夹下的文件夹路径加入到文件夹路径列表
    dirList = []
    for fileOrDirectory in fileAndDirectoryList:
        if not os.path.isfile(os.path.join(directoryPath_, fileOrDirectory)):
            dirList.append(os.path.join(directoryPath_, fileOrDirectory))
    if print_Str:
        for dirPath in dirList:
            print("文件夹：", dirPath)
    return dirList


# 获取文件夹路径下的所有文件的类型（后缀名）
def traversalDirectory_fileType(directoryPath, print_Str=False):
    fileList = traversalDirectory_file(directoryPath)
    fileTypeList = {}
    for file in fileList:
        fileTypeList[getFileName(file)] = getFileType(file)
    if print_Str:
        for key, value in fileTypeList.items():
            print("文件名：" + key, "类型：" + value)
    return fileTypeList


# 获取路径下的所有文件和文件夹
def getFiles(directoryPath, returnPath=False):
    # 获取当前文件夹路径
    directoryPath_ = directoryPath
    if os.path.isfile(directoryPath):
        directoryPath_ = os.path.dirname(directoryPath)
    # 获取当前文件夹下的所有文件和目录
    if not returnPath:
        return os.listdir(directoryPath_)
    else:
        return os.listdir(directoryPath_), directoryPath_


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


# 计算文件MD5
def getFileMD5(filePath):
    file_hash = None
    if os.path.isfile(filePath):
        f = open(filePath, "rb")
        f_buffer = f.read()
        f.close()
        file_hash = hashlib.md5(f_buffer).hexdigest()
    return file_hash


# 对文件夹层级结构精简
def directoryLevel_streamlining(path, pathLevel=0, printLog=False):
    p = pathlib.Path(path)
    if printLog:
        print("当前为第%d层" % pathLevel)
    pathList = []
    for pathObj in p.iterdir():
        if printLog:
            print(pathObj)
        pathList.append(pathObj)
    if len(pathList) == 1:
        if pathList[0].is_dir():
            directoryLevel_streamlining(p/pathList[0], pathLevel+1, printLog)
        else:
            pSrc = p
            pDit = p
            pRemove = None
            remove_bool = True
            # 根据层级获取根目录路径
            while pathLevel:
                pDit = pDit.parent
                pathLevel = pathLevel - 1
                if pathLevel == 1:
                    pRemove = pDit
            # 循环遍历移动文件
            continue_bool = False
            for src_file in pSrc.iterdir():
                # 如果需要移动的文件与根目录路径下文件的文件名有重复，则重命名需要移动的文件
                for dit_file in pDit.iterdir():
                    if src_file.name == dit_file.name:
                        src_file_name = src_file.stem + "~" + src_file.suffix
                        try:
                            # 给文件改名，更新src_file对象的路径
                            src_file = src_file.rename(src_file.parent/src_file_name)

                        except FileExistsError as e:
                            print(e)
                            remove_bool = False
                            continue_bool = True
                            break
                if continue_bool:
                    continue_bool = False
                    continue
                shutil.move(str(src_file), str(pDit))
            # 如果移动文件时不出错，则删除无用目录
            if remove_bool:
                shutil.rmtree(str(pRemove))
    else:
        if pathLevel != 0:
            pSrc = p
            pDit = p
            pRemove = None
            remove_bool = True
            # 根据层级获取根目录路径
            while pathLevel:
                pDit = pDit.parent
                pathLevel = pathLevel - 1
                if pathLevel == 1:
                    pRemove = pDit
            # 循环遍历移动文件
            continue_bool = False
            for src_file in pSrc.iterdir():
                # 如果需要移动的文件与根目录路径下文件的文件名有重复，则重命名需要移动的文件
                for dit_file in pDit.iterdir():
                    if src_file.name == dit_file.name:
                        src_file_name = src_file.stem + "~" + src_file.suffix
                        try:
                            # 给文件改名，更新src_file对象的路径
                            src_file = src_file.rename(src_file.parent/src_file_name)
                        except FileExistsError as e:
                            print(e)
                            remove_bool = False
                            continue_bool = True
                            break
                if continue_bool:
                    continue_bool = False
                    continue
                shutil.move(str(src_file), str(pDit))
            # 如果移动文件时不出错，则删除无用目录
            if remove_bool:
                shutil.rmtree(str(pRemove))


# 测试
if __name__ == '__main__':
    directoryLevel_streamlining("C:\\Users\\Sy\\Desktop\\新建文件夹", 0, True)
