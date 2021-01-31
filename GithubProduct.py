import os

from backup.GithubTools import GithubTools
import time


class GithubProduct():

    # 执行自动化命令
    def product_execute(self, project, organization, product_kind, src_path, des_path, repo_str):
        print("\n" + project + ": 开始执行自动化构建")

        FILE_PATH = "data/" + organization + "/" + project
        if os.path.isdir(FILE_PATH):
            cmd = "cd " + FILE_PATH + "; git pull"
            GithubTools.execute_CommandReturn(cmd)
        else:
            cmd = "git clone --depth=1 https://github.com/" + organization + "/" + project + ".git data/" + organization + "/" + project
            GithubTools.execute_CommandReturn(cmd)

        if product_kind == "copy":
            cmd = "echo y | cp -r data/" + organization + "/" + project + "/" + src_path + " data/" + organization + "/" + project + "/" + des_path
            flag = GithubTools.execute_CommandReturn(cmd)
            if flag == 1:
                print("本工程操作成功...")
                rcontent = self.github_push(organization, project, product_kind)
                if rcontent == 1:
                    self.complete_work(1, organization, project, product_kind, repo_str, src_path, des_path)
                else:
                    self.complete_work(0, organization, project, product_kind, repo_str, src_path, des_path)
            else:
                print("本工程操作失败...")
                self.complete_work(0, organization, project, product_kind, repo_str, src_path, des_path)


    # 将本地工程提交到github（push to remote）
    def github_push(self, organization, project, product):

        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (organization, project, product)
        content = GithubTools.execute_CommandReturn(cmd)

        return content

    # 主体构建工作完成后的处理，删除表中该工程
    def complete_work(self, flag, organization, project, product_kind, repository_str, src_path, des_path):
        if flag == 1:
            print(project + ": 自动化任务完成,从缓存列表删除该工程,并追加日志")
            cmd = "sed -i '""' '/^$/d;/" + project + "/d' " + repository_str
            GithubTools.execute_Command(cmd)
            self.log_maker(project, product_kind, src_path, des_path, flag)
        else:
            print(project + ": 自动化任务未完成,在缓存列表保留此工程,并追加日志")
            self.log_maker(project, product_kind, src_path, des_path, flag)



    def log_maker(self, project, product, src_path, des_path, flag):
        FILE_PATH = "log/auto_make.log"
        nowtime = time.strftime("%H:%M:%S")
        logline = nowtime
        if (flag == 1):
            logline += " |OK"
        else:
            logline += "| FAILED"
        logline += "| " + project + " execute " + "|" + product.upper() + "|" + " src: |" + src_path + "| des: |" + des_path + "|"
        GithubTools.execute_Command("echo '" + logline + "' >>" + FILE_PATH)

    def repo_remove(self, organization, project):
        cmd = "rm -rf data/" + organization + "/"+project
        GithubTools.execute_Command(cmd)
