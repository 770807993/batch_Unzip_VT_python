import requests
from virustotal_python import Virustotal
import os.path
import time
import 文件操作

# 初始化对象，填入API_Key
# vtotal = Virustotal("51f9194a2d0e7d60cb7952f8bed2849a65617614e9edaa615c1e7d3ea45cb954")
vtotal = Virustotal("5af41c462b8cb6b9b02f1641ab3ebbbe6bc289b723de142c9765beb691f704b6")


# 上传文件,参数为文件路径，返回值为查询结果
def scanFile(filePath):
    file_hash_list = [文件操作.getFileMD5(filePath)]
    try:
        resp = vtotal.file_report(file_hash_list)
    except Exception as e:
        print(e)
        time.sleep(5)
        try:
            resp = vtotal.file_report(file_hash_list)
        except Exception as err:
            print("重试失败")
            print(err)
            return None
    file_report_num = 0
    while resp["status_code"] == 204:
        print("超过请求速率", filePath, "将在60S后重试")
        time.sleep(60)
        try:
            resp = vtotal.file_report(file_hash_list)
        except requests.exceptions as err:
            print(err)
            print("请求扫描失败，60s后尝试")
            time.sleep(60)
            resp = vtotal.file_report(file_hash_list)
        file_report_num = file_report_num + 1
        if file_report_num == 4:
            return resp
    # pprint(resp)
    if resp["json_resp"]["response_code"] == 0:
        try:
            resp = vtotal.file_scan(filePath)
        except requests.exceptions as e:
            print(e)
            print(filePath, "上传文件失败")
            return None
        if resp["json_resp"]["response_code"] == 0:
            print("上传失败")
            return None
    if "positives" in resp["json_resp"]:
        print(filePath, resp["json_resp"]["positives"])
    return resp


# 批量上传文件，参数：文夹路径list，返回dict,"result"对应dict,key为文件路径，value为查询结果json，"testAgain"对应一个list,内部为需要重新上传的文件路径
def scanFilePaths(filePaths):
    scanFile_result = {}
    result = {}
    testAgain = []
    for file_path in filePaths:
        resp = scanFile(file_path)
        result[file_path] = resp
        if resp is None:
            print(file_path, "上传失败")
        elif resp["status_code"] == 204:
            print(file_path, "扫描失败")
        elif not ("positives" in resp["json_resp"]):
            print(file_path, "已上传，排队等待扫描")
            testAgain.append(file_path)
    scanFile_result["result"] = result
    scanFile_result["testAgain"] = testAgain
    return scanFile_result


def scanFiles_dir(dirPath, scanInfo=False):
    filesPath = 文件操作.getFileList_all(dirPath, string=True)
    scanFile_result = scanFilePaths(filesPath)
    if len(scanFile_result.get("testAgain")) != 0:
        print("获取排队扫描结果,等待一分钟")
        time.sleep(60)
        scanFile_result_1 = scanFilePaths(scanFile_result.get("testAgain"))
        for resultItem in scanFile_result_1.get("result"):
            scanFile_result["result"].append(resultItem)
    # 将查询的返回结果写入文件
    if len(scanFile_result["result"]) != 0:
        result = scanFile_result["result"]
        if scanInfo:
            scanResultRecording(result, dirPath, True)
        else:
            scanResultRecording(result, dirPath)


# 记录查询后的结果
def scanResultRecording(scanResult, dirPath, scanInfo=False):
    scanFileResultPath = os.path.join(dirPath, "扫描结果")
    文件操作.checkDir(scanFileResultPath, True)
    # 记录简单统计
    scanFileResultStatistical = os.path.join(scanFileResultPath, "扫描结果简单统计.txt")
    scanFile_many_Path = os.path.join(scanFileResultPath, "报毒数高的.txt")
    scanFile_less_Path = os.path.join(scanFileResultPath, "报毒数低的.txt")
    scanFile_ManualConfirmation_Path = os.path.join(scanFileResultPath, "需要手动确认的.txt")
    scanFileResultStatisticalList = []
    scanFile_many = []
    scanFile_less = []
    scanFile_ManualConfirmation = []
    for key, value in scanResult.items():
        if value.get("json_resp", False):
            json_resp = value.get("json_resp")
            json_resp_scans = json_resp.get("scans")
            # 将写入文件的扫描的文件路径转成相对路径 方便观看
            filesPath_result = os.path.relpath(key, dirPath)
            scanFileResultStatistical_Str = filesPath_result.ljust(60) + "引擎报毒数：" + str(json_resp.get("positives", "获取失败"))
            scanFileResultStatisticalList.append(scanFileResultStatistical_Str)
            if json_resp.get("positives", 0) >= 20:
                scanFile_many.append(scanFileResultStatistical_Str)
            else:
                # 报毒数少，但两个可信度很高的引擎报毒了
                if json_resp_scans.get("Microsoft", {}).get("detected", False) or json_resp_scans.get("Kaspersky", {}).get("detected", False):
                    scanFile_less.append(scanFileResultStatistical_Str)
                else:
                    # 报毒少，高可信引擎未报毒，需要手动确认
                    scanFile_ManualConfirmation.append(scanFileResultStatistical_Str)
            if scanInfo:
                # 拼接单个文件查询结果文件的路径
                scanFile_info_path = os.path.join(scanFileResultPath, filesPath_result)
                scanFile_info_path = scanFile_info_path+".txt"
                # 遍历单个文件查询结果记录其中报毒的引擎
                scanFile_info = []
                for scan_engine, scan_engine_info in json_resp_scans.items():
                    if scan_engine_info.get("detected", False):
                        # 记录下报毒的引擎和报毒名
                        scanFile_info_str = "报毒引擎：" + scan_engine.ljust(30) + "病毒名：" + scan_engine_info.get("result", "未知")
                        scanFile_info.append(scanFile_info_str)
                # 创建目录结构
                文件操作.checkDir(os.path.dirname(scanFile_info_path), True)
                文件操作.writeData(scanFile_info_path, scanFile_info)
    文件操作.writeData(scanFileResultStatistical, scanFileResultStatisticalList)
    文件操作.writeData(scanFile_many_Path, scanFile_many)
    文件操作.writeData(scanFile_less_Path, scanFile_less)
    文件操作.writeData(scanFile_ManualConfirmation_Path, scanFile_ManualConfirmation)

    pass


if __name__ == '__main__':
    scanFile('C:\\Users\\SY\\Desktop\\4.17-\\EXE样本5X_251\\EXE╤∙▒╛5X_251\\MD5\\2.exe')
