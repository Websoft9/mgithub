import click
from GithubCommand import GithubCommand

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# class option:
#     version = False
#     logs = False
#     url = "https://github.com/websoft"
#     skip_get_repositories = False
#     skip_broken = False
#     force = False
#
#     def __init__(self, version, logs, url, skip_get_repositories, skip_broken, force):
#         self.version = version
#         self.logs = logs
#         self.url = url
#         self.skip_get_repositories = skip_get_repositories
#         self.skip_broken = skip_broken
#         self.force = force

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-v', '--version', help='show the version.', is_flag=True)
@click.option('-l', '--logs', help='show the logs.', is_flag=True)
@click.option('-url',
              help='set your git URL, the default value is https://github.com/websoft9.',
              default='https://github.com/websoft9')
@click.option('--skip-get-repositories', help='skip get repositories.', is_flag=True)
@click.option('--skip-broken', help='skip command error and continue next repository.', is_flag=True)
@click.option('-f', '--force', help='do not prompt before overwriting.', is_flag=True)
@click.pass_context
def mgithub(ctx, version, logs, url, skip_get_repositories, skip_broken, force):

    ctx.ensure_object(dict)
    ctx.obj['version'] = version
    ctx.obj['logs'] = logs
    ctx.obj['url'] = url
    ctx.obj['skip_get_repositories'] = skip_get_repositories
    ctx.obj['skip_broken'] = skip_broken
    ctx.obj['force'] = force

    if version:
        click.echo("version is true")

    click.echo("################ option flag check: ")
    click.echo("--version: %s" % version)
    click.echo("--logs: %s" % logs)
    click.echo("--url: %s" % url)
    click.echo("--sgr: %s" % skip_get_repositories)
    click.echo("--sb: %s" % skip_broken)
    click.echo("--force: %s" % force)

@click.option('-v', '--version', help='show the version.', is_flag=True)
@click.command()
def version(ctx, version):
    click.echo("Version 0.1")

@mgithub.command()
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def copy(ctx, source_path, destination_path):
    click.echo("source: %s" % source_path)
    click.echo("des: %s" % destination_path)
    command = GithubCommand()
    command.copy(source_path, destination_path)
    click.echo("################ option flag check: ")
    click.echo("--version: %s" % ctx.obj['version'])
    click.echo("--logs: %s" % ctx.obj['logs'])
    click.echo("--url: %s" % ctx.obj['url'])
    click.echo("--sgr: %s" % ctx.obj['skip_get_repositories'])
    click.echo("--sb: %s" % ctx.obj['skip_broken'])
    click.echo("--force: %s" % ctx.obj['force'])
