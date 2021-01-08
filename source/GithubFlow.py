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
    def auto_make(self, organization, productkind, sourcepath, despath, cmd): 

        print("==============start automake task ============== ")

        # 先判断模板是否存在，是否有内容
        # 根据对象组织确定模板文件
        repository_cache_str = "data/repositories_cache.txt"
        repository_str = "data/repositories.txt"
        if organization == "template":
            repository_cache_str = 'data/repositories_cache.txt'
            repository_str = "data/repositories.txt"
        elif organization == "role":
            repository_cache_str = 'data/dev_repositories_cache.txt'
            repository_str = "data/repositories_cache.txt"
        else: 
            print('\n\t>>>目前仅存在template和role，无法进行自动化操作，请确认后更换命令再试！')
            return

        # 判断缓存文件是否存在
        cathe_path=repository_cache_str
        if os.path.isdir(cathe_path):  
            ## 缓存文件存在，需要继续判断文件内容是否为空
            # 判断缓存是否为空 ，如果不为空， 说明上次任务未完成，提示用户执行
            file_object=open(repository_cache_str)
            project_list=file_object.readlines()
            if project_list :
                print("上次自动化构建任务尚未完成，请确认是否继续当前任务！")
                print("未完成清单内容如下：")
                GithubTools.execute_CommandReturn('cat '+ repository_cache_str)
                print("上次执行的任务日志如下（最新10条）：")
                #GithubTools.execute_CommandReturn('cat '+ logfile)

                # 选择继续任务还是
                continue_id=self.continue_select()

                ## 仅仅根据缓存列表完成 上次未完成的项目
                if continue_id == "0": 
                    self.automake_cache(organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str)
                    return
                else:# 退出让用户自行输入命令再次执行
                    print("已经清空所有未完成任务，请重新输入命令再次执行!")
                    GithubTools.execute_Command('cat data/repositories_cache.txt > data/repositories.txt')
                    return
                    
            else :
                pass

        else:
            # 缓存文件不存在, 创建空的缓存文件
            GithubTools.execute_CommandReturn('touch '+ repository_cache_str)

        repo_path=repository_str
        if os.path.isdir(repo_path):  
            ## 清单文件存在，需要继续判断文件内容是否为空
            # 判断清单为空 ，如果不为空， 说明上次任务未完成，提示用户执行
            file_object=open(repository_str)
            project_list=file_object.readlines()
            if project_list :
                print("清单里有未完成的任务列表，请确认对列表内容！")
                print("未完成清单内容如下：")
                GithubTools.execute_CommandReturn('cat '+ repository_str)

                # 选择继续任务还是
                continue_id=self.continue_selectlist()

                ## 仅仅根据清单列表完成 上次未完成的项目
                if continue_id == "0":               
                    self.automake_list(organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str)
                    return
                else:# 退出让用户自行输入命令再次执行
                    print('\n\t>>>即将清空清单列表，然后重新从github上获取最新列表')
                    GithubTools.execute_CommandReturn('echo "" '+ repository_str)
                    pass
                    
            else :
                pass

        else:
            # 清单文件不存在, 创建空清单文件
            GithubTools.execute_CommandReturn('touch '+ repository_str)

        self.automake_new(organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str)
    
    def automake_new(self, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str):

        print('\n\t>>>自动化任务开始，将从github下载最新的项目列表后开始构建')
        # 下载最新的template模板
        downloadflag=GithubTools.execute_CommandReturn('git clone --depth=1 git@github.com:Websoft9test/ansible-template.git data/ansible-template/')
        # 正确执行--template还不存在
        if downloadflag==0:
            pass
        else:
            # 将template更新到最新
            GithubTools.execute_CommandReturn('git pull')

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

    def automake_list(self, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str):

        print('\n\t>>>自动化任务开始，根据已有清单列表开始构建')
        # 下载最新的template模板
        downloadflag=GithubTools.execute_CommandReturn('git clone --depth=1 git@github.com:Websoft9test/ansible-template.git data/ansible-template/')
        # 正确执行--template还不存在
        if downloadflag==0:
            pass
        else:
            # 将template更新到最新
            GithubTools.execute_CommandReturn('git pull')

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
    
   def automake_cache(self, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str):

        print('\n\t>>>自动化任务开始，根据已有缓存列表开始构建')
        # 下载最新的template模板
        downloadflag=GithubTools.execute_CommandReturn('git clone --depth=1 git@github.com:Websoft9test/ansible-template.git data/ansible-template/')
        # 正确执行--template还不存在
        if downloadflag==0:
            pass
        else:
            # 将template更新到最新
            GithubTools.execute_CommandReturn('git pull')

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

    #选择继续操作
    #格式：选择是否在上次任务上继续：  \n\t 0. 继续 \n\t 1. 终止退出  \n\n\t选择:
    def continue_select(self):
        input_str = "\n\t缓存任务尚未完成，是否继续上次任务：  \n\n\t "
        i = 0
        
        for x in ['继续进行当前执行的自动化操作','终止退出']:
            input_str = input_str + str(i) + "." + x + " \n\t "          
            i = i+1
        input_str = input_str + "\n\t选择: "
        continue_id = input(input_str)
        while continue_id not in ['0','1']:
          print('\n\t输入错误，请重新选择')
          continue_id = input(input_str)
        return continue_id

    def continue_selectlist(self):
        input_str = "\n\t清单任务尚未完成，是否继续上次任务：  \n\n\t "
        i = 0
        
        for x in ['仅对当前清单剩余任务执行的自动化操作','更新清单后执行自动化操作']:
            input_str = input_str + str(i) + "." + x + " \n\t "          
            i = i+1
        input_str = input_str + "\n\t选择: "
        continue_id = input(input_str)
        while continue_id not in ['0','1']:
          print('\n\t输入错误，请重新选择')
          continue_id = input(input_str)
        return continue_id

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