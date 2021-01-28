import click
from GithubCommand import GithubCommand

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

command = GithubCommand()

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-v', '--version', help='show the version.', is_flag=True)
@click.option('-l', '--logs', help='show the logs.', is_flag=True)
@click.option('-url',
              help='set your git URL, the default value is https://github.com/websoft9.',
              prompt="url: ")
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
        click.echo("mgithub version 1.0.1")

    if logs:
        click.echo("Showing logs ....")

    print("url is %s" % url)
    if url is not None:
        click.echo("User setting URL ....")

    #
    # click.echo("################ option flag check: ")
    # click.echo("--version: %s" % version)
    # click.echo("--logs: %s" % logs)
    # click.echo("--url: %s" % url)
    # click.echo("--sgr: %s" % skip_get_repositories)
    # click.echo("--sb: %s" % skip_broken)
    # click.echo("--force: %s" % force)


# @mgithub.command()
# @click.option('-url', required=True, prompt=True)
# def configure(url):
#     click.echo("input url: ")

@mgithub.command()
@click.pass_context
def repocache(ctx):
    command.repocache(ctx)


@mgithub.command()
@click.pass_context
@click.argument('source_path', nargs=1, required=True)
@click.argument('destination_path', nargs=1, required=True)
def copy(ctx, source_path, destination_path):
    command.copy(source_path, destination_path)
