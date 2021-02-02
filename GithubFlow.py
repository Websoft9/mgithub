import os
from backup.GithubTools import GithubTools
from GithubProduct import GithubProduct
from GithubException import CustomException


class GithubFlow():

    def __init__(self, skip_get_repo, skip_broken, force):
        self.skip_get_repo = skip_get_repo
        self.skip_broken = skip_broken
        self.force = force

    # 根据组织确定需要作业的范围对象,对所有对象循环处理要做的自动化处理
    def auto_make(self, organization, product_kind, src_path, des_path):

        print("============================ Automake task starting... ============================ \n")

        repo_str = "data/" + organization + "_repositories.txt"

        # 判断缓存文件是否存在
        if os.path.isfile(repo_str):
            project_list = open(repo_str).read().splitlines()
            if (len(project_list) == 0):
                self.automake_new(organization, product_kind, src_path, des_path, repo_str)
            else:
                print("清单里有未完成的任务列表, 请确认对列表内容")
                print("未完成清单内容如下：")
                GithubTools.execute_CmdCommand("cat " + repo_str)
                print("最新10条任务日志如下：")
                GithubTools.execute_CmdCommand("tail -n 10 log/auto_make.log")

                continue_id = self.continue_select()

                if continue_id == "0":
                    self.automake_cache(repo_str)
                    return
                else:
                    print("已经清空所有未完成任务，请重新输入命令再次执行")
                    GithubTools.execute_Command('echo -n "" > data/' + organization + "_repositories.txt")
                    return
        else:
            # 缓存文件不存在，创建空的缓存文件
            GithubTools.execute_CommandReturn('touch ' + repo_str)
            self.automake_new(organization, product_kind, src_path, des_path, repo_str)

    def automake_new(self, organization, product_kind, src_path, des_path, repo_str):

        product = GithubProduct(self.skip_get_repo, self.skip_broken, self.force)

        # 获取组织下的项目列表并写入相应的xxxx_repositories.txt
        self.create_repository(organization, repo_str)
        project_list = open(repo_str).read().splitlines()

        # 如果项目列表为空，可能由于网络原因无法获取
        try:
            if len(project_list) == 0:
                raise CustomException("您的仓库列表为空,请检查您的网络连接或组织名称")
        except CustomException as e:
            print(e.msg)
            print("============================ [[Empty]]: 任务列表为空\n")
            return

        if self.skip_get_repo:
            # mgithub --skip-get-repositories
            print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
        else:
            print("\n正在将本组织下的仓库clone到本地...")
            for proj in project_list:
                FILE_PATH = "data/" + organization + "/" + proj
                if os.path.isdir(FILE_PATH):
                    print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                else:
                    print("git clone from " + proj + "....")
                    cmd = "git clone --depth=1 https://github.com/" + organization + "/" + proj + ".git data/" + organization + "/" + proj
                    try:
                        GithubTools.execute_CommandIgnoreReturn(cmd)
                    except CustomException as e:
                        # 仓库clone未成功，结束本次任务
                        print(e.msg)
                        product.complete_work(0, organization, proj, product_kind, repo_str, src_path, des_path)
                        return

        # 对项目列表中的项目进行循环执行操作
        for proj in project_list:
            try:
                product.product_execute(proj, organization, product_kind, src_path, des_path, repo_str)
            except CustomException as e:
                # 操作抛出异常
                print(e.msg)
                product.complete_work(0, organization, proj, product_kind, repo_str, src_path, des_path)
                print("============================ [[" + proj + "]]: 项目正在回滚")
                # 回滚项目
                cmd = "cd data/" + organization + "/" + proj + ";git fetch --all;git reset --hard origin/master;git clean -f -d;"
                try:
                    GithubTools.execute_CommandIgnoreReturn(cmd)
                except CustomException as e:
                    print(e.msg)
                    print(proj + ": 项目回滚失败, 请检查您的网络连接状况和组织名称")
                else:
                    print(proj + ": 项目已回滚")
                if self.skip_broken:
                    continue
                else:
                    return

    def automake_cache(self, repo_str):
        product_kind = None
        organization = None
        src_path = None
        des_path = None
        product = None

        project_list = open(repo_str).read().splitlines()
        log_list = open("log/auto_make.log").read().splitlines()
        log_index = len(log_list) - 1
        while (log_index >= 0):
            # print(log_list[log_index].split("|")[1])
            # print(project_list[0])
            if (log_list[log_index].split("|")[5] == project_list[0] and
                    log_list[log_index].split("|")[1] == "FAILED"):
                # print(log_list[log_index])

                product_kind = log_list[log_index].split("|")[7].lower()
                organization = log_list[log_index].split("|")[3]
                src_path = log_list[log_index].split("|")[9]
                des_path = log_list[log_index].split("|")[11]
                product = GithubProduct(log_list[log_index].split("|")[15],
                                        log_list[log_index].split("|")[17],
                                        log_list[log_index].split("|")[13])

                if log_list[log_index].split("|")[15] == "True":
                    # mgithub --skip-get-repositories
                    print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
                else:
                    print("\n正在将本组织下的仓库clone到本地...")
                    for proj in project_list:
                        FILE_PATH = "data/" + organization + "/" + proj
                        if os.path.isdir(FILE_PATH):
                            print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                        else:
                            print("git clone from " + proj + "....")
                            cmd = "git clone --depth=1 https://github.com/" + organization + "/" + proj + ".git data/" + organization + "/" + proj
                            try:
                                GithubTools.execute_CommandIgnoreReturn(cmd)
                            except CustomException as e:
                                # 仓库clone未成功，结束本次任务
                                print(e.msg)
                                product.complete_work(0, organization, proj, product_kind, repo_str, src_path, des_path)
                                return
                for proj in project_list:
                    try:
                        product.product_execute(proj, organization, product_kind, src_path, des_path, repo_str)
                    except CustomException as e:
                        # 操作抛出异常
                        print(e.msg)
                        product.complete_work(0, organization, proj, product_kind, repo_str, src_path, des_path)
                        print("============================ [[" + proj + "]]: 项目正在回滚")
                        # 回滚项目
                        cmd = "git fetch --all;git reset --hard origin/master;git clean -f -d"
                        try:
                            GithubTools.execute_CommandIgnoreReturn(cmd)
                        except CustomException as e:
                            print(e.msg)
                            print(proj + ": 项目回滚失败, 请检查您的网络连接状况和组织名称")
                        print(proj + ": 项目已回滚")
                        if log_list[log_index].split("|")[17] == "True":
                            continue
                        else:
                            return
                break
            log_index -= 1

    # 根据organization生成最新的repository文件列表
    def create_repository(self, organization, repository_str):
        print('开始更新%s Github仓库列表...' % organization)
        GithubTools.execute_CommandWriteFile(
            'curl -s  https://api.github.com/orgs/mgithubTestOrg/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
            repository_str)

    # 选择继续操作
    # 格式：选择是否在上次任务上继续：  \n\t 0. 继续 \n\t 1. 终止退出  \n\n\t选择:
    def continue_select(self):
        input_str = "\n\t缓存任务尚未完成，是否继续上次任务：  \n\n\t "
        i = 0

        for x in ['继续进行当前执行的自动化操作', '终止退出']:
            input_str = input_str + str(i) + "." + x + " \n\t "
            i = i + 1
        input_str = input_str + "\n\t选择: "
        continue_id = input(input_str)
        while continue_id not in ['0', '1']:
            print('\n\t输入错误，请重新选择')
            continue_id = input(input_str)
        return continue_id
