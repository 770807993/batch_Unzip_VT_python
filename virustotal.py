from virustotal_python import Virustotal
import hashlib
import os.path
import time

# 初始化对象，填入API_Key
vtotal = Virustotal("5af41c462b8cb6b9b02f1641ab3ebbbe6bc289b723de142c9765beb691f704b6")
# 上传文件
def scanfile(filePath):
    file_hash = None
    if os.path.isfile(filePath):
        f = open(filePath, "rb")
        f_buffer = f.read()
        f.close()
        file_hash = hashlib.md5(f_buffer).hexdigest()
    file_hash_list = []
    file_hash_list.append(file_hash)
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
        print("超过请求速率",filePath,"将在60S后重试")
        time.sleep(60)
        resp = vtotal.file_report(file_hash_list)
        file_report_num = file_report_num + 1
        if file_report_num == 4:
            return resp
    # pprint(resp)
    if resp["json_resp"]["response_code"] == 0:
        resp = vtotal.file_scan(filePath)
        if resp["json_resp"]["response_code"] == 0:
            print("上传失败")
            return None
    print(filePath, resp["json_resp"]["positives"])
    return resp
# 批量上传文件，返回需要重新检查的文件的路径
def scanfiles(filepaths):
    testagain = []
    for file_path in filepaths:
        resp = scanfile(file_path)
        if resp == None:
            print(file_path, "上传失败")
        elif resp["status_code"] == 204:
            print(file_path, "扫描失败")
        elif not ("positives" in resp["json_resp"]):
            print(file_path, "排队等待重更新上传")
            testagain.append(file_path)
        time.sleep(10)
    return testagain

if __name__ == '__main__':
    scanfile('C:\\Users\\SY\\Desktop\\4.17-\\EXE样本5X_251\\EXE╤∙▒╛5X_251\\MD5\\2.exe')


