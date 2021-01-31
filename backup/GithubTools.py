#!/usr/bin/python3
import os, io, sys, platform, shutil, urllib3, subprocess
from GithubException import CustomException

class GithubTools():
    """统一的云CLI命令执行，所有CLI命令必须精准可用"""

    def __init__(self):
        self.public_ip = ''
        self.os_distribution = ''

    # 下载最新的template模板
    def download_latesttemplate():

        print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            pass
        else:
            print('\n此次任务执行失败，请根据错误原因排查\n')

        print(out_str)

    # 执行CLI命令，无返回值
    def execute_Command(cmd_str):
        # print(cmd_str)

        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            pass
        else:
            print('\n此次任务执行失败，请根据错误原因排查\n')

        print(out_str)

    # 执行CLI命令，有返回值
    def execute_CommandIgnoreReturn(cmd_str):
        # print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        print(out_str)
        if(out_str[0] == "128"):
            raise CustomException(out_str)
        return out_str


    # 执行CLI命令，有返回值
    def execute_CommandReturn(cmd_str):
        # print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            # 去掉\n和"
            # 返回值是元组，不能修改，需要赋值给变量
            temp_str = out_str[1]
            temp_str = temp_str.strip('\n')
            temp_str = temp_str.strip('"')
            print("abcabcabc")
            print(temp_str)
            return 1
        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            print(out_str)
            # raise CustomException(out_str)
            return 0

    # 执行CLI命令，结果写入到文件
    def execute_CommandWriteFile(cmd_str, directory_str):
        # print(cmd_str)

        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            # 去掉\n和"
            # 返回值是元组，不能修改，需要赋值给变量
            temp_str = out_str[1]
            temp_str = temp_str.strip('\n')
            temp_str = temp_str.strip('"')
            print(temp_str)

            with open(directory_str, 'w') as file_object:
                # file_object.write('[remote]\n')
                file_object.write(temp_str)

        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            print(out_str)
