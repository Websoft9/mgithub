import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--version', help='show the version.', is_flag=True)
@click.option('-l', '--logs', help='show the logs.', is_flag=True)
@click.option('-url',
              help='set your git URL, the default value is https://github.com/websoft9.',
              default='https://github.com/websoft9')
@click.option('--skip-get-repositories', help='skip get repositories.', is_flag=True)
@click.option('--skip-broken', help='skip command error and continue next repository.', is_flag=True)
@click.option('-f', '--force', help='do not prompt before overwriting.',is_flag=True)
def mgithub():
    pass


@mgithub.command()
@click.option('-url')
def configure(url):
    click.echo("running...")
    click.echo("the url: %s" % (url))
