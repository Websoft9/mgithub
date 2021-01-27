from setuptools import setup

setup(
    name='mgithub',
    version='0.1',
    py_modules=['GithubCLI'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mgithub=GithubCLI:mgithub
    ''',
)
