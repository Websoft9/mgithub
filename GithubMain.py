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
    
    var url
    var organization
    var help
    var version
    var logs
    var skip-get-repositories
    var skip-broken
    var force
    
    var command
    var commandstring
    
    
    if (skip-get-repositories)
    {
        if data/websoft9_repositories.txt=null
        print("没有项目可以执行，--skip-get-repositories 参数不能使用")
        exit; 
    }
    
    else
    
    {
        if data/websoft9_repositories.txt !=null{
            print("有历史遗留清单没有完成，忽略清单？")
            if 忽略
             {
                repocache() 
             }
            else
             {
                 exit
             }
        }else
        
        {
            repocache() 
        }

    }
    
    
    for (repository in organazition_repositories.txt)
        {
            returnvalue=GithubCommand.command;
            if {force}{
                if returnvalue==ok
                else 
                 continue;  
            }else{
                if returnvalue==failed
                  break;

            }
            
        }