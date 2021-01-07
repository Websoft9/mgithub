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
from GithubTools import GithubTools
from GithubProduct import GithubProduct

class GithubFlow():

    # 根据组织确定需要作业的范围对象,对所有对象循环处理要做的自动化处理
    def auto_make(self, organization, productkind):  

        print("start automake task from " + organization)

        # 下载最新的template模板
        GithubTools.execute_Command('git clone --depth=1 https://github.com/Websoft9test/ansible-template.git data/ansible-template/')

        # get the project list from organization
        repository_str = "data/repositories.txt"
        repository_cache_str = "data/repositories_cache.txt"
        if organization == "template":
            repository_str = 'data/repositories.txt' 
            repository_cache_str = 'data/repositories_cache.txt'
        elif organization == "role":
            repository_str = 'data/dev_repositories.txt' 
            repository_cache_str = 'data/dev_repositories_cache.txt'
        else: 
            print('\n\t>>>无匹配的组织，无法生成列表文件')

        # 判断缓存是否为空 ，如果不为空， 说明上次任务未完成，提示用户执行
        file_object=open(repository_cache_str)
        project_list=file_object.readlines()
        if project_list :
            print("已经存在未完成的自动化构建任务")
        else :
            # 生成文件列表
            self.create_repository(organization)
            # 复制文件到缓存
            self.create_cache(organization)

            file_object=open(repository_cache_str)
            #project_list=file_object.readlines()
            project_list = file_object.read().splitlines()

            product=GithubProduct()
            for project_name in project_list:
 
                if productkind == "0" :
                    # 生成中文文档
                    product.product_readme_cn(project_name, organization)

                elif productkind == "1" :
                    # 生成英文文档
                    product.product_readme_en(project_name, organization)

                elif productkind == "2" :
                    # issue标准模板
                    product.product_issue_template(project_name, organization)

                elif productkind == "3" :
                    # workflows
                    product.product_workflows(project_name, organization)

                elif productkind == "4" :
                    # 产品文件夹（含其中文档）
                    product.product_prdfiles(project_name, organization)

                elif productkind == "5" :
                    # 创建main分支 dev分支，并删除master分支
                    product.product_resetbranches(project_name, organization)

                elif productkind == "6" :
                    # github工程备份
                    product.product_backup(project_name, organization)


    # 根据organization生成最新的repository文件列表
    def create_repository(self, organization):

        print("====create_cache from repositories====")

        # get the project list from organization
        repository_cache_str = 'data/repositories_cache.txt'

        if organization == "template" :
            print(('\n开始更新Websoft9 Github仓库列表\n'))
            # GithubTools.execute_CommandWriteFile('curl -s  https://api.github.com/orgs/websoft9/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'| grep -E "^ansible-*"','data/repositories.txt')
            GithubTools.execute_CommandWriteFile('curl -s  https://api.github.com/orgs/websoft9test/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'| grep -E "^ansible-lcmp*"','data/repositories.txt')
        elif organization == "role" :
            print(('\n开始更新Websoft9dev Github仓库列表\n'))
            # GithubTools.execute_CommandWriteFile('curl -s  https://api.github.com/orgs/websoft9dev/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'| grep -E "^role_*"','data/dev_repositories.txt')
            GithubTools.execute_CommandWriteFile('curl -s  https://api.github.com/orgs/websoft9test/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'| grep -E "^role_-*"','data/dev_repositories.txt')       

    # 复制文件到缓存
    def create_cache(self, organization):

        print("====create_cache from repositories====")

        print(('\n开始更新缓存文件\n'))
        if organization == "template" :
            GithubTools.execute_Command('cat data/repositories.txt > data/repositories_cache.txt')
        elif organization == "role" :
            GithubTools.execute_Command('cat data/dev_repositories.txt > data/dev_repositories_cache.txt')