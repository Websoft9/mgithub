#!/usr/bin/env python3
# coding=utf-8
import json
import os

from GithubUtil import GithubHelperFunc
from GithubException import CustomException

class GithubSystemCmd():

    def __init__(self, ctx):
        self.ctx = ctx

    def repocache(self):
        # 通过url得到organization name
        organization = self.ctx.obj["url"].split("/")[len(self.ctx.obj["url"].split("/")) - 1]
        print('开始更新%s Github仓库列表...' % organization)

        # 清除本地已存在的项目列表
        GithubHelperFunc.execute_CmdCommand(": > data/" + organization + "_repositories.txt")

        page = 1
        dict = []
        while len(dict) != 0 or page == 1:
            # 从github official api获取用户/个人的所用项目信息并存为json
            if self.ctx.obj['client']:
                client_id = GithubHelperFunc().get_prop("client_id")
                client_secrets = GithubHelperFunc().get_prop("client_secrets")
                GithubHelperFunc.execute_Command(
                    'curl -u ' + client_id + ':' + client_secrets + ' https://api.github.com/users/' + organization + "/repos\?per_page\=100\&page\=" + str(
                        page) + "  > data/repoapi.json"
                )
            else:
                GithubHelperFunc.execute_Command(
                    'curl -s  https://api.github.com/users/' + organization + "/repos\?per_page\=100\&page\=" + str(
                        page) + "  > data/repoapi.json"
                )


            # json -> python data
            with open('data/repoapi.json', 'r') as f:
                dict = json.load(f)

            # 对json中的每一个仓库信息进行遍历，找到仓库名并写入项目列表
            for repo in dict:

                if self.ctx.obj['release']:

                    if self.ctx.obj['client']:
                        client_id = GithubHelperFunc().get_prop("client_id")
                        client_secrets = GithubHelperFunc().get_prop("client_secrets")
                        GithubHelperFunc.execute_Command(
                            'curl -u ' + client_id + ':' + client_secrets + ' https://api.github.com/repos/' + organization + "/" +
                            repo['name'] + "/tags > data/repotag.json"
                        )
                    else:
                        GithubHelperFunc.execute_Command(
                            'curl -s https://api.github.com/repos/' + organization + "/" +
                            repo['name'] + "/tags > data/repotag.json"
                        )

                    with open('data/repotag.json', 'r') as f1:
                        dict_tag = json.load(f1)
                    if len(dict_tag) != 0:

                        # if len(dict_tag['message']) > 0:
                        #     raise CustomException("API rate limit exceeded for 175.13.97.100.")
                        version = dict_tag[0]['name']
                        record = repo['name'] + " " + version
                    else:
                        record = repo['name']
                else:
                    record = repo['name']

                GithubHelperFunc.execute_Command(
                    "echo " + record + " >> data/" + organization + "_repositories.txt"
                )
                print(record)

            page += 1

        # 如果仓库列表为空
        if not os.path.getsize("data/" + organization + "_repositories.txt"):
            print("仓库列表为空，请检查您的组织/用户名或网络设置")
            GithubHelperFunc.execute_CommandReturn("rm data/" + organization + "_repositories.txt")

        print()