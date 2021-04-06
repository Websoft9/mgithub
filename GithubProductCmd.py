#!/usr/bin/env python3
# coding=utf-8
import os

from GithubException import CustomException
from GithubUtils import GithubUtils

#########################################
#          GithubProductCmd             #
# mgithub core operation product        #
# Created by: Haozhe Chen               #
#########################################

class GithubProductCmd:

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
            GithubUtils.execute_CmdCommand(cmd)
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
                    GithubUtils.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])
                else:
                    # 不覆盖
                    print("\n正在执行不强制覆盖的New Secret设置")
                    # 判断当前项目中是否存在相同key的secret
                    cmd = "gh secret list -R " + self.ctx.obj['organization'] + "/" + project \
                          + "| grep -c ^" + secret_key
                    rcontent = GithubUtils.execute_CmdCommand(cmd)[1]
                    # 不存在则正常创建一个新的secret
                    if rcontent == "0":
                        GithubUtils.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])

            # clistring: gh secret remove ...
            elif self.ctx.obj['clistring'].split(" ")[1] == "secret" and self.ctx.obj['clistring'].split(" ")[
                2] == "remove":
                # 转移到本地的相对应仓库目录下
                cd_cmd = "cd data/" + self.ctx.obj['organization'] + "/" + project + ";"
                print("\n正在执行批量删除Secret设置")
                GithubUtils.execute_CmdCommand(cd_cmd + self.ctx.obj['clistring'])
            else:
                print("\nmgithub githubcli目前不支持此命令")

    def delete(self, project):
        localfile_path = "data/" + self.ctx.obj['organization'] + "/" + project + self.ctx.obj['path']
        if not os.path.exists(localfile_path):
            raise CustomException(
                "\nThe target file doesn't exist.\nmgithub commend will abort, you can use "
                "--skip-broken to jump over this abort.")
        if self.ctx.obj['force']:
            cmd = "rm -fr " + localfile_path
        else:
            cmd = "rm -ir " + localfile_path
        try:
            GithubUtils.execute_InteractiveCommand(cmd)
        except CustomException as e:
            raise e
        print("删除操作已完成")

    def replace(self, project):
        localfile_path = "data/" + self.ctx.obj['organization'] + "/" + project + self.ctx.obj['file_path']
        if not os.path.isfile(localfile_path):
            raise CustomException(
                "\nThe target file doesn't exist or is not a writable file.\nmgithub commend will abort, you can use "
                "--skip-broken to jump over this abort.")
        if self.ctx.obj['role']:
            # cmd = "sed -i '' 's/" + self.ctx.obj['old_content'] + "/" + project + "/g' " + localfile_path
            cmd = "sed -i 's/" + self.ctx.obj['old_content'] + "/" + project + "/g' " + localfile_path
        else:
            # cmd = "sed -i '' 's/" + self.ctx.obj['old_content'] + "/" + self.ctx.obj[
            #     'new_content'] + "/g' " + localfile_path
            cmd = "sed -i 's/" + self.ctx.obj['old_content'] + "/" + self.ctx.obj[
                'new_content'] + "/g' " + localfile_path
        try:
            GithubUtils.execute_CmdCommand(cmd)
        except CustomException as e:
            raise e
        print("替换操作已完成")

    def format(self, project):
        pass

    def branch(self, project):
        pass

    def backup(self, project):
        pass
