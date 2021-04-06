#!/usr/bin/env python3
# coding=utf-8
import os
import click
import sys

from GithubSystemCmd import GithubSystemCmd
from GithubUtils import GithubUtils
from GithubWork import GithubWork
from GithubException import CustomException

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
    ctx.obj['url'] = GithubUtils().get_prop("mgithub","meta/mgithub.config","url")
    ctx.obj['organization'] = ctx.obj['url'].split("/")[len(ctx.obj['url'].split("/")) - 1]
    # 通过sys.argv记录用户输入的命令
    ctx.obj['command'] = "mgithub"
    # config parameter
    ctx.obj['config_item'] = "mgithub"
    ctx.obj['config_path'] = "meta/mgithub.config"

    i = 1
    while i < len(sys.argv):
        ctx.obj['command'] += " " + sys.argv[i]
        i += 1

    if version:
        click.echo("mgithub version 1.0.1")

    if logs:
        # click.echo("Showing logs ....")
        GithubUtils().show_logs(10)


@mgithub.command(short_help="Input organization URL for initiation.")
@click.pass_context
@click.option('-url', nargs=1, prompt="input URL",
              help="Set your git URL, the default value is https://github.com/websoft9.")
def configure(ctx, url):
    ctx.obj['url'] = url
    GithubUtils().set_prop(ctx.obj['config_item'],ctx.obj['config_path'],"url", url)
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
@click.option('-v', '--version', help='Show the release version in project list.', is_flag=True)
@click.option('-c', '--client', help='Use clentID to fetch the repo info.', is_flag=True)
@click.pass_context
def repocache(ctx, version, client):
    ctx.obj['release'] = version
    ctx.obj['client'] = client
    command = GithubSystemCmd(ctx)
    try:
        command.repocache()
    except CustomException as e:
        print(e.msg)


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
    ctx.obj['path'] = path
    ctx.obj['product_kind'] = 'delete'
    mauto = GithubWork(ctx)
    mauto.auto_make()


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
@click.option('-role', help='replace role_template in role_XXX/tests/test.yml', is_flag=True)
def replace(ctx, file_path, old_content, new_content, role):
    print("[[replace]] function is running")
    print("file_path is: %s" % file_path)
    print("old_content is: %s" % old_content)
    print("new_content is: %s" % new_content)
    ctx.obj['file_path'] = file_path
    ctx.obj['old_content'] = old_content
    if new_content is None:
        print("Since not new_content is provided, old_content will be deleted from file_path")
        ctx.obj['new_content'] = ""
    else:
        ctx.obj['new_content'] = new_content
    ctx.obj['product_kind'] = 'replace'
    ctx.obj['role'] = role
    mauto = GithubWork(ctx)
    mauto.auto_make()



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

@mgithub.command(short_help="Clone all github repositories in local project_list.")
@click.pass_context
def clone(ctx):
    command = GithubSystemCmd(ctx)
    try:
        command.clone()
    except CustomException as e:
        print(e.msg)
