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

#### CLI文件打包并使用
如使用虚拟环境需启动虚拟环境
```buildoutcfg
cd mgithub/backup
pip3 install --editable .
```
之后就可以直接使用mgithub命令，pip3命令需在GithubCLI.py， setup.py同目录下执行

#### 需要的package (推荐使用虚拟环境)
1. click 安装：pip3 install click
2. setuptools 安装：pip3 install setuptools

## mgithub-COPY

#### 整体执行步骤
1. 通过组织名，获取到组织下的所有project，并将其保存到orgName_repositories.txt文件（项目列表）。
2. 遍历项目列表，对列表中的project依次进行clone处理。
3. 再次遍历项目列表，对列表中的project进行相应command的操作。
4. 操作完成后，push
5. 对本次操作记录

#### 任务中断：异常抛出
1. 通过对可能抛出异常的cmd命令进行try-catch，将异常向上抛出。
2. 一旦捕获到异常，认为本项目操作失败，以--skip-broken来判断是否继续执行。
3. 对当前抛出异常对项目进行回滚处理。

#### 任务中断：Ctrl-C
1. 通过监听器在GithubFlow中监听用户的手动中断指令。
2. 如果在项目操作还未开始时ctrl-c，则认为当前项目列表中的第一个项目ABORT，并记录到log中。
3. 如果在项目执行过程中ctrl-c，则通过全局变量追踪到当前正在进行操作的project，以ABORT结束项目，
并对本项目进行回滚处理。

#### 任务中断：断点任务续执行
1. 先找到残存项目列表的第一个项目，再去日志中寻找最近的与本项目匹配的FAILED或ABORT记录
2. 通过记录的内容，覆盖当前GithubFlow中的变量，从而起到恢复上次工作状态的作用。
3. 接下来的操作与正常执行任务相同
4. 问题：假设有ABCD四个项目，如果在没有加--skip-broken的情况下，B项目抛出异常并终止。
下次对断点任务进行续执行，本任务将会由于B项目的异常永远阻塞（因为续执行任务的命令与上次中断时
保持一致），CD两个项目永远无法执行到。

## mgithub-githubCLI-secret

#### 创建新的secret
官方CLI创建新的secret的命令：gh secret set -R"repo_name" secret_name -b"secret_value"
```buildoutcfg
gh secret set -R"mgithubTestOrg/projAAA" SECRET_1 -b"abcdefg666"
```
在代码中，将不需要用户手动输入—R来确定仓库名，用户只需要输入：
```buildoutcfg
mgithub githubcli gh secret set SECRET_1 -b"abcdefg666"
```
则会为组织下的所有仓库批量创建一个名为SECRET_1值为abcdefg666的secret。
如果用户使用-f option，则会强行覆盖已经存在的同名secret，反之则不会。

#### 删除已经存在的secret
官方CLI删除secret的命令：gh secret remove -R"repo_name" secret_name
```buildoutcfg
gh secret remove -R"mgithubTestOrg/projAAA" SECRET_1
```
在代码中，将不需要用户手动输入—R来确定仓库名，用户只需要输入：
```buildoutcfg
mgithub githubcli gh secret remove SECRET_1
```
则会将组织下所有仓库内名为SECRET_1的secret进行批量删除，如果未找到，则抛出异常。
可通过--skip-broken进行强制续执行
