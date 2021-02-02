import click
import os
from GithubCommand import GithubCommand
from GithubSystem import GithubSystem

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

command = GithubCommand()

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-v', '--version', help='show the version.', is_flag=True)
@click.option('-l', '--logs', help='show the logs.', is_flag=True)
@click.option('--skip-get-repositories', help='skip get repositories.', is_flag=True)
@click.option('--skip-broken', help='skip command error and continue next repository.', is_flag=True)
@click.option('-f', '--force', help='do not prompt before overwriting.', is_flag=True)
@click.pass_context
def mgithub(ctx, version, logs, skip_get_repositories, skip_broken, force):
    if ctx.invoked_subcommand is None:
        os.system("mgithub -h")

    ctx.ensure_object(dict)
    ctx.obj['version'] = version
    ctx.obj['logs'] = logs
    ctx.obj['url'] = GithubSystem().get_prop("url")
    ctx.obj['skip_get_repositories'] = skip_get_repositories
    ctx.obj['skip_broken'] = skip_broken
    ctx.obj['force'] = force

    if version:
        click.echo("mgithub version 1.0.1")

    if logs:
        click.echo("Showing logs ....")


@mgithub.command(short_help="Input organization URL for initiation.")
@click.pass_context
@click.option('-url', nargs=1, prompt="input URL",
              help="Set your git URL, the default value is https://github.com/websoft9.")
def configure(ctx, url):
    ctx.obj['url'] = url
    command.configure(ctx)


@mgithub.command(short_help="Generate the repositories cache.")
@click.pass_context
def repocache(ctx):
    command.repocache(ctx)


@mgithub.command(short_help="Backup all repositories to path.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
def backup(ctx, path):
    command.backup(ctx, path)


@mgithub.command(short_help="Copy files or folder from source path to destination path.")
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def copy(ctx, source_path, destination_path):
    command.copy(ctx, source_path, destination_path)


@mgithub.command(short_help="Move files or folder from source path to destination path, \
                            source and destination path must be in the same repository.")
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def move(ctx, source_path, destination_path):
    command.move(ctx, source_path, destination_path)


@mgithub.command(short_help="Delete files or folder of repository.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
def delete(ctx, path):
    command.delete(ctx, path)


@mgithub.command(short_help="Rename the file or folder.")
@click.pass_context
@click.argument('path', nargs=1, required=True)
@click.argument('new_name', nargs=1, required=True)
def rename(ctx, path, new_name):
    command.rename(ctx, path, new_name)


@mgithub.command(short_help="Replace single file's content according to the specific command, \
                            if no new_content provided, old_content will be deleted from file.")
@click.pass_context
@click.argument('file_path', nargs=1, required=True)
@click.argument('old_content', nargs=1, required=True)
@click.argument('new_content', nargs=1, required=False)
def replace(ctx, file_path, old_content, new_content):
    command.replace(ctx, file_path, old_content, new_content)


@mgithub.command(short_help="Insert content under certain line (or multiple lines) of file accoring to the specific command.")
@click.pass_context
@click.argument('file_path', nargs=1, required=True)
@click.argument('line', nargs=-1, required=True)
@click.argument('content', nargs=1, required=True)
def lineinsert(ctx, file_path, line, content):
    command.lineinsert(ctx, file_path, line, content)


@mgithub.command(short_help="Instantiate template base on jinja2.")
@click.pass_context
@click.argument('template', nargs=1, required=True)
@click.argument('variable', nargs=1, required=True)
def format(ctx, template, variable):
    command.format(ctx, template, variable)


@mgithub.command(short_help="Execute official Github's CLI command.")
@click.pass_context
@click.argument('clistring', nargs=1, required=True)
def githubcli(ctx, clistring):
    command.githubcli(ctx, clistring)
