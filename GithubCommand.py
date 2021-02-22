#!/usr/bin/env python3
# coding=utf-8
import json
import os

from GithubSystem import GithubSystem
from GithubWork import GithubWork

class GithubCommand:

    # 功能：提示用户输入初始化所需的 组织URL 等信息
    def configure(self, ctx):
        print("Set new URL successfully")
        # print(ctx.obj['url'])
        GithubSystem().set_prop("url", ctx.obj['url'])
        # print(GithubSystem().get_prop("url"))
        # GithubCommand.debug(ctx)
        # TODO:
        # 写入 meta/data.txt

    # 功能：Generate the repositories cache
    def repocache(self, ctx):
        # 通过url得到organization name
        organization = ctx.obj["url"].split("/")[len(ctx.obj["url"].split("/")) - 1]
        print('开始更新%s Github仓库列表...' % organization)
        # 清除本地已存在的项目列表
        GithubSystem.execute_CmdCommand(": > data/" + organization + "_repositories.txt")
        # 从github official api获取用户/个人的所用项目信息并存为json
        GithubSystem.execute_Command(
            'curl -s  https://api.github.com/users/' + organization + "/repos > data/repoapi.json"
        )
        # json -> python data
        with open('data/repoapi.json', 'r') as f:
            dict = json.load(f)
        # 对json中的每一个仓库信息进行遍历，找到仓库名并写入项目列表
        for repo in dict:
            GithubSystem.execute_Command(
                "echo " + repo['name'] + " >> data/" + organization + "_repositories.txt"
            )
            print(repo['name'])
        # 如果仓库列表为空
        if not os.path.getsize("data/" + organization + "_repositories.txt"):
            print("仓库列表为空，请检查您的组织/用户名或网络设置")
            GithubSystem.execute_CommandReturn("rm data/" + organization + "_repositories.txt")

    # 功能：backup all repositiries to Path
    def backup(self, ctx, path):
        print("[[backup]] function is running")
        print("path is: %s" % path)
        GithubCommand.debug(ctx)
        # TODO:
        # if path not null -> backup all repositories to Path/organization_20200122
        # else -> backup all repositories to pwd/organization_20200122

    # 功能：copy files or folder from source to destination
    def copy(self, ctx, src_path, des_path):
        print("[[copy]] function is running")
        print('src_path: %s' % src_path)
        print('des_path: %s' % des_path)
        print('url: %s' % ctx.obj['url'])
        # print(des_path[0])
        if des_path[0] != '/':
            print("des_path必须以/开头，来表示仓库根目录。")
            return

        # mauto = GithubFlow(ctx.obj['url'], ctx.obj['skip_get_repositories'], ctx.obj['skip_broken'], ctx.obj['force'],
        #                    "copy", src_path, des_path, None)
        # mauto.auto_make()
        ctx.obj['src_path'] = src_path
        ctx.obj['des_path'] = des_path
        ctx.obj['product_kind'] = 'copy'
        mauto = GithubWork(ctx)
        mauto.auto_make()


    # 功能：Move files or folder from source to destination
    #      Source and destination must be in the sane repository
    def move(self, ctx, src_path, des_path):
        print("[[move]] function is running")
        print('src_path: %s' % src_path)
        print('des_path: %s' % des_path)
        GithubCommand.debug(ctx)
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：Delete files or folder of repository
    def delete(self, ctx, path):
        print("[[delete]] function is running")
        print("path is: %s" % path)
        GithubCommand.debug(ctx)
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：rename the file or folder
    def rename(self, ctx, path, new_name):
        print("[[rename]] function is running")
        print("path is: %s" % path)
        print("new_name is: %s" % new_name)
        GithubCommand.debug(ctx)
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：根据指定的命令行，对单个文件进行内容替换，如果没有提供new_content
    #      则等同于删除old_content操作
    def replace(self, ctx, file_path, old_content, new_content):
        print("[[replace]] function is running")
        print("file_path is: %s" % file_path)
        print("old_content is: %s" % old_content)
        print("new_content is: %s" % new_content)
        if (new_content == None):
            print("Since not new_content is provided, old_content will be deleted from file_path")
        # GithubCommand.debug(ctx)
        # mauto = GithubFlow(ctx.obj['url'], ctx.obj['skip_get_repositories'], ctx.obj['skip_broken'], ctx.obj['force'],
        #                "replace", file_path, old_content, new_content)
        # mauto.auto_make()
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：更具指定的命令行，向指定文件的指定位置下方插入新的字段（支持多行）
    def lineinsert(self, ctx, file_path, line, content):
        print("[[lineinsert]] function is running")
        print("file_path is: %s" % file_path)
        print("line is: %s" % (line,))
        print("content is: %s" % content)
        for li in line:
            print("insert %s into line %s of %s" % (content, li, file_path))
        GithubCommand.debug(ctx)
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：基于jinja2，对模版进行实例化
    def format(self, ctx, template, variable):
        print("[[format]] function is running")
        print("template is: %s" % template)
        print("variable is: %s" % variable)
        GithubCommand.debug(ctx)
        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

    # 功能：执行Github官方的 [CLI](https://cli.github.com/manual/) 命令
    def githubcli(self, ctx, clistring):
        print("[[githubcli]] function is running")
        print("clistring is: %s" % clistring)
        # mauto = GithubFlow(ctx.obj['url'], ctx.obj['skip_get_repositories'], ctx.obj['skip_broken'], ctx.obj['force'],
        #                    "githubcli", None, None, clistring)
        # mauto.auto_make()
        ctx.obj['product_kind'] = "githubcli"
        ctx.obj['clistring'] = clistring
        mauto = GithubWork(ctx)
        mauto.auto_make()


    @staticmethod
    def debug(ctx):
        print("########## debug flag check ##########")
        print("url: %s" % ctx.obj['url'])
        print("skip-get-repositories: %s" % ctx.obj['skip_get_repositories'])
        print("skip-broken: %s" % ctx.obj['skip_broken'])
        print("force: %s" % ctx.obj['force'])
