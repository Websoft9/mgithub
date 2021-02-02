import configparser
import os, subprocess

from GithubException import CustomException


class GithubSystem:

    # 从config文件获取指定的属性
    def get_prop(self, key):
        config = configparser.ConfigParser()
        config.read("meta/mgithub.config", encoding="utf-8")
        mgithub_item = config.items("mgithub")
        for content in mgithub_item:
            if content[0] == key:
                return content[1]
        return False

    # 设置指定的config属性
    def set_prop(self, key, value):
        config = configparser.ConfigParser()
        config.read("meta/mgithub.config")
        config.set("mgithub", key, value)
        with open("meta/mgithub.config", "w") as fw:
            config.write(fw)

    # command: 无反馈的命令
    # 如果有反馈，则命令执行过程中出现错误，并打印错误信息
    # return: void
    def execute_Command(cmd_str):
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            pass
        else:
            print('\n此次任务执行失败，请根据错误原因排查\n')
            print(out_str)

    # command: 执行git操作的命令，e.g. git push
    # 如返回值为(128, xxxxxx), 则命令执行失败，并将错误信息以异常的方式向上抛出
    # return: void
    def execute_GitCommand(cmd_str):
        out_str = subprocess.getstatusoutput(cmd_str)
        if (out_str[0] == 128):
            raise CustomException(out_str[1])
        return out_str

    # command: 执行command的命令，e.g. mgithub copy
    # 如返回值为 cp: file not existed... 则命令执行失败，并将错误信息以异常的方式向上抛出
    # return: 1-success, 0-fail
    def execute_CmdCommand(cmd_str):
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            if (str(out_str[1]).split(":")[0] == "cp"):
                raise CustomException(out_str[1])
            temp_str = out_str[1]
            temp_str = temp_str.strip('\n')
            temp_str = temp_str.strip('"')
            print(temp_str)
            return 1
        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            raise CustomException(out_str[1])
            return 0

    # command: 执行系统script命令
    # 如返回值不为(0, null), 则命令执行失败，打印错误信息，但不抛出异常
    # return: 1-success, 0-fail
    def execute_CommandReturn(cmd_str):
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            return 1
        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            print(out_str)
            return 0

    # command: 执行需要写入文件的命令
    # 如果返回值不为(0, null), 则命令执行失败，打印错误信息，不抛出异常
    # 如果命令执行成功，打印返回信息
    # return: void
    def execute_CommandWriteFile(cmd_str, directory_str):
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            temp_str = out_str[1]
            temp_str = temp_str.strip('\n')
            temp_str = temp_str.strip('"')
            print(temp_str)
            with open(directory_str, 'w') as file_object:
                file_object.write(temp_str)
        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            print(out_str)
