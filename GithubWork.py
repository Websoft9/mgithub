#!/usr/bin/env python3
# coding=utf-8
import os
import signal
import sys

from GithubProductCmd import GithubProduct
from GithubException import CustomException
from GithubHelperFunc import GithubSystem


class GithubWork():

    def __init__(self, ctx):
        self.ctx = ctx
        self.current_proj = None
        self.repo_str = None
        self.skip_broken = ctx.obj['skip_broken']
        self.skip_get_repo = ctx.obj['skip_get_repositories']
        self.organization = ctx.obj['organization']
        self.url = ctx.obj['url']
        self.product_kind = ctx.obj['product_kind']

    # 添加对Ctrl-C的监听器
    def signal_handler(self, signal, frame):
        if os.path.isfile(self.repo_str):
            if self.current_proj is None:
                # 如果当前还没有开始执行项目，则任务项目列表中的第一个项目执行失败
                GithubSystem().complete_work(2, open(self.repo_str).read().splitlines()[0], self.ctx)
            else:
                # 如果已经开始执行项目，则当前项目执行失败
                GithubSystem().complete_work(2, self.current_proj, self.ctx)
                GithubSystem().rollback_proj(self.current_proj, self.organization)
        print("用户主动中断任务")
        sys.exit(0)

    # 对本组织下的仓库进行循环处理任务
    def auto_make(self):

        # 将监听器注册到本function
        signal.signal(signal.SIGINT, self.signal_handler)

        print("============================ Automake task starting... ============================ \n")

        self.ctx.obj['repo_str'] = "data/" + self.ctx.obj['organization'] + "_repositories.txt"
        self.repo_str = self.ctx.obj['repo_str']

        # 判断项目列表是否存在
        if os.path.isfile(self.repo_str):
            if len(open(self.repo_str).read().splitlines()) == 0:
                # 空的项目列表
                print("项目列表为空，请执行mgithub [option] repocache来获取本组织/用户的项目列表")
                return
            else:
                # 非空项目列表
                # 向用户展示当前项目列表
                print("当前项目列表内容：")
                GithubSystem.execute_CmdCommand("cat " + self.repo_str)

                # 等待用户确认列表待办事项
                if GithubSystem().continue_select() == "0":

                    # 获取项目列表内容
                    project_list = open(self.repo_str).read().splitlines()

                    # 根据项目列表，将每个项目的远程仓库clone到本地
                    try:
                        GithubSystem().clone_repo_list(project_list, self.skip_get_repo,
                                                       self.skip_broken, self.organization, self.url)
                    except CustomException as e:
                        print(e.msg)
                        if str(self.skip_broken) != "True":
                            return

                    # 根据项目列表，对每个项目进行循环command操作
                    self.loop_proj_work(project_list)
                else:
                    return
        else:
            print("未找到项目列表，请执行mgithub [option] repocache来获取本组织/用户的项目列表")
            return

    # 根据项目列表，对每个项目进行循环command操作
    def loop_proj_work(self, project_list):
        for proj in project_list:
            # 记录本次正在执行command的项目，方便与监听器记录
            self.current_proj = proj
            # 执行相应的command
            try:
                self.product_execute(proj)
            except CustomException as e:
                # 捕捉执行过程中出现异常
                print(e.msg)
                # 已 FAILED 记录本次任务
                GithubSystem().complete_work(0, proj, self.ctx)
                # 对项目进行回滚
                GithubSystem().rollback_proj(proj, self.organization)
                # 如果用户使用 mgithub --skip-broken
                if str(self.skip_broken) == "True":
                    continue
                else:
                    break

    def product_execute(self, project):

        print("\n============================ [[" + project + "]]: 开始执行自动化构建")

        # 对本地仓库进行更新
        GithubSystem().update_repo(self.organization, self.url, project)

        # 创建GithubProduct对象并传入对应项目与ctx参数
        product = GithubProduct(self.ctx)

        try:
            if self.product_kind == "copy":
                product.copy(project)
            elif self.product_kind == "githubcli":
                product.githubcli(project)
            elif self.product_kind == "delete":
                product.delete(project)
            elif self.product_kind == "replace":
                product.replace(project)
            elif self.product_kind == "format":
                product.format(project)
            elif self.product_kind == "branch":
                product.branch(project)
            elif self.product_kind == "backup":
                product.backup(project)

            # 将本地改动PUSH到远程仓库
            print("\n正在将本地改动push到远程仓库...")
            GithubSystem().push_repo(project, self.organization, self.product_kind)
        except CustomException as e:
            raise e

        # 本次任务完成
        GithubSystem().complete_work(1, project, self.ctx)
