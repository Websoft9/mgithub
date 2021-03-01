#!/usr/bin/env python3
# coding=utf-8
import json
import click
import os
from GithubSystem import GithubSystem
from GithubWork import GithubWork

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-v', '--version', help='Show the version.', is_flag=True)
@click.option('-l', '--logs', help='Show the logs.', is_flag=True)
@click.option('--skip-get-repositories', help='Skip get repositories.', is_flag=True)
@click.option('--skip-broken', help='Skip command error and continue next repository.', is_flag=True)
@click.option('-f', '--force', help='Do not prompt before overwriting.', is_flag=True)
@click.pass_context
def mgithub(ctx, version, logs, skip_get_repositories, skip_broken, force):
    if ctx.invoked_subcommand is None and not version and not logs:
        os.system("mgithub -h")

    ctx.ensure_object(dict)
    ctx.obj['version'] = version
    ctx.obj['logs'] = logs
    ctx.obj['skip_get_repositories'] = skip_get_repositories
    ctx.obj['skip_broken'] = skip_broken
    ctx.obj['force'] = force
    ctx.obj['url'] = GithubSystem().get_prop("url")
    ctx.obj['organization'] = ctx.obj['url'].split("/")[len(ctx.obj['url'].split("/")) - 1]

    if version:
        click.echo("mgithub version 1.0.1")

    if logs:
        # click.echo("Showing logs ....")
        GithubSystem().show_logs(10)


@mgithub.command(short_help="Input organization URL for initiation.")
@click.pass_context
@click.option('-url', nargs=1, prompt="input URL",
              help="Set your git URL, the default value is https://github.com/websoft9.")
def configure(ctx, url):
    ctx.obj['url'] = url
    GithubSystem().set_prop("url", url)
    print("Set new URL successfully")


@mgithub.command(short_help="Backup all repositories to path.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
def backup(ctx, path):
    print("[[backup]] function is running")
    print("path is: %s" % path)
    # TODO


@mgithub.command(short_help="Copy files or folder from source path to destination path.")
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def copy(ctx, source_path, destination_path):
    if destination_path[0] != '/':
        print("des_path必须以/开头，来表示仓库根目录。")
        return
    print("[[copy]] function is running")
    print('src_path: %s' % source_path)
    print('des_path: %s' % destination_path)
    print('url: %s' % ctx.obj['url'])

    ctx.obj['src_path'] = source_path
    ctx.obj['des_path'] = destination_path
    ctx.obj['product_kind'] = 'copy'
    mauto = GithubWork(ctx)
    mauto.auto_make()


@mgithub.command(short_help="List all user/organization's projects into ORGNAME/USERNAME_repositories.txt")
@click.pass_context
def repocache(ctx):
    # 通过url得到organization name
    organization = ctx.obj["url"].split("/")[len(ctx.obj["url"].split("/")) - 1]
    print('开始更新%s Github仓库列表...' % organization)

    # 清除本地已存在的项目列表
    GithubSystem.execute_CmdCommand(": > data/" + organization + "_repositories.txt")

    page = 1
    dict = []
    while len(dict) != 0 or page == 1:
        # 从github official api获取用户/个人的所用项目信息并存为json
        GithubSystem.execute_Command(
            'curl -s  https://api.github.com/users/' + organization + "/repos\?per_page\=100\&page\=" + str(
                page) + "  > data/repoapi.json"
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

        page += 1

    # 如果仓库列表为空
    if not os.path.getsize("data/" + organization + "_repositories.txt"):
        print("仓库列表为空，请检查您的组织/用户名或网络设置")
        GithubSystem.execute_CommandReturn("rm data/" + organization + "_repositories.txt")


@mgithub.command(short_help="Move files or folder from source path to destination path, \
                            source and destination path must be in the same repository.")
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def move(ctx, source_path, destination_path):
    print("[[move]] function is running")
    print('src_path: %s' % source_path)
    print('des_path: %s' % destination_path)
    # TODO


@mgithub.command(short_help="Delete files or folder of repository.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
def delete(ctx, path):
    print("[[delete]] function is running")
    print("path is: %s" % path)
    # TODO


@mgithub.command(short_help="Rename the file or folder.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
@click.argument('new_name', nargs=1, required=True)
def rename(ctx, path, new_name):
    print("[[rename]] function is running")
    print("path is: %s" % path)
    print("new_name is: %s" % new_name)
    # TODO


@mgithub.command(short_help="Replace single file's content according to the specific command, \
                            if no new_content provided, old_content will be deleted from file.")
@click.pass_context
@click.argument('file_path', nargs=1, required=True)
@click.argument('old_content', nargs=1, required=True)
@click.argument('new_content', nargs=1, required=False)
def replace(ctx, file_path, old_content, new_content):
    print("[[replace]] function is running")
    print("file_path is: %s" % file_path)
    print("old_content is: %s" % old_content)
    print("new_content is: %s" % new_content)
    if new_content == None:
        print("Since not new_content is provided, old_content will be deleted from file_path")
    # TODO


@mgithub.command(
    short_help="Insert content under certain line (or multiple lines) of file accoring to the specific command.")
@click.pass_context
@click.argument('file_path', nargs=1, required=True)
@click.argument('line', nargs=-1, required=True)
@click.argument('content', nargs=1, required=True)
def lineinsert(ctx, file_path, line, content):
    print("[[lineinsert]] function is running")
    print("file_path is: %s" % file_path)
    print("line is: %s" % (line,))
    print("content is: %s" % content)
    for li in line:
        print("insert %s into line %s of %s" % (content, li, file_path))
    # TODO:


@mgithub.command(short_help="Instantiate template base on jinja2.")
@click.pass_context
@click.argument('template', nargs=1, required=True)
@click.argument('variable', nargs=1, required=True)
def format(ctx, template, variable):
    print("[[format]] function is running")
    print("template is: %s" % template)
    print("variable is: %s" % variable)
    # TODO:


@mgithub.command(short_help="Execute official Github's CLI command.")
@click.pass_context
@click.argument('clistring', nargs=1, required=True)
def githubcli(ctx, clistring):
    print("[[githubcli]] function is running")
    print("clistring is: %s" % clistring)

    ctx.obj['product_kind'] = "githubcli"
    ctx.obj['clistring'] = clistring
    mauto = GithubWork(ctx)
    mauto.auto_make()
