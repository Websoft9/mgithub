#!/usr/bin/env python3
# coding=utf-8
import configparser
import os, subprocess
import time

from GithubException import CustomException


class GithubHelperFunc:

    ###################################### config helper func ######################################

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

    ###################################### System command helper func ######################################

    # command: 无反馈的命令
    # 如果有反馈，则命令执行过程中出现错误，并打印错误信息
    # return: void
    @staticmethod
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
    @staticmethod
    def execute_GitCommand(cmd_str):
        # print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        if out_str[0] == 128 or out_str[0] == 129:
            raise CustomException(out_str[1])
        # print(out_str)
        return out_str

    # command: 执行command的命令，e.g. mgithub copy
    # 如返回值为 cp: file not existed... 则命令执行失败，并将错误信息以异常的方式向上抛出
    # return: 1-success, 0-fail
    @staticmethod
    def execute_CmdCommand(cmd_str):
        # print(cmd_str)
        out_str = subprocess.getstatusoutput(cmd_str)
        # print(out_str)
        if out_str[0] == 0 or out_str[1] == '':
            if str(out_str[1]).split(":")[0] == "cp":
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
    @staticmethod
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

    # 根据项目列表，将每个项目的远程仓库clone到本地
    def clone_repo_list(self, project_list, skip_get_repo, skip_broken, organization, url):
        # 如果用户执行时使用 mgithub --skip-get-repositories
        if str(skip_get_repo) == "True":
            print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
        else:
            print("\n正在将本组织下的仓库clone到本地...")
            for proj in project_list:
                FILE_PATH = "data/" + organization + "/" + proj
                # 判断仓库是否已经保存在本地
                if os.path.isdir(FILE_PATH):
                    # 存在
                    print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                else:
                    # 不存在，从远程仓库clone
                    print("git clone from " + proj + "....")
                    cmd = "git clone  " + url + "/" + proj + ".git data/" + organization + "/" + proj
                    try:
                        self.execute_GitCommand(cmd)
                    except CustomException as e:
                        # 仓库clone未成功，结束本次任务
                        if str(skip_broken) == "True":
                            print(proj + ": 本仓库clone失败")
                        else:
                            print("仓库clone未成功，结束本次任务")
                            raise e

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
                self.execute_GitCommand(cmd)
            except CustomException as e:
                raise e
        else:
            print("本地仓库不存在：正在从远程仓库clone")
            # 不存在：使用git clone从新获取本地仓库
            cmd = "git clone  " + url + "/" + project + ".git data/" + organization + "/" + project
            try:
                # GithubTools.execute_CommandIgnoreReturn(cmd)
                self.execute_GitCommand(cmd)
            except CustomException as e:
                raise e
        print(project + ": 本地仓库更新完成")

    # 将本地工程提交到github（push to remote）
    def push_repo(self, project, organization, product_kind):
        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (
            organization, project, product_kind)
        try:
            self.execute_GitCommand(cmd)
        except CustomException as e:
            raise e

    ###################################### Work helper func ######################################

    # 对项目进行回滚
    def rollback_proj(self, project, organization):
        print("============================ [[" + project + "]]: 项目正在回滚")
        cmd = "cd data/" + organization + "/" + project + ";git fetch --all;git reset --hard origin/master;git clean -f -d . ;"
        try:
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            self.execute_GitCommand(cmd)
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
            cmd = "sed -i '/^$/d;/" + project + "/d' " + ctx.obj['repo_str']
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            self.execute_GitCommand(cmd)
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
