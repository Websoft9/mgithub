from backup.GithubTools import GithubTools
import time


class GithubProduct():

    # 执行自动化命令
    def product_execute(self, project, organization, product_kind, src_path, des_path, repo_str, project_list):

        print("\n" + project + ": 开始执行自动化构建")

        if product_kind == "copy":
            self.log_maker(project, product_kind, src_path, des_path, True)
            # 移动到 data/organization/ 文件夹下
            cmd = "cd data/" + organization
            GithubTools.execute_CommandReturn(cmd)

            # 执行 copy 命令
            cmd = "echo y | cp -r data/" + organization + "/" + src_path + " data/" + organization + "/" + des_path
            GithubTools.execute_CommandReturn(cmd)

            # 将 copy 操作的目标仓库push到远程仓库
            rcontent = self.github_push(organization, des_path.split("/")[0], product_kind)

            if (rcontent == 1):
                print("Success!")
                self.complete_work(project, product_kind, repo_str, src_path, des_path, project_list)
            else:
                print("Failed!")

    # 将本地工程提交到github（push to remote）
    def github_push(self, organization, project, product):

        print(project + ": 将本地工程提交到github")
        cmd = 'cd data/%s/%s;\ngit add -A;\ngit commit -m "%s";\ngit push' % (organization, project, product)
        content = GithubTools.execute_CommandReturn(cmd)

        return content

    # 主体构建工作完成后的处理，删除表中该工程
    def complete_work(self, project, product_kind, repository_str, src_path, des_path, project_list):

        print("自动化任务完成后从缓存列表删除该工程，并追加日志")

        if (product_kind == "copy"):
            # 因为copy只涉及到两个仓库，完成就可以删除所有repo list
            # 从project_list中循环删除project
            for proj in project_list:
                cmd = "sed -i '""' '/^$/d;/" + proj + "/d' " + repository_str
                GithubTools.execute_Command(cmd)
            self.log_maker(project, product_kind, src_path, des_path, False)
        else:
            pass

    def log_maker(self, project, product, src_path, des_path, start):
        FILE_PATH = "log/auto_make.log"
        nowtime = time.strftime("%H:%M:%S")
        if (start == True):
            logline = "[[Start]]  "
        else:
            logline = "[[Finish]] "
        logline += nowtime + ": " + project + " execute " + product.upper() + " src(" + src_path + ") des(" + des_path + ")";
        GithubTools.execute_Command("echo '" + logline + "' >>" + FILE_PATH)
