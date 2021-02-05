#!/usr/bin/env python3
# coding=utf-8
import os
import signal
import sys

from backup.GithubTools import GithubTools
from GithubProduct import GithubProduct
from GithubException import CustomException
from GithubSystem import GithubSystem


class GithubFlow():

    def __init__(self, url, skip_get_repo, skip_broken, force, product_kind, src_path, des_path, clistring):
        self.url = url
        self.skip_get_repo = skip_get_repo
        self.skip_broken = skip_broken
        self.force = force
        self.product_kind = product_kind
        self.src_path = src_path
        self.des_path = des_path
        self.organization = url.split("/")[len(url.split("/")) - 1]
        self.repo_str = None
        self.current_proj = None
        self.cache = "data/cache.txt"
        self.clistring = clistring

    # 添加对Ctrl-C的监听器
    def signal_handler(self, signal, frame):
        if os.path.isfile(self.repo_str):
            product = GithubProduct(self.url, self.skip_get_repo, self.skip_broken, self.force, self.product_kind,
                                    self.src_path,
                                    self.des_path, self.repo_str, self.clistring)
            if self.current_proj is None:
                # 如果当前还没有开始执行项目，则任务项目列表中的第一个项目执行失败
                product.complete_work(2, open(self.repo_str).read().splitlines()[0])
            else:
                # 如果已经开始执行项目，则当前项目执行失败
                product.complete_work(2, self.current_proj)
                self.rollback_proj(self.current_proj)
        print("用户主动中断任务")
        sys.exit(0)

    # 对本组织下的仓库进行循环处理任务
    def auto_make(self):

        # 将监听器注册到本function
        signal.signal(signal.SIGINT, self.signal_handler)

        print("============================ Automake task starting... ============================ \n")

        self.repo_str = "data/" + self.organization + "_repositories.txt"
        # 判断项目列表是否存在
        if os.path.isfile(self.repo_str):
            if len(open(self.repo_str).read().splitlines()) == 0:
                print("项目列表为空，请执行mgithub [option] repocache来获取本组织/用户的项目列表")
                return
            else:
                print("当前项目列表内容：")
                GithubSystem.execute_CmdCommand("cat " + self.repo_str)
                if self.continue_select() == "0":
                    self.automake_new()
                else:
                    return
        else:
            print("未找到项目列表，请执行mgithub [option] repocache来获取本组织/用户的项目列表")
            return

    # 无任务中断，正常操作
    def automake_new(self):

        # 创建一个新的GitHubProduct对象并传入全局参数与command参数
        product = GithubProduct(self.url, self.skip_get_repo, self.skip_broken, self.force, self.product_kind,
                                self.src_path,
                                self.des_path, self.repo_str, self.clistring)

        # 获取项目列表内容
        project_list = open(self.repo_str).read().splitlines()

        # 根据项目列表，将每个项目的远程仓库clone到本地
        try:
            self.clone_repo_list(project_list, product)
        except CustomException as e:
            print(e.msg)
            if str(self.skip_broken) != "True":
                return

        # 根据项目列表，对每个项目进行循环command操作
        self.loop_proj_work(project_list, product)

    # 根据项目列表，将每个项目的远程仓库clone到本地
    def clone_repo_list(self, project_list, product):
        # 如果用户执行时使用 mgithub --skip-get-repositories
        if str(self.skip_get_repo) is True:
            print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
        else:
            print("\n正在将本组织下的仓库clone到本地...")
            for proj in project_list:
                FILE_PATH = "data/" + self.organization + "/" + proj
                # 判断仓库是否已经保存在本地
                if os.path.isdir(FILE_PATH):
                    # 存在
                    print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                else:
                    # 不存在，从远程仓库clone
                    print("git clone from " + proj + "....")
                    cmd = "git clone --depth=1 " + self.url + "/" + proj + ".git data/" + self.organization + "/" + proj
                    try:
                        GithubSystem.execute_GitCommand(cmd)
                    except CustomException as e:
                        # 仓库clone未成功，结束本次任务
                        if str(self.skip_broken) == "True":
                            print(proj + ": 本仓库clone失败")
                        else:
                            print("仓库clone未成功，结束本次任务")
                            raise e

    # 根据项目列表，对每个项目进行循环command操作
    def loop_proj_work(self, project_list, product):
        for proj in project_list:
            # 记录本次正在执行command的项目，方便与监听器记录
            self.current_proj = proj
            # 执行相应的command
            try:
                product.product_execute(proj)
            except CustomException as e:
                # 捕捉执行过程中出现异常
                print(e.msg)
                # 已 FAILED 记录本次任务
                product.complete_work(0, proj)
                # 对项目进行回滚
                self.rollback_proj(proj)
                # 如果用户使用 mgithub --skip-broken
                if str(self.skip_broken) == "True":
                    continue
                else:
                    break

    def rollback_proj(self, project):
        # 对项目进行回滚
        print("============================ [[" + project + "]]: 项目正在回滚")
        cmd = "cd data/" + self.organization + "/" + project + ";git fetch --all;git reset --hard origin/master;git clean -f -d data/" + self.organization + "/" + project + ";"
        try:
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            GithubSystem.execute_GitCommand(cmd)
        except CustomException as e:
            # 项目回滚中出现异常，回滚失败
            print(e.msg)
            print(project + ": 项目回滚失败, 请检查您的网络连接状况和组织名称")
        else:
            print(project + ": 项目已回滚")

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
