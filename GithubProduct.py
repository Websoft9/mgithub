import os

from backup.GithubTools import GithubTools
import time
from GithubException import CustomException


class GithubProduct():

    def __init__(self, skip_get_repo, skip_broken, force):
        self.skip_get_repo = skip_get_repo
        self.skip_broken = skip_broken
        self.force = force

    # 执行自动化命令
    def product_execute(self, project, organization, product_kind, src_path, des_path, repo_str):
        print("\n============================ [[" + project + "]]: 开始执行自动化构建")

        print("更新本地仓库: " + project)
        FILE_PATH = "data/" + organization + "/" + project
        if os.path.isdir(FILE_PATH):
            cmd = "cd " + FILE_PATH + "; git pull"
            try:
                GithubTools.execute_CommandIgnoreReturn(cmd)
            except CustomException as e:
                raise e
        else:
            cmd = "git clone --depth=1 https://github.com/" + organization + "/" + project + ".git data/" + organization + "/" + project
            try:
                GithubTools.execute_CommandIgnoreReturn(cmd)
            except CustomException as e:
                raise e

        if product_kind == "copy":
            if self.force:
                print("\n执行强制覆盖的copy动作...")
                cmd = "cp -rf data/" + organization + "/" + project + "/" + src_path + " data/" + organization + "/" + project + "/" + des_path
            else:
                print("\n执行不覆盖的copy动作...")
                cmd = "awk \'BEGIN { cmd=\"cp -ri %s %s\"; print \"n\" |cmd; }\'" % ("data/" + organization + "/" + project + "/" + src_path, "data/" + organization + "/" + project + "/" + des_path,)
            # flag = GithubTools.execute_CommandReturn(cmd)
            try:
                GithubTools.execute_CmdCommand(cmd)
            except CustomException as e:
                raise e

            print("\n正在将本地改动push到远程仓库...")
            try:
                self.github_push(organization, project, product_kind)
            except CustomException as e:
                # self.complete_work(0, organization, project, product_kind, repo_str, src_path, des_path)
                raise e

            self.complete_work(1, organization, project, product_kind, repo_str, src_path, des_path)


            # if flag == 1:
            #     # print("\n本工程操作成功")
            #     print("\n正在将本地改动push到远程仓库...")
            #     rcontent = self.github_push(organization, project, product_kind)
            #     if rcontent == 1:
            #         print("push操作成功")
            #         self.complete_work(1, organization, project, product_kind, repo_str, src_path, des_path)
            #         print("============================ [[" + project + "]]: 本项目任务成功\n")
            #     else:
            #         print("push操作失败")
            #         self.complete_work(0, organization, project, product_kind, repo_str, src_path, des_path)
            #         print("============================ [[" + project + "]]: 本项目任务失败\n")
            # else:
            #     self.complete_work(0, organization, project, product_kind, repo_str, src_path, des_path)
            #     print("============================ [[" + project + "]]: 本项目任务失败\n")


    # 将本地工程提交到github（push to remote）
    def github_push(self, organization, project, product):

        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (organization, project, product)
        try:
            GithubTools.execute_CommandIgnoreReturn(cmd)
        except CustomException as e:
            raise e


    # 主体构建工作完成后的处理，删除表中该工程
    def complete_work(self, flag, organization, project, product_kind, repository_str, src_path, des_path):
        if flag == 1:
            print("\n" + project + ": 自动化任务完成,从缓存列表删除该工程,并追加日志")
            cmd = "sed -i '""' '/^$/d;/" + project + "/d' " + repository_str
            GithubTools.execute_CommandIgnoreReturn(cmd)
            self.log_maker(project, product_kind, src_path, des_path, flag)
            print("============================ [[" + project + "]]: 本项目任务成功\n")
        else:
            print("\n" + project + ": 自动化任务未完成,在缓存列表保留此工程,并追加日志")
            self.log_maker(project, product_kind, src_path, des_path, flag)
            print("============================ [[" + project + "]]: 本项目任务失败\n")



    def log_maker(self, project, product, src_path, des_path, flag):
        FILE_PATH = "log/auto_make.log"
        nowtime = time.strftime("%H:%M:%S")
        logline = nowtime
        if (flag == 1):
            logline += " |OK"
        else:
            logline += " |FAILED"
        logline += "| " + project + " execute " + "|" + product.upper() + "|" + " src: |" + src_path + "| des: |" + des_path + "| force: |" + str(self.force) + "|"
        GithubTools.execute_CommandIgnoreReturn("echo '" + logline + "' >>" + FILE_PATH)
        print("log: " + logline)

    def repo_remove(self, organization, project):
        cmd = "rm -rf data/" + organization + "/"+project
        GithubTools.execute_Command(cmd)
