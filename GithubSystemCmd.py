#!/usr/bin/env python3
# coding=utf-8
import json
import os

from GithubUtils import GithubUtils
from GithubException import CustomException

#########################################
#          GithubSystemCmd             #
# mgithub system setting command       #
# Created by: Haozhe Chen              #
#########################################

class GithubSystemCmd():

    def __init__(self, ctx):
        self.ctx = ctx

    def repocache(self):
        # 通过url得到organization name
        organization = self.ctx.obj["url"].split("/")[len(self.ctx.obj["url"].split("/")) - 1]
        print('开始更新%s Github仓库列表...' % organization)

        # 清除本地已存在的项目列表
        GithubUtils.execute_CmdCommand(": > data/" + organization + "_repositories.txt")

        page = 1
        dict = []
        while len(dict) != 0 or page == 1:
            # 从github official api获取用户/个人的所用项目信息并存为json
            if self.ctx.obj['client']:
                client_id = GithubUtils().get_prop(self.ctx.obj["config_item"], self.ctx.obj["config_path"],
                                                        "client_id")
                client_secrets = GithubUtils().get_prop(self.ctx.obj["config_item"], self.ctx.obj["config_path"],
                                                             "client_secrets")
                GithubUtils.execute_CmdCommand(
                    'curl -u ' + client_id + ':' + client_secrets + ' https://api.github.com/users/' + organization + "/repos\?per_page\=100\&page\=" + str(
                        page) + "  > data/repoapi.json"
                )
            else:
                GithubUtils.execute_CmdCommand(
                    'curl -s  https://api.github.com/users/' + organization + "/repos\?per_page\=100\&page\=" + str(
                        page) + "  > data/repoapi.json"
                )

            # json -> python data
            with open('data/repoapi.json', 'r') as f:
                dict = json.load(f)

            if 'message' in dict:
                break

            # 对json中的每一个仓库信息进行遍历，找到仓库名并写入项目列表
            for repo in dict:

                if self.ctx.obj['release']:

                    if self.ctx.obj['client']:
                        client_id = GithubUtils().get_prop(self.ctx.obj["config_item"],
                                                                self.ctx.obj["config_path"], "client_id")
                        client_secrets = GithubUtils().get_prop(self.ctx.obj["config_item"],
                                                                     self.ctx.obj["config_path"], "client_secrets")
                        GithubUtils.execute_CmdCommand(
                            'curl -u ' + client_id + ':' + client_secrets + ' https://api.github.com/repos/' + organization + "/" +
                            repo['name'] + "/tags > data/repotag.json"
                        )
                    else:
                        GithubUtils.execute_CmdCommand(
                            'curl -s https://api.github.com/repos/' + organization + "/" +
                            repo['name'] + "/tags > data/repotag.json"
                        )

                    with open('data/repotag.json', 'r') as f1:
                        dict_tag = json.load(f1)
                    if len(dict_tag) != 0:
                        version = dict_tag[0]['name']
                        record = repo['name'] + " " + version
                    else:
                        record = repo['name']
                else:
                    record = repo['name']

                GithubUtils.execute_CmdCommand(
                    "echo " + record + " >> data/" + organization + "_repositories.txt;" +
                    "cat data/" + organization + "_repositories.txt | awk 'END {print}'"
                )

            page += 1

        # 如果仓库列表为空
        if not os.path.getsize("data/" + organization + "_repositories.txt"):
            print("仓库列表为空，请检查您的组织/用户名或网络设置")
            # GithubHelperFunc.execute_CommandReturn("rm data/" + organization + "_repositories.txt")
            GithubUtils.execute_CmdCommand("rm data/" + organization + "_repositories.txt")
        else:
            print()

    def clone(self):

        self.ctx.obj['repo_str'] = "data/" + self.ctx.obj['organization'] + "_repositories.txt"
        if os.path.isfile(self.ctx.obj['repo_str']):
            if len(open(self.ctx.obj['repo_str']).read().splitlines()) == 0:
                # 空的项目列表
                raise CustomException("项目列表为空，请执行mgithub [option] repocache来获取本组织/用户的项目列表")

        project_list = []
        for line in open(self.ctx.obj['repo_str']).read().splitlines():
            info = line.split(" ")
            project_list.append(info[0])

        print("正在将本组织下的仓库clone到本地...\n")
        for proj in project_list:
            FILE_PATH = "data/" + self.ctx.obj['organization'] + "/" + proj
            if os.path.isdir(FILE_PATH):
                print("本地仓库" + proj + "已存在：正在更新")
                # 存在：使用git pull对本地仓库进行更新
                cmd = "cd " + FILE_PATH + "; git pull"
                try:
                    GithubUtils.execute_CmdCommand(cmd)
                except CustomException as e:
                    raise e
            else:
                print("git clone from " + proj + "....")
                cmd = "git clone  " + self.ctx.obj['url'] + "/" + proj + ".git data/" + self.ctx.obj[
                    'organization'] + "/" + proj
                try:
                    GithubUtils.execute_CmdCommand(cmd)
                except CustomException as e:
                    # 仓库clone未成功，结束本次任务
                    if str(self.ctx.obj['skip_broken']) == "True":
                        print(proj + ": 本仓库clone失败")
                    else:
                        print("仓库clone未成功，结束本次任务")
                        raise e
            print()
