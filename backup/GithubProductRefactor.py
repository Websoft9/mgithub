#!/usr/bin/env python3
# coding=utf-8
import os
import time

from GithubException import CustomException
from GithubSystem import GithubSystem

class GithubProductRefactor():

    def __init__(self, ctx):
        self.ctx = ctx
        self.organization = ctx.obj['organization']
        self.product_kind = ctx.obj['product_kind']
        self.url = ctx.obj['url']
        self.repo_str = ctx.obj['repo_str']

    def product_execute(self, project):

        print("\n============================ [[" + project + "]]: 开始执行自动化构建")

        # COPY
        if self.product_kind == "copy":
            # 判断是否需要强制覆盖文件
            if self.ctx.obj['force']:
                print("\n执行强制覆盖的copy动作...")
                cmd = "cp -rf " + self.ctx.obj['src_path'] + " data/" + self.ctx.obj['organization'] + "/" + project  + self.ctx.obj['des_path']
            else:
                print("\n执行不覆盖的copy动作...")
                cmd = "cp -nr " + self.ctx.obj['src_path'] + " data/" + self.ctx.obj['organization'] + "/" + project  + self.ctx.obj['des_path']
            # 执行相应的COPY命令
            try:
                GithubSystem.execute_CmdCommand(cmd)
            except CustomException as e:
                raise e

        # GITHUBCLI
        elif self.product_kind == "githubcli":
            if len(self.ctx.obj['clistring']) >= 3:
                # clistring: gh secret set ...
                if self.ctx.obj['clistring'].split(" ")[1] == "secret" and self.ctx.obj['clistring'].split(" ")[2] == "set":
                    # 转移到本地的相对应仓库目录下
                    cd_cmd = "cd data/" + self.organization + "/" + project + ";"
                    # 获取用户从命令输入的secret key
                    clistr = self.ctx.obj['clistring'].split(" ")
                    secret_key = clistr[3]
                    # 如果用户使用mgithub -f githubcli
                    if self.ctx.obj['force']:
                        # 覆盖
                        print("\n正在执行强制覆盖的New Secret设置")
                        GithubSystem.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])
                    else:
                        # 不覆盖
                        print("\n正在执行不强制覆盖的New Secret设置")
                        # 判断当前项目中是否存在相同key的secret
                        cmd = "gh secret list -R " + self.organization + "/" + project \
                              + "| grep -c ^" + secret_key
                        rcontent = GithubSystem.execute_GitCommand(cmd)[1]
                        # 不存在则正常创建一个新的secret
                        if rcontent == "0":
                            GithubSystem.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])

                # clistring: gh secret remove ...
                elif self.ctx.obj['clistring'].split(" ")[1] == "secret" and self.ctx.obj['clistring'].split(" ")[2] == "remove":
                    # 转移到本地的相对应仓库目录下
                    cd_cmd = "cd data/" + self.organization + "/" + project + ";"
                    print("\n正在执行批量删除Secret设置")
                    GithubSystem.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])
                else:
                    print("\nmgithub githubcli目前不支持此命令")

        elif self.product_kind == "delete":
            pass
        elif self.product_kind == "replace":
            replacefile =  "data/" + self.organization + "/" + project  + self.src_path
            cmd = "sed -i 's/" + self.des_path + "/" + self.clistring + "/g' " + replacefile
            print(cmd)
            # 执行相应的COPY命令
            try:
                GithubSystem.execute_CmdCommand(cmd)
            except CustomException as e:
                raise e
        elif self.product_kind == "format":
            pass
        elif self.product_kind == "branch":
            pass
        elif self.product_kind == "backup":
            pass

        # 将本地改动PUSH到远程仓库
        print("\n正在将本地改动push到远程仓库...")
        try:
            self.github_push(project)
        except CustomException as e:
            raise e

        # 本次任务完成
        self.complete_work(1, project)

    # 将本地工程提交到github（push to remote）
    def github_push(self, project):
        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (
            self.organization, project, self.product_kind)
        try:
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            GithubSystem.execute_GitCommand(cmd)
        except CustomException as e:
            raise e

    # 主体构建工作完成后的处理
    def complete_work(self, flag, project):
        # 由flag参数判断本次操作是否成功
        if flag == 1:
            # 操作成功
            print("\n" + project + ": 自动化任务完成,从cache列表删除该工程,并追加日志")
            # 删除列表中对应的项目
            cmd = "sed -i '/^$/d;/" + project + "/d' " + self.repo_str
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            GithubSystem.execute_GitCommand(cmd)
            # 生成log
            self.log_maker(project, flag)
            print("============================ [[" + project + "]]: 本项目任务成功\n")
        else:
            # 操作失败
            print("\n" + project + ": 自动化任务未完成,在缓存列表保留此工程,并追加日志")
            # 生成log
            self.log_maker(project, flag)
            print("============================ [[" + project + "]]: 本项目任务失败\n")

    # 生成log
    def log_maker(self, project, flag):
        FILE_PATH = "log/auto_make.log"
        nowtime = time.strftime("%Y%m%d %H:%M:%S")
        logline = nowtime
        # 对任务结束类型进行判断
        if flag == 1:
            logline += " |OK"
        elif flag == 0:
            logline += " |FAILED"
        elif flag == 2:
            logline += " |ABORT"
        logline += "| organization: |" + str(self.organization) + "| project: |" + str(project) + "| execute " + "|" + str(self.product_kind.upper())
        logline += "| force: |" + str(self.ctx.obj['force']) + "| skip-get-repositories: |" \
                   + str(self.ctx.obj['skip_get_repositories']) + "| skip-broken: |" + str(self.ctx.obj['skip_broken']) \
                   + "| url: |" + str(self.url)
        if self.ctx.obj['product_kind'] == 'copy':
            logline += "| src: |" + str(self.ctx.obj['src_path']) + "| des: |" + str(self.ctx.obj['des_path'])
        elif self.ctx.obj['product_kind'] == 'githubcli':
            logline += "| clistring: |" + str(self.ctx.obj['clistring'])
        # GithubTools.execute_CommandIgnoreReturn("echo '" + logline + "' >>" + FILE_PATH)
        GithubSystem.execute_CmdCommand("echo '" + logline + "' >>" + FILE_PATH)
        # print("log: " + logline)
        GithubSystem().show_logs(1)