import os
import signal
import sys

from backup.GithubTools import GithubTools
from GithubProduct import GithubProduct
from GithubException import CustomException
from GithubSystem import GithubSystem


class GithubFlow():

    def __init__(self, url, skip_get_repo, skip_broken, force, product_kind, src_path, des_path, clistring):
        self.url = url
        self.skip_get_repo = skip_get_repo
        self.skip_broken = skip_broken
        self.force = force
        self.product_kind = product_kind
        self.src_path = src_path
        self.des_path = des_path
        self.organization = url.split("/")[len(url.split("/")) - 1]
        self.repo_str = None
        self.current_proj = None
        self.clistring = clistring

    # 添加对Ctrl-C的监听器
    def signal_handler(self, signal, frame):
        if os.path.isfile(self.repo_str):
            product = GithubProduct(self.url, self.skip_get_repo, self.skip_broken, self.force, self.product_kind,
                                    self.src_path,
                                    self.des_path, self.repo_str, self.clistring)
            if self.current_proj is None:
                # 如果当前还没有开始执行项目，则任务项目列表中的第一个项目执行失败
                product.complete_work(2, open(self.repo_str).read().splitlines()[0])
            else:
                # 如果已经开始执行项目，则当前项目执行失败
                product.complete_work(2, self.current_proj)
                self.rollback_proj(self.current_proj)
        print("用户主动中断任务")
        sys.exit(0)

    # 对本组织下的仓库进行循环处理任务
    def auto_make(self):

        # 将监听器注册到本function
        signal.signal(signal.SIGINT, self.signal_handler)

        print("============================ Automake task starting... ============================ \n")

        # 判断项目列表是否存在
        self.repo_str = "data/" + self.organization + "_repositories.txt"
        if os.path.isfile(self.repo_str):
            # 项目列表存在，判断内容是否为空
            project_list = open(self.repo_str).read().splitlines()
            if (len(project_list) == 0):
                # 内容为空，直接执行正常操作
                self.automake_new()
            else:
                # 内容不为空，让用户决定是否继续上次的任务
                print("清单里有未完成的任务列表, 请确认列表内容")
                print("未完成清单内容如下：")
                # GithubTools.execute_CmdCommand("cat " + self.repo_str)
                GithubSystem.execute_CmdCommand("cat " + self.repo_str)
                print("最新10条任务日志如下：")
                # GithubTools.execute_CmdCommand("tail -n 10 log/auto_make.log")
                # GithubSystem.execute_CmdCommand("tail -n 10 log/auto_make.log")
                GithubSystem().show_logs(10)
                # 用户输入
                continue_id = self.continue_select()
                # 根据不同的用户输入决定操作
                if continue_id == "0":
                    # 继续上次中断的任务
                    self.automake_cache()
                    return
                else:
                    # 放弃上次的任务并删除项目列表
                    print("已经清空所有未完成任务，请重新输入命令再次执行")
                    # GithubTools.execute_CmdCommand(": > data/" + self.organization + "_repositories.txt")
                    GithubSystem.execute_CmdCommand(": > data/" + self.organization + "_repositories.txt")
                    return
        else:
            # 缓存文件不存在，创建空的缓存文件
            # GithubTools.execute_CommandReturn('touch ' + self.repo_str)
            GithubSystem.execute_CommandReturn('touch ' + self.repo_str)
            # 执行正常操作
            self.automake_new()

    # 无任务中断，正常操作
    def automake_new(self):

        # 创建一个新的GitHubProduct对象并传入全局参数与command参数
        product = GithubProduct(self.url, self.skip_get_repo, self.skip_broken, self.force, self.product_kind,
                                self.src_path,
                                self.des_path, self.repo_str, self.clistring)

        # 获取组织下的所有项目并写入项目列表
        self.create_repository(self.organization, self.repo_str)
        project_list = open(self.repo_str).read().splitlines()

        # 如果项目列表为空，可能由于网络原因无法获取或者组织名错误
        try:
            if len(project_list) == 0:
                raise CustomException("您的仓库列表为空,请检查您的网络连接或组织名称")
        except CustomException as e:
            print(e.msg)
            print("============================ [[Empty]]: 任务列表为空\n")
            return

        # 根据项目列表，将每个项目的远程仓库clone到本地
        try:
            self.clone_repo_list(project_list, product)
        except CustomException as e:
            print(e.msg)
            if str(self.skip_broken) != "True":
                return

        # 根据项目列表，对每个项目进行循环command操作
        self.loop_proj_work(project_list, product)

    # 执行上次中断的任务
    def automake_cache(self):

        # 获得上次遗留的项目列表
        project_list = open(self.repo_str).read().splitlines()

        # 获得log日志列表
        log_list = open("log/auto_make.log").read().splitlines()

        # 根据遗留项目列表的第一项，寻找log日志列表中相对应的 FAILED 或 ABORT 项目（自下而上）
        log_index = len(log_list) - 1
        while (log_index >= 0):

            if (log_list[log_index].split("|")[5] == project_list[0] and
                    (log_list[log_index].split("|")[1] == "FAILED" or
                     log_list[log_index].split("|")[1] == "ABORT")):
                # 根据日志记录的option内容，对本次任务的option进行覆盖
                self.product_kind = log_list[log_index].split("|")[7].lower()
                self.organization = log_list[log_index].split("|")[3]
                self.src_path = log_list[log_index].split("|")[9]
                self.des_path = log_list[log_index].split("|")[11]
                self.url = log_list[log_index].split("|")[19]
                self.skip_get_repo = log_list[log_index].split("|")[15]
                self.skip_broken = log_list[log_index].split("|")[17]
                self.force = log_list[log_index].split("|")[13]

                # 生成一个新的GitHubProduct对象
                product = GithubProduct(self.url, self.skip_get_repo, self.skip_broken, self.force, self.product_kind,
                                        self.src_path,
                                        self.des_path, self.repo_str, self.clistring)

                # 根据项目列表，将每个项目的远程仓库clone到本地
                try:
                    self.clone_repo_list(project_list, product)
                except CustomException as e:
                    print(e.msg)
                    if str(self.skip_broken) != "True":
                        return
                # self.clone_repo_list(project_list, product)

                # 根据项目列表，对每个项目进行循环command操作
                self.loop_proj_work(project_list, product)

                # 中断循环
                break

            # 从下而上检索log日志条例
            log_index -= 1

    # 根据组织寻找组织下所有的项目
    def create_repository(self, organization, repository_str):
        print('开始更新%s Github仓库列表...' % organization)
        # GithubTools.execute_CommandWriteFile(
        #     'curl -s  https://api.github.com/orgs/mgithubTestOrg/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
        #     repository_str)
        if GithubSystem().get_prop("repogrep")is "":
            GithubSystem.execute_CommandWriteFile_uncover(
                'curl -s  https://api.github.com/users/' + organization + '/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
                repository_str
            )
        else:
            repogrep = GithubSystem().get_prop("repogrep").split(",")
            for repo in repogrep:
                # if org:
                #     GithubSystem.execute_CommandWriteFile(
                #         'curl -s  https://api.github.com/orgs/' + organization + '/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
                #         repository_str
                #     )
                # else:
                #     GithubSystem.execute_CommandWriteFile(
                #         'curl -s  https://api.github.com/users/' + organization + '/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
                #         repository_str
                #     )

                # print("user")
                GithubSystem.execute_CommandWriteFile_uncover(
                    'curl -s  https://api.github.com/users/' + organization + '/repos?per_page=999999 | grep \'"' + repo + '.*"\'|awk -F \'"\' \'{print $4}\'',
                    repository_str
                )

    # 根据项目列表，将每个项目的远程仓库clone到本地
    def clone_repo_list(self, project_list, product):

        # 如果用户执行时使用 mgithub --skip-get-repositories
        if self.skip_get_repo:
            print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
        else:
            print("\n正在将本组织下的仓库clone到本地...")
            for proj in project_list:
                FILE_PATH = "data/" + self.organization + "/" + proj
                # 判断仓库是否已经保存在本地
                if os.path.isdir(FILE_PATH):
                    # 存在
                    print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                else:
                    # 不存在，从远程仓库clone
                    print("git clone from " + proj + "....")
                    cmd = "git clone --depth=1 " + self.url + "/" + proj + ".git data/" + self.organization + "/" + proj
                    try:
                        # GithubTools.execute_CommandIgnoreReturn(cmd)
                        GithubSystem.execute_GitCommand(cmd)
                    except CustomException as e:
                        # 仓库clone未成功，结束本次任务
                        # print(e.msg)
                        if str(self.skip_broken) == "True":
                            print(proj + ": 本仓库clone失败")
                        else:
                            print("仓库clone未成功，结束本次任务")
                            raise e
                        # product.complete_work(0, proj)

    # 根据项目列表，对每个项目进行循环command操作
    def loop_proj_work(self, project_list, product):
        for proj in project_list:
            # 记录本次正在执行command的项目，方便与监听器记录
            self.current_proj = proj
            # 执行相应的command
            try:
                product.product_execute(proj)
            except CustomException as e:
                # 捕捉执行过程中出现异常
                print(e.msg)
                # 已 FAILED 记录本次任务
                product.complete_work(0, proj)
                # 对项目进行回滚
                self.rollback_proj(proj)
                # 如果用户使用 mgithub --skip-broken
                if str(self.skip_broken) == "True":
                    continue
                else:
                    break

    def rollback_proj(self, project):
        # 对项目进行回滚
        print("============================ [[" + project + "]]: 项目正在回滚")
        cmd = "cd data/" + self.organization + "/" + project + ";git fetch --all;git reset --hard origin/master;git clean -f -d;"
        try:
            # GithubTools.execute_CommandIgnoreReturn(cmd)
            GithubSystem.execute_GitCommand(cmd)
        except CustomException as e:
            # 项目回滚中出现异常，回滚失败
            print(e.msg)
            print(project + ": 项目回滚失败, 请检查您的网络连接状况和组织名称")
        else:
            print(project + ": 项目已回滚")

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
