import os
from backup.GithubTools import GithubTools
from GithubProduct import GithubProduct


class GithubFlow():

    # 根据组织确定需要作业的范围对象,对所有对象循环处理要做的自动化处理
    def auto_make(self, organization, product_kind, src_path, des_path):

        print("==============start automake task ============== ")

        repo_str = "data/" + organization + "_repositories.txt"

        # 判断缓存文件是否存在
        if os.path.isdir(repo_str):
            pass
        else:
            pass
            # 缓存文件不存在，创建空的缓存文件
            GithubTools.execute_CommandReturn('touch ' + repo_str)

        self.automake_new(organization, product_kind, src_path, des_path, repo_str)

    def automake_new(self, organization, product_kind, src_path, des_path, repo_str):
        self.create_repository(organization, repo_str)
        project_list = open(repo_str).read().splitlines()

        for proj in project_list:
            FILE_PATH = "data/organization/" + proj
            if os.path.isdir(FILE_PATH):
                pass
            else:
                cmd="git clone --depth=1 https://github.com/"  + organization + "/" + proj + ".git data/" + organization + "/" + proj
                GithubTools.execute_CommandReturn(cmd)

        product = GithubProduct()
        for proj in project_list:
            product.product_execute(proj, organization, product_kind, src_path, des_path, repo_str)

    # 根据organization生成最新的repository文件列表
    def create_repository(self, organization, repository_str):
        print('\n开始更新%s Github仓库列表' % organization)
        GithubTools.execute_CommandWriteFile(
            'curl -s  https://api.github.com/orgs/mgithubTestOrg/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
            repository_str)

