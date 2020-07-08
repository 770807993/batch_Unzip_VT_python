import os
import json
import pathlib
import hashlib


# 获取文件类型
def getFileType(filePath):
    p = pathlib.Path(filePath)
    if p.exists() and p.is_file():
        return str(p.suffix)
    else:
        print("文件不存在")
        return ""


# 获取文件名称
def getFileName(filePath, extensionName=True):
    p = pathlib.Path(filePath)
    if p.exists() and p.is_file():
        if extensionName:
            return str(p.name)
        else:
            return str(p.stem)
    else:
        print("文件不存在")
        return ""


# 检查路径是否存在根据参数创建
def checkDir(path, make=False):
    p = pathlib.Path(path)
    if not p.exists() and make:
        p.mkdir(path, parents=True)
        print(path, "不存在，但已创建")
        return True
    if p.exists() and p.is_dir():
        return True
    else:
        print(path, "不存在或不是文件夹")
        return False


# 获取绝对路径
def getDirPath(filePath):
    print(os.path.abspath(filePath))


# 将数据写入文件
def writeData(filePath, data, wordWrap=True):
    with open(filePath) as f:
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


# 计算文件MD5
def getFileMD5(filePath):
    file_hash = None
    if os.path.isfile(filePath):
        f = open(filePath, "rb")
        f_buffer = f.read()
        f.close()
        file_hash = hashlib.md5(f_buffer).hexdigest()
    return file_hash


# 获取需要可以省略的文件夹层级
def getCanOmittedPath(path):
    p = pathlib.Path(path)
    # 获取path下的所有子目录路路径
    pathList = []
    for pathList_item in p.glob("**"):
        pathList.append(pathList_item)
    canOmittedPath = []


# 获取指定目录下的所有子目录和文件(递归查找)，distinguish决定返回字典还是列表，默认返回字典,string指路径为字符串还是Path对象
def getDirListAndFileList_all(path, distinguish=True, string=False):
    p = pathlib.Path(path)
    if distinguish:
        fileList = []
        dirList = []
        retDic = {}
        for item in p.glob("**/*"):
            if item.is_file():
                if string:
                    fileList.append(str(item))
                else:
                    fileList.append(item)
            elif item.is_dir():
                if string:
                    dirList.append(str(item))
                else:
                    dirList.append(item)
        retDic["file"] = fileList
        retDic["dir"] = dirList
        return retDic
    else:
        pathList = []
        for item in p.glob("**/*"):
            if item.is_file() or item.is_dir():
                if string:
                    pathList.append(str(item))
                else:
                    pathList.append(item)
        return pathList


# 获取当前路径下的所有子目录列表(递归查找),string指路径为字符串还是Path对象
def getDirList_all(path, string=False):
    p = pathlib.Path(path)
    dirList = []
    for item in p.glob("**"):
        if item.is_dir():
            if string:
                dirList.append(str(item))
            else:
                dirList.append(item)
    return dirList


# 获取当前路径下的所有文件列表(递归查找),string指路径为字符串还是Path对象
def getFileList_all(path, string=False):
    p = pathlib.Path(path)
    fileList = []
    for item in p.glob("**/*"):
        if item.is_file():
            if string:
                fileList.append(str(item))
            else:
                fileList.append(item)
    return fileList


# 获取指定目录下的子目录列表和文件列表(当前)，distinguish决定返回字典还是列表，默认返回字典,string指路径为字符串还是Path对象
def getDirListAndFileList(path, distinguish=True, string=False):
    p = pathlib.Path(path)
    if distinguish:
        fileList = []
        dirList = []
        retDic = {}
        for item in p.iterdir():
            if item.is_file():
                if string:
                    fileList.append(str(item))
                else:
                    fileList.append(item)
            elif item.is_dir():
                if string:
                    dirList.append(str(item))
                else:
                    dirList.append(item)
        retDic["file"] = fileList
        retDic["dir"] = dirList
        return retDic
    else:
        pathList = []
        for item in p.iterdir():
            if item.is_file() or item.is_dir():
                if string:
                    pathList.append(str(item))
                else:
                    pathList.append(item)
        return pathList


# 获取当前路径下子目录列表(单层),string指路径为字符串还是Path对象
def getDirList(path, string=False):
    p = pathlib.Path(path)
    dirList = []
    for item in p.iterdir():
        if item.is_dir():
            if string:
                dirList.append(str(item))
            else:
                dirList.append(item)
    return dirList


# 获取当前路径下的文件列表(单层),string指路径为字符串还是Path对象
def getFileList(path, string=False):
    p = pathlib.Path(path)
    fileList = []
    for item in p.iterdir():
        if item.is_file():
            if string:
                fileList.append(str(item))
            else:
                fileList.append(item)
    return fileList


# 测试
if __name__ == '__main__':
    pass

