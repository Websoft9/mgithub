#!/usr/bin/env python3
# coding=utf-8
import configparser
import os, subprocess
import time

from GithubException import CustomException


class GithubHelperFunc:

    ###################################### config helper func ######################################

    # 从config文件获取指定的属性
    # def get_prop(self, key):
    #     config = configparser.ConfigParser()
    #     config.read("meta/mgithub.config", encoding="utf-8")
    #     mgithub_item = config.items("mgithub")
    #     for content in mgithub_item:
    #         if content[0] == key:
    #             return content[1]
    #     return False
    def get_prop(self, item, path, key):
        config = configparser.ConfigParser()
        config.read(path, encoding="utf-8")
        items = config.items(item)
        for content in items:
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

    ###################################### System command helper func ######################################

    @staticmethod
    def execute_InteractiveCommand(cmd_str):
        print("")
        subprocess.run(cmd_str, shell=True)

    # # command: 执行command的命令，e.g. mgithub copy
    # # 如返回值为 cp: file not existed... 则命令执行失败，并将错误信息以异常的方式向上抛出
    # # return: 1-success, 0-fail
    # @staticmethod
    # def execute_CmdCommand(cmd_str):
    #
    #     out_str = subprocess.getstatusoutput(cmd_str)
    #
    #     # max_run = 3
    #     # run = 0
    #     # while run < max_run:
    #     #     try:
    #     #         out_str = subprocess.call(cmd_str, timeout = 5)
    #     #     except subprocess.TimeoutExpired:
    #     #         continue
    #     #     else:
    #     #         break
    #     #     finally:
    #     #         run += 1
    #
    #     if out_str[0] == 0 or out_str[1] == '':
    #         if str(out_str[1]).split(":")[0] == "cp":
    #             raise CustomException(out_str[1])
    #         if out_str[0] == 128 or out_str[0] == 129:
    #             raise CustomException(out_str[1])
    #         temp_str = out_str[1]
    #         temp_str = temp_str.strip('\n')
    #         temp_str = temp_str.strip('"')
    #         if temp_str != "":
    #             print(temp_str)
    #         return 1
    #     else:
    #         print('\n此次任务执行失败，请根据下面错误原因排查：')
    #         raise CustomException(out_str[1])

    @staticmethod
    def execute_CmdCommand(cmd_str):
        max_run = 3
        run = 0
        result = None
        while run < max_run:
            try:
                result = subprocess.run(cmd_str, shell=True, capture_output=True, timeout=100)
            except subprocess.TimeoutExpired:
                continue
            else:
                break
            finally:
                run += 1

        if result is None:
            raise CustomException("Timeout !!!")
        err_msg = result.stderr.decode('utf-8')
        out_msg = result.stdout.decode('utf-8')

        if result.returncode != 0 and err_msg != "":
            # err_msg = str(result.stderr).split("'")[1]
            err_msg = result.stderr.decode('utf-8')
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            # print(result)
            raise CustomException(err_msg)
        else:
            # out_msg = str(result.stdout).split("'")[1]
            out_msg = result.stdout.decode('utf-8')
            if out_msg != "":
                print(out_msg, end='')


    # command: 执行需要写入文件的命令
    # 如果返回值不为(0, null), 则命令执行失败，打印错误信息，不抛出异常
    # 如果命令执行成功，打印返回信息
    # return: void
    @staticmethod
    def execute_CommandWriteFile(cmd_str, directory_str):
        # print(cmd_str)
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

    # command: 执行需要写入文件的命令 【不覆盖】
    # 如果返回值不为(0, null), 则命令执行失败，打印错误信息，不抛出异常
    # 如果命令执行成功，打印返回信息
    # return: void
    @staticmethod
    def execute_CommandWriteFile_uncover(cmd_str, directory_str):
        # print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 0:
            temp_str = out_str[1]
            temp_str = temp_str.strip('\n')
            temp_str = temp_str.strip('"')
            print(temp_str)
            if len(temp_str) > 0:
                with open(directory_str, 'a') as file_object:
                    file_object.write(temp_str + "\n")
        else:
            print('\n此次任务执行失败，请根据下面错误原因排查：')
            print(out_str)

    ###################################### Log helper func ######################################

    # 输出日志
    def show_logs(self, num):

        log_list = open("log/auto_make.log").read().splitlines()

        if (len(log_list) - num - 1) < 0:
            i = 0
        else:
            i = len(log_list) - num

        while i < len(log_list):
            print("#" + str(i + 1) + " " + log_list[i])
            i += 1

    def log_maker(self, project, flag, ctx):
        FILE_PATH = "log/auto_make.log"
        nowtime = time.strftime("%Y%m%d %H:%M:%S")
        logline = nowtime
        logline += " " + ctx.obj["url"] + "->" + project

        # 对任务结束类型进行判断
        if flag == 1:
            logline += " [OK]: "
        elif flag == 0:
            logline += " [FAILED]: "
        elif flag == 2:
            logline += " [ABORT]: "

        logline += ctx.obj["command"]

        self.execute_CmdCommand("echo '" + logline + "' >>" + FILE_PATH)

    ###################################### Repo operation helper func ######################################

    # 更新已经存在的本地仓库 或 获取未存在的本地仓库
    def update_repo(self, organization, url, project):
        # 对本地仓库进行更新
        print(project + ": 更新本地仓库")
        FILE_PATH = "data/" + organization + "/" + project
        # 判断本地仓库是否已经存在
        if os.path.isdir(FILE_PATH):
            print("本地仓库已存在：正在更新")
            # 存在：使用git pull对本地仓库进行更新
            cmd = "cd " + FILE_PATH + "; git pull"
            try:
                self.execute_CmdCommand(cmd)
            except CustomException as e:
                raise e
        else:
            print("本地仓库不存在：正在从远程仓库clone")
            # 不存在：使用git clone从新获取本地仓库
            cmd = "git clone  " + url + "/" + project + ".git data/" + organization + "/" + project
            try:
                # GithubTools.execute_CommandIgnoreReturn(cmd)
                self.execute_CmdCommand(cmd)
            except CustomException as e:
                raise e
        print(project + ": 本地仓库更新完成")

    # 将本地工程提交到github（push to remote）
    def push_repo(self, project, organization, product_kind):
        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (
            organization, project, product_kind)
        try:
            self.execute_CmdCommand(cmd)
        except CustomException as e:
            raise e

    ###################################### Work helper func ######################################

    # 对项目进行回滚
    def rollback_proj(self, project, organization):
        print("============================ [[" + project + "]]: 项目正在回滚")
        cmd = "cd data/" + organization + "/" + project + ";git fetch --all;git reset --hard origin/master;git clean -f -d . ;"
        try:
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            self.execute_CmdCommand(cmd)
        except CustomException as e:
            # 项目回滚中出现异常，回滚失败
            print(e.msg)
            print(project + ": 项目回滚失败, 请检查您的网络连接状况和组织名称")
        else:
            print(project + ": 项目已回滚")

    # 主体构建工作完成后的处理
    def complete_work(self, flag, project, ctx):
        # 由flag参数判断本次操作是否成功
        if flag == 1:
            # 操作成功
            print("\n" + project + ": 自动化任务完成,从cache列表删除该工程,并追加日志")
            # 删除列表中对应的项目
            # cmd = "sed -i '/^$/d;/" + project + "/d' " + ctx.obj['repo_str']
            cmd = "sed -i '' '/^$/d;/" + project + "/d' " + ctx.obj['repo_str']
            self.execute_CmdCommand(cmd)
            # 生成log
            self.log_maker(project, flag, ctx)
            print("============================ [[" + project + "]]: 本项目任务成功\n")
        else:
            # 操作失败
            print("\n" + project + ": 自动化任务未完成,在缓存列表保留此工程,并追加日志")
            # 生成log
            self.log_maker(project, flag, ctx)
            print("============================ [[" + project + "]]: 本项目任务失败\n")

    # 选择继续操作
    # 格式：选择是否在上次任务上继续：  \n\t 0. 继续 \n\t 1. 终止退出  \n\n\t选择:
    def continue_select(self):
        input_str = "\n确认任务清单：  \n "
        i = 0

        for x in ['确认执行', '终止退出']:
            input_str = input_str + str(i) + "." + x + " \n "
            i = i + 1
        input_str = input_str + "\n选择: "

        continue_id = input(input_str)
        while continue_id not in ['0', '1']:
            print('\n\t输入错误，请重新选择')
            continue_id = input(input_str)
        return continue_id
