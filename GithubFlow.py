import os
from backup.GithubTools import GithubTools

class GithubFlow():

    # 根据组织确定需要作业的范围对象,对所有对象循环处理要做的自动化处理
    def auto_make(self, organization, product_kind, src_path, des_path, cmd):

        print("==============start automake task ============== ")

        repository_str = "data/" + organization + "_repositories.txt"

        # 判断缓存文件是否存在
        if os.path.isdir(repository_str):
            pass
        else:
            pass
        # 缓存文件不存在，创建空的缓存文件
            GithubTools.execute_CommandReturn('touch ' + repository_str)

        self.automake_new(organization, product_kind, src_path, des_path, cmd, repository_str)

    def automake_new(self, organization, product_kind, src_path, des_path, cmd, repository_str):

        print('自动化任务开始，将从github下载最新的项目列表后开始构建')

        src_repo = organization + "/" + src_path.split("/")[0]
        des_repo = organization + "/" + des_path.split("/")[0]

        print("repository_str: " + repository_str)
        print("src_repo: " + src_repo)
        print("des_repo: " + des_repo)

        src_cmd = "git clone --depth=1 https://github.com/" + src_repo +".git data/" + src_repo
        des_cmd = "git clone --depth=1 https://github.com/" + des_repo + ".git data/" + des_repo
        print(src_cmd)
        GithubTools.execute_CommandReturn(src_cmd)
        GithubTools.execute_CommandReturn(des_cmd)

        self.create_repository(organization, repository_str)

    # 根据organization生成最新的repository文件列表
    def create_repository(self, organization, repository_str):
        print(('\n开始更新%s Github仓库列表\n') % organization)
        GithubTools.execute_CommandWriteFile(
            'curl -s  https://api.github.com/orgs/mgithubTestOrg/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
            repository_str)