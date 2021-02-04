import os

from GithubFlow import GithubFlow
from GithubSystem import GithubSystem

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
        organization = ctx.obj["url"].split("/")[len(ctx.obj["url"].split("/")) - 1]
        print('开始更新%s Github仓库列表...' % organization)
        GithubSystem.execute_CommandWriteFile(
            'curl -s  https://api.github.com/users/' + organization + '/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
            "data/" + organization + "_repositories.txt"
        )
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
        # GithubCommand.debug(ctx)
        mauto = GithubFlow(ctx.obj['url'], ctx.obj['skip_get_repositories'], ctx.obj['skip_broken'], ctx.obj['force'],
                           "copy", src_path, des_path, None)
        mauto.auto_make()
        # print(GithubSystem().get_prop("repogrep").split(","))


        # TODO:
        # git_clone()
        # ...
        # push_repo()
        # print_log()

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
        GithubCommand.debug(ctx)
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
        mauto = GithubFlow(ctx.obj['url'], ctx.obj['skip_get_repositories'], ctx.obj['skip_broken'], ctx.obj['force'],
                           "githubcli", None, None, clistring)
        mauto.auto_make()
        # GithubCommand.debug(ctx)
        # TODO:
        # ...
        # print_log()

    @staticmethod
    def debug(ctx):
        print("########## debug flag check ##########")
        print("url: %s" % ctx.obj['url'])
        print("skip-get-repositories: %s" % ctx.obj['skip_get_repositories'])
        print("skip-broken: %s" % ctx.obj['skip_broken'])
        print("force: %s" % ctx.obj['force'])
