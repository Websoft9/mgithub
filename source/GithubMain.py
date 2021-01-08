#!/usr/bin/env python3
# coding=utf-8
# *******************************************************************
# *** GithubProcess ***
# * Description:
#   Auto Makeup Github repositories
# * Version:
#   v0.1
# * Author:
#   Qiaofeng1227
# *******************************************************************
# Modules
import json
import os, io, sys, platform, shutil, urllib3, time
try:
    import queue
except ImportError:
    import Queue as queue
import threading
import time

import argparse
import git
import requests
from GithubFlow import GithubFlow


class GithubMain():

    print(sys.argv)

    # copy：复制模板文件（或文件夹）到github项目 delete: 删除github项目某个路径下所有文件或者目录 modify:对github的文件进行cmd操作，例如字符串替换等
    # format：根据模板文件的format重新生成到github项目 branch:对github的项目进行分支操作，如建新分支dev，main，删除master分支，并设置main为default
    # backup:备份项目 other:目前没有明确的需求，待追加
    product_content="copy"

    # role||template
    org_code="template"  

    # local path
    sourcepath=""

    # github path
    despath=""

    # 执行命令
    cmd=""

    mauto=GithubFlow()

    mauto.auto_make(org_code, product_content, sourcepath, despath, cmd)
    

