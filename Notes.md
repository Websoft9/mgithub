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

#### 使用pass_context在父子命令之间传参
每当命令被调用时，click 会创建新的上下文，并链接到父上下文。通常，我们是看不到上下文信息的。但我们可以通过 pass_context 装饰器来显式让 click 传递上下文，此变量会作为第一个参数进行传递。
```buildoutcfg
@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # 确保 ctx.obj 存在并且是个 dict。 (以防 `cli()` 指定 obj 为其他类型
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))

if __name__ == '__main__':
    cli(obj={})
```

#### 让mgithub主command脱离子command进行工作
```buildoutcfg
@click.group(invoke_without_command=True)
```

#### 在只键入mgithub的情况下依然显示help信息
因为mgithub可脱离子命令单独执行，所以正常情况mgithub将会被视为合法命令。
使用以下python语句，在mgithub后无参数无子命令时，执行命令行"mgithub -h"从而达到显示help信息的功能
```buildoutcfg
if ctx.invoked_subcommand is None:
     os.system("mgithub -h")
```

#### command 读入多个argument
使用以下命令读入多个参数，参数将会存放在一个名为line的python tuple内
```buildoutcfg
@click.argument('line', nargs=-1, required=True)
```

