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

class GithubProduct():
    
    # 根据模板生成中文文档
    def product_readme_cn(self, projectname, organization):

        print("根据模板在本地生成中文文档")


    # 根据模板生成英文文档
    def product_readme_en(self, projectname, organization):

        print(projectname +"根据模板在本地生成英文文档")
  
    
    # 在本地复制issue标准模板
    def product_issue_template(self, projectname, organization):

        print(projectname +"将template工程下issue模板复制到本地")

    # 在本地复制workflows
    def product_workflows(self, projectname, organization):

        print(projectname +"将template工程下workflows模板复制到本地")


    # 在本地复制产品文件夹（含其中文档）
    def product_prdfiles(self, projectname, organization):

        print(projectname +"将template工程下PRD模板复制到本地")
        try:
            cmd=""

            if organization == "template" :
                #cmd="git clone --depth=1 https://github.com/Websoft9/"+projectname+".git data/"+projectname

                cmd="git clone --depth=1 git@github.com:Websoft9test/"+projectname+".git data/"+projectname
            elif organization == "role" :
                cmd="git clone --depth=1 https://github.com/Websoft9dev/"+projectname+".git data/"+projectname

            GithubTools.execute_CommandReturn(cmd)

            GithubTools.execute_CommandReturn("cp -R data/ansible-template/product " + "data/" + projectname)

            # 将模板复制产品文档文件夹所有内容推送到github
            self.github_push(projectname, "add prodoct files")
            self.complete_work(projectname, organization)
        except:
            return 0
        else:
            return 1


    # 创建main分支 dev分支，并删除master分支
    def product_resetbranches(self, projectname, organization):

        print(projectname+"创建main分支 dev分支，并删除master分支")
        try:  
            self.complete_work(projectname, organization)
        except:
            return 0
        else:
            return 1
        

    # github工程备份
    def product_backup(self, projectname, organization):

        print(projectname + "github工程备份")
    
    # 主体构建工作完成后的 后处理，删除列表中该工程
    def complete_work(self, projectname, organization):

        print(projectname+"自动化任务完成后从缓存列表删除该工程")
        
        cmd=''
        if organization == "template" :
            cmd="sed -i '/^$/d;/"+projectname+"/d' data/repositories_cache.txt"
        elif organization == "role" :
            cmd="sed -i '/^$/d;/"+projectname+"/d' data/dev_repositories_cache.txt"

        GithubTools.execute_Command(cmd)

    # 将本地工程提交到github（push to remote）
    def github_push(self, projectname, product):

        print(projectname+"将本地工程提交到github")
        
        GithubTools.execute_CommandReturn("cd "+ "data/" + projectname + ';git add -A;git commit -m "'+product+'";git push')
        # GithubTools.execute_CommandReturn("git add -A")
        # GithubTools.execute_CommandReturn('git commit -m "'+product+'"')
        # GithubTools.execute_Command("git push origin main")



 
