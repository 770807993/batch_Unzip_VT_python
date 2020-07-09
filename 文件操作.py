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
        p.mkdir(parents=True)
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
    p = pathlib.Path(filePath)
    if p.exists() and not p.exists():
        print("存在与写入文件名称相同的文件夹，请手动删除")
        return
    with open(filePath, "w") as f:
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
# dirPath   是否返回绝对路径，相对路径为String类型
def getDirList_all(path, dirPath=True, string=False):
    p = pathlib.Path(path)
    dirList = []
    for item in p.glob("**"):
        if item.is_dir():
            if not dirPath:
                string = True
            if string:
                if dirPath:
                    dirList.append(str(item))
                else:
                    dirList.append(str(item)[len(str(p)):])
            else:
                dirList.append(item)
    return dirList


# 获取当前路径下的所有文件列表(递归查找),string指路径为字符串还是Path对象
# filePath 是否返回绝对路径，相对路径为String类型
def getFileList_all(path, filePath=True, string=False):
    p = pathlib.Path(path)
    fileList = []
    for item in p.glob("**/*"):
        if item.is_file():
            if not filePath:
                string = True
            if string:
                if filePath:
                    fileList.append(str(item))
                else:
                    fileList.append(str(item)[len(str(p)):])
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
# dirPath 为True表示获取完整路径，否则表示获取子目录名称
def getDirList(path, dirPath=True, string=False):
    p = pathlib.Path(path)
    dirList = []
    for item in p.iterdir():
        if item.is_dir():
            if not dirPath:
                string = True
            if string:
                if dirPath:
                    dirList.append(str(item))
                else:
                    dirList.append(str(item.name))
            else:
                dirList.append(item)
    return dirList


# 获取当前路径下的文件列表(单层),string指路径为字符串还是Path对象
# filePath 是否未获取完整路径
# fileSuffix 只获取文件名称时是否带后缀（只有最后一个后缀不带）
def getFileList(path, filePath=True, fileSuffix=True, string=False):
    p = pathlib.Path(path)
    fileList = []
    for item in p.iterdir():
        if item.is_file():
            # 简化参数输入
            if not filePath:
                string = True
            if not fileSuffix:
                filePath = False
                string = True
            if string:
                if filePath:
                    fileList.append(str(item))
                else:
                    if fileSuffix:
                        fileList.append(str(item.name))
                    else:
                        fileList.append(str(item.stem))
            else:
                fileList.append(item)
    return fileList


# 获取指定路径下的各级绝对路径,迭代获取，大目录可能很慢
def dirRating_absolutePath(path, level=0):
    dirRat = {"level": level, "path": str(path)}
    temDict = getDirListAndFileList(path, string=True)
    dirRat["file"] = temDict.get("file")
    dirList = []
    for dirItem in temDict.get("dir"):
        dirList.append(dirRating_absolutePath(dirItem, level + 1))
    dirRat["dir"] = dirList
    return dirRat


# 获取指定路径下的各级相对路径,迭代获取，大目录可能很慢
def dirRating_relativePath(path, level=0):
    p = pathlib.Path(path)
    dirRat = {"level": level, "parentPath": str(p.parent),
              "name": str(p.name), "path": str(p),
              "file": getFileList(p, filePath=False)}
    subDirList = []
    for dirItem in getDirList(p):
        subDirList.append(dirRating_relativePath(dirItem, level + 1))
    dirRat["subDir"] = subDirList
    return dirRat


# 更改指定路径下的所有下项的编码格式
def modifyEncodingFormat_Path(path, encode, decode="gbk"):
    pathList = getDirListAndFileList_all(path, False)


# 测试
if __name__ == '__main__':
    pass
