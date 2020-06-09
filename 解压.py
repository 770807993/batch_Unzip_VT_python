import os
import zipfile
import rarfile
import 文件操作
import shutil


# 根据不同的类型进行解压
def switch_Unzip(fileType, filePath, unFilePath, filePassword=None):
    # 把后缀名全部转成小写然后进行对比
    if fileType.lower() == "zip":
        unZip(filePath, unFilePath, filePassword.encode())
    elif fileType.lower() == "rar":
        unRar(filePath, unFilePath, filePassword)
    elif fileType.lower() == "7z":
        un7z(filePath, unFilePath, filePassword)


# 解压rar
def unRar(filePath, unFilePath, filePassword=None):
    if not rarfile.is_rarfile(filePath):
        print(文件操作.getFileName(filePath), "不是RAR文件")
        return False
    rarfile.UNRAR_TOOL = 'C:\\Program Files\\WinRAR\\UnRAR.exe'
    rarFileObj = rarfile.RarFile(filePath)
    if rarFileObj.needs_password() and filePassword != None:
        rarFileObj.setpassword(filePassword)
    elif rarFileObj.needs_password() and filePassword == None:
        print(filePath, "需要密码")
        rarFileObj.close()
        return False
    try:
        rarFileObj.extractall(unFilePath)
        return True
    except rarfile.Error as e:
        print(文件操作.getFileName(filePath), "解压失败")
        print("错误提示：", e)
    finally:
        rarFileObj.close()
    return False


# 解压zip
def unZip(filePath, unFilePath, filePassword=None):
    if not zipfile.is_zipfile(filePath):
        print(文件操作.getFileName(filePath), "不是ZIP文件")
        return False
    zipFileObj = zipfile.ZipFile(filePath)
    # if  __isEncrypteZip(filePath) and filePassword != None:
    zipFileObj.setpassword(filePassword)
    # elif __isEncrypteZip(filePath) and filePassword == None:
    # print(filePath, "需要密码")
    # zipFileObj.close()
    # return False
    try:
        zipFileObj.extractall(unFilePath)
        return True
    except zipfile.BadZipFile as e:
        print(文件操作.getFileName(filePath), "解压失败")
        print("错误提示：", e)
    finally:
        zipFileObj.close()
    return False


# 判断文件是否加密
def __isEncrypteZip(filePath):
    try:
        f = open(filePath, "rb")
        top8hex = f.read(8)
        if top8hex[6:] == '\t\x00':
            return True
        return False
    except IOError as e:
        print(filePath, "判断是否加密时打开文件出错")
    finally:
        f.close()
    return False


# 解压7Z
def un7z(filePath, unFilePath, filePassword=None):
    unState = False
    cmd = "7z x " + os.path.abspath(filePath) + " -y " + " -o" + os.path.abspath(unFilePath)
    if filePassword is not None:
        cmd = "7z x " + os.path.abspath(filePath) + " -p" + filePassword + " -y " + " -o" + os.path.abspath(unFilePath)
    if os.system(cmd) == 0:
        unState = True
    if unState:
        return True
    else:
        print(文件操作.getFileName(filePath), "解压失败，可能是密码错误")
        return False


def unDirectory(zipPath, uZipPath, password="infected"):
    filePathList = 文件操作.traversalDirectory_file(zipPath)
    文件操作.checkDir(uZipPath, True, True)
    for filePath in filePathList:
        print("正在解压", 文件操作.getFileName(filePath))
        fileType = 文件操作.getFileType(filePath)
        uZipFilePath = os.path.join(uZipPath, 文件操作.getFileName(filePath, False))
        try:
            fileNameStr = 文件操作.getFileName(filePath, False)
            passwordStr_index = fileNameStr.index("密码") + 2
            passwordStr = fileNameStr[passwordStr_index:]
            if passwordStr[0:1] == ":":
                passwordStr_index = passwordStr_index + 1
                passwordStr = fileNameStr[passwordStr_index:]
            switch_Unzip(fileType, filePath, uZipFilePath, passwordStr)
        except ValueError as e:
            switch_Unzip(fileType, filePath, uZipFilePath, password)
        if not 文件操作.checkDir(uZipFilePath):
            print(文件操作.getFileName(filePath), "解压失败")
        # if 文件操作.checkDir(uZipFilePath):
        # fileOrDirectoyr_ = 文件操作.traversalDirectory(uZipFilePath)
        # 如果压缩包内为单个文件夹，则将文件夹向上提一层
        # if fileOrDirectoyr_["dirLsit"] and not fileOrDirectoyr_["fileLsit"] and len(fileOrDirectoyr_["dirLsit"]) == 1:
        #     filePath_1_1 = os.path.dirname(os.path.dirname(fileOrDirectoyr_["dirLsit"][0]))
        #     filePath_1 = os.path.dirname(fileOrDirectoyr_["dirLsit"][0])
        #     fileName = os.path.basename(fileOrDirectoyr_["dirLsit"][0])
        #     os.rename(filePath_1, filePath_1+"_1")
        #     shutil.move(os.path.join(filePath_1+"_1", fileName), filePath_1_1)
        #     shutil.rmtree(filePath_1+"_1")


if __name__ == '__main__':
    cmd = "7z x D:\\项目\\测黑脚本\\4-8\\4.7z -pinfected -y  -oD:\\项目\\测黑脚本\\4-8解压\\4.7z"
    os.system(cmd)
    print("解压完成")
