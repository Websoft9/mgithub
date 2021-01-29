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
from GithubSystem import GithubSystem

#!/usr/bin/env python3
# coding=utf-8
# *******************************************************************
# *** GithubProduct ***
# * Description:
#   what to do in github
# * Version:
#   v0.1
# * Author:
#   Qiaofeng1227
# *******************************************************************

class GithubCommand():


**configure**

功能：提示用户输入初始化所需的 组织URL 等信息

configure{

  input URL?  等待输入；
  ...
  写入 meta/data.txt
}

**repocache**

功能：Generate the repositories cache

repocache{

  get_list();
  write to data/organization_repositories.txt
}

**backup**

功能：backup all repositories to Path

backup(path){
    if path not null, backup all repositories to Path/organization_20200122
    else
       backup all repositories in the pwd/organization_20200122
}


**copy**

功能：copy files or folder from source to destination


copy(source_path, destination_path){
    git_clone();
    ...
    push_repo();
    print_log();
}


**move**

功能：Move files or folder from source to destination, source and destination must in the same repository


move(source_path, destination_path){
    git_clone();
    ...
    push_repo();
    print_log();
}

**delete**

功能：Delete files or folder of repository

delete(path){

    git_clone();
    ...
    push_repo();
    print_log();
}

**rename**

功能：rename the file or folder

rename(path, new_name){

    git_clone();
    ...
    push_repo();
    print_log();
}

**replace**

功能：根据指定的命令行，对单个文件进行内容替换，如果没有提供 new_content，则等同于删除 old_content 操作

replace(file_path, old_content, new_content){

    git_clone();
    ...
    push_repo();
    print_log();
}

**lineinsert**

功能：根据指定的命令行，向指定文件的指定位置下方插入新的字段（支持多行）

lineinsert(file_path, line, content){

    git_clone();
    ...
    push_repo();
    print_log();
}

**jinja2format**

功能：基于jinja2，对模板进行实例化

format(template, variable){

    git_clone();
    ...
    push_repo();
    print_log();
}

**githubcli**

功能：执行 Github 官方的 [CLI](https://cli.github.com/manual/) 命令 

githubcli(clistring){

    ...
    print_log();
}



 
