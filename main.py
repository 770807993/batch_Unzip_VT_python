import 文件操作
import 解压
import os
import getopt
import sys
import virustotal

def scanfiles(dirPath):
    filesAndDirectoyrs = 文件操作.traversalDirectory(dirPath)
    filesPath = filesAndDirectoyrs["fileLsit"]
    testagain = virustotal.scanfiles(filesPath)
    if len(testagain) != 0:
        for filePath in testagain:
            print(filePath, "请稍后重新查询")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-z:-u:-p:-s-S:")
    except getopt.GetoptError as err:
        print(err.opt, "参数填写错误")
        sys.exit(2)
    passwordStr = ""
    zipPath = ""
    unzipPath = ""
    scan = ""
    scan_bool = False
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
    if zipPath != "":
        if os.path.isdir(zipPath):
            解压.unDirectory(zipPath, unzipPath)
        if scan_bool:
            scanfiles(unzipPath)
    if scan != "":
        if os.path.isdir(scan):
            scanfiles(scan)