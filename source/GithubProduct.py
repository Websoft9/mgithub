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

    # 执行自动化内容
    def product_excute(self, projectname, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str):

        print(projectname + "开始执行自动化构建") 

        # copy：复制模板文件（或文件夹）到github项目 delete: 删除github项目某个路径下所有文件或者目录 modify:对github的文件进行cmd操作，例如字符串替换等
        # format：根据模板文件的format重新生成到github项目 branch:对github的项目进行分支操作，如建新分支dev，main，删除master分支，并设置main为default
        # backup:备份项目 other:目前没有明确的需求，待追加
        if productkind == "copy" :

            # 如果工程已经存在，就更新；否则从github上克隆最新的代码
            cmd="cd template/" + projectname + ";git pull"

            FILE_PATH="template/" + projectname
            if os.path.isdir(FILE_PATH): 
                pass
            else:
                # 当前任务工程不存在 github克隆最新的
                if organization == "template" :
                    cmd="git clone --depth=1 git@github.com:Websoft9/"+projectname+".git data/"+projectname
                elif organization == "role" :
                    cmd="git clone --depth=1 git@github.com:Websoft9dev/"+projectname+".git data/"+projectname
            GithubTools.execute_CommandReturn(cmd)

            GithubTools.execute_CommandReturn("echo y |cp -Rr data/ansible-template/"+sourcepath + " template/" + projectname+"/"+despath)

            # 将模板复制产品文档文件夹所有内容推送到github
            rcontent=self.github_push(projectname, "add prodoct files")
            if rcontent == 0 :
                self.complete_work(projectname, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str)
            else:
                print(projectname +"执行失败")

        elif productkind == "delete" :

        elif productkind == "modify" :

        elif productkind == "format" :

        elif productkind == "branch" :

        elif productkind == "backup" :

    
    # 主体构建工作完成后的 后处理，删除列表中该工程
    def complete_work(self, projectname, organization, productkind, sourcepath, despath, cmd, repository_cache_str, repository_str):

        print(projectname+"自动化任务完成后从缓存列表删除该工程,并追加日志")  
        cmd=''
        if organization == "template" :
            cmd="sed -i '/^$/d;/"+projectname+"/d' data/repositories_cache.txt"
        elif organization == "role" :
            cmd="sed -i '/^$/d;/"+projectname+"/d' data/dev_repositories_cache.txt"
        GithubTools.execute_Command(cmd)

        FILE_PATH="log/auto_make.log"
        if os.path.isfile(FILE_PATH):
            pass
        else:
            GithubTools.execute_Command("touch log/auto_make.log")

        ## 追加日志
        nowtime=time.strftime("%H:%M:%S")
        logline=nowtime+":"projectname+"excute "+productkind+" sourcepath("+sourcepath+") despath("+despath+") cmd("+cmd+")"
        GithubTools.execute_Command("echo '"+logline+ "' >>"+FILE_PATH)


    # 将本地工程提交到github（push to remote）
    def github_push(self, projectname, product):

        print(projectname+"将本地工程提交到github") 
        #content=GithubTools.execute_CommandReturn("cd "+ "data/" + projectname + ';git add -A;git commit -m "'+product+'";git push')
        content=0
        return content
        # GithubTools.execute_CommandReturn("git add -A")
        # GithubTools.execute_CommandReturn('git commit -m "'+product+'"')
        # GithubTools.execute_Command("git push origin main")



 
