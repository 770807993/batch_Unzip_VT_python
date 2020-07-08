import 解压
import os
import getopt
import sys
import VT扫描


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-z:-u:-p:-s-S:-i")
    except getopt.GetoptError as err:
        print(err.opt, "参数填写错误")
        sys.exit(2)
    passwordStr = ""
    zipPath = ""
    unzipPath = ""
    scan = ""
    scan_bool = False
    scan_info = False
    for opt_name, opt_value in opts:
        if opt_name == "-z":
            zipPath = opt_value
            print(zipPath)
        if opt_name == "-u":
            unzipPath = opt_value
            print(unzipPath)
        if opt_name == "-p":
            passwordStr = opt_value
            print(passwordStr)
        if opt_name == "-S":
            scan = opt_value
            print(scan)
        if opt_name == "-s":
            scan_bool = True
        if opt_name == "-i":
            scan_info = True
    if zipPath != "":
        if os.path.isdir(zipPath):
            if unzipPath == "":
                unzipPath = os.path.join(zipPath, "解压")
            解压.unDirectory(zipPath, unzipPath)
        else:
            print("压缩包所在文件夹路径不存在")
            exit()
        if scan_bool:
            if scan_info:
                VT扫描.scanFiles_dir(unzipPath, True)
            else:
                VT扫描.scanFiles_dir(unzipPath)
    if scan != "":
        if os.path.isdir(scan):
            if scan_info:
                VT扫描.scanFiles_dir(scan, True)
            else:
                VT扫描.scanFiles_dir(scan)
        else:
            print("扫描文件所在文件夹路径不存在")
            exit()
