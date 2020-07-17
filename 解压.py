import os
import zipfile
import rarfile
import 文件操作
import shutil
import pathlib


# 根据不同的类型进行解压
def switch_Unzip(fileType, filePath, unFilePath, filePassword=None):
    # 把后缀名全部转成小写然后进行对比
    if fileType.lower() == ".zip":
        unZip(filePath, unFilePath, filePassword.encode())
    elif fileType.lower() == ".rar":
        unRar(filePath, unFilePath, filePassword)
    elif fileType.lower() == ".7z":
        un7z(filePath, unFilePath, filePassword)


# 解压rar
def unRar(filePath, unFilePath, filePassword=None):
    if not rarfile.is_rarfile(filePath):
        print(文件操作.getFileName(filePath), "不是RAR文件")
        return False
    rarfile.UNRAR_TOOL = 'C:\\Program Files\\WinRAR\\UnRAR.exe'
    rarFileObj = rarfile.RarFile(filePath)
    if rarFileObj.needs_password() and filePassword is not None:
        rarFileObj.setpassword(filePassword)
    elif rarFileObj.needs_password() and filePassword is None:
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
    zipFileObj.setpassword(filePassword)
    # 将文件路径和解压路径初始化为Path对象
    unPathObj = pathlib.Path(unFilePath)
    pathObj = pathlib.Path(filePath)
    # 如果解压路径不存在则创建
    if not unPathObj.exists():
        unPathObj.mkdir()
    try:
        # 如果这个文件夹不存在则创建
        if not unPathObj.exists():
            unPathObj.mkdir()
        # 遍历压缩包内部对象
        for fName in zipFileObj.namelist():
            # 转变压缩包内文件/文件夹编码
            correct_fn = fName.encode('cp437').decode('gbk')
            # 将当前遍历路径转成路径对象
            correct_fnObj = unPathObj / correct_fn
            # 如果当前遍历的路径为文件夹
            if str(correct_fn).endswith("/"):
                # 文件夹不存在则创建
                if not correct_fnObj.exists():
                    correct_fnObj.mkdir()
                # 否则跳过
                else:
                    continue
            else:
                # 如果当前遍历路径为文件，则复制
                with correct_fnObj.open("wb") as defile:
                    with zipFileObj.open(fName, "r") as srcfile:
                        shutil.copyfileobj(srcfile, defile)
        return True
    except Exception as e:
        print(文件操作.getFileName(filePath), "解压失败")
        print("错误提示：", e)
        print("尝试使用7z解压")
        un7z(filePath, unFilePath, filePassword.decode())
    finally:
        zipFileObj.close()
    return False


# 解压7Z
def un7z(filePath, unFilePath, filePassword=None):
    unState = False
    cmd = "7z x " + os.path.abspath(filePath) + " -y " + " -o" + os.path.abspath(unFilePath)
    if filePassword is not None:
        cmd = "7z x " + "\"" + os.path.abspath(
            filePath) + "\"" + " -p" + filePassword + " -y " + " -o" + "\"" + os.path.abspath(unFilePath) + "\""
    if os.system(cmd) == 0:
        unState = True
    if unState:
        return True
    else:
        print(文件操作.getFileName(filePath), "解压失败")
        return False


def unDirectory(zipPath, uZipPath, password="infected"):
    filePathList = 文件操作.getFileList_all(zipPath, string=True)
    文件操作.checkDir(uZipPath, True)
    for filePath in filePathList:
        print("正在解压", 文件操作.getFileName(filePath))
        fileType = 文件操作.getFileType(filePath)
        uZipFilePath = os.path.join(uZipPath, 文件操作.getFileName(filePath, False))
        try:
            fileNameStr = 文件操作.getFileName(filePath, False)
            passwordStr_index = fileNameStr.index("密码") + 2
            passwordStr = fileNameStr[passwordStr_index:]
            if passwordStr[0:1] == ":" or passwordStr[0:1] == "：" or passwordStr[0:1] == "_":
                passwordStr_index = passwordStr_index + 1
                if len(fileNameStr[passwordStr_index:]) !=0:
                    passwordStr = fileNameStr[passwordStr_index:]
            switch_Unzip(fileType, filePath, uZipFilePath, passwordStr)
        except ValueError as e:
            switch_Unzip(fileType, filePath, uZipFilePath, password)
        if not 文件操作.checkDir(uZipFilePath):
            print(文件操作.getFileName(filePath), "解压失败")


if __name__ == '__main__':
    unZip("C:\\Users\\Sy\\Desktop\\字符串处理工具.zip", "C:\\Users\\Sy\\Desktop\\1")
    print("解压完成")
