# Note for mgithub

## CLI框架构建--click

#### 测试用例——helloworld.py

helloworld.py
```buildoutcfg
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    hello()
```

setup.py
```buildoutcfg
from setuptools import setup

setup (
    name='hello',
    version='0.1',
    py_modules=['HelloWorld'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hello=HelloWorld:hello
    ''',
)
```
先试用python3 setup.py install, 即可对打包的命令进行cli实现。

#### Help Parameter Customization
统一help的格式，变为-h --help
```
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    pass
```

#### 使用group装饰器修饰commend function
```buildoutcfg
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()  # @cli, not @click!
def sync():
    click.echo('Syncing')
```

