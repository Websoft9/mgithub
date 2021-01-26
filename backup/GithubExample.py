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

    org_code="template"  # role||template

    # 0：自动化构建readme文档（中文） 1:自动化构建readme文档（英文） 2:自动化构建issue标准模板 3:workflows（目前已有文档自动化构建程序）
    # 4：自动化替换标题栏图标  5:自动化构建产品文件夹 6:创建dev分支main分支，并删除master分支 7:backup
    product_code="4"

    mauto=GithubFlow()

    mauto.auto_make(org_code,product_code)
    

