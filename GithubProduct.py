#!/usr/bin/env python3
# coding=utf-8
from GithubException import CustomException
from GithubSystem import GithubSystem


class GithubProduct:

    def __init__(self, ctx):
        self.ctx = ctx

    def copy(self, project):
        # 判断是否需要强制覆盖文件
        if self.ctx.obj['force']:
            print("\n执行强制覆盖的copy动作...")
            cmd = "cp -rf " + self.ctx.obj['src_path'] + " data/" + self.ctx.obj['organization'] + "/" + project + \
                  self.ctx.obj['des_path']
        else:
            print("\n执行不覆盖的copy动作...")
            cmd = "cp -nr " + self.ctx.obj['src_path'] + " data/" + self.ctx.obj['organization'] + "/" + project + \
                  self.ctx.obj['des_path']
        # 执行相应的COPY命令
        try:
            GithubSystem.execute_CmdCommand(cmd)
        except CustomException as e:
            raise e

    def githubcli(self, project):
        if len(self.ctx.obj['clistring']) >= 3:
            # clistring: gh secret set ...
            if self.ctx.obj['clistring'].split(" ")[1] == "secret" and self.ctx.obj['clistring'].split(" ")[2] == "set":
                # 转移到本地的相对应仓库目录下
                cd_cmd = "cd data/" + self.ctx.obj['organization'] + "/" + project + ";"
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
                    cmd = "gh secret list -R " + self.ctx.obj['organization'] + "/" + project \
                          + "| grep -c ^" + secret_key
                    rcontent = GithubSystem.execute_GitCommand(cmd)[1]
                    # 不存在则正常创建一个新的secret
                    if rcontent == "0":
                        GithubSystem.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])

            # clistring: gh secret remove ...
            elif self.ctx.obj['clistring'].split(" ")[1] == "secret" and self.ctx.obj['clistring'].split(" ")[
                2] == "remove":
                # 转移到本地的相对应仓库目录下
                cd_cmd = "cd data/" + self.ctx.obj['organization'] + "/" + project + ";"
                print("\n正在执行批量删除Secret设置")
                GithubSystem.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])
            else:
                print("\nmgithub githubcli目前不支持此命令")
