import os
from backup.GithubTools import GithubTools
from GithubProduct import GithubProduct


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
        if os.path.isdir(repo_str):
            pass
        else:
            pass
            # 缓存文件不存在，创建空的缓存文件
            GithubTools.execute_CommandReturn('touch ' + repo_str)

        self.automake_new(organization, product_kind, src_path, des_path, repo_str)

    def automake_new(self, organization, product_kind, src_path, des_path, repo_str):
        self.create_repository(organization, repo_str)
        # GithubTools.execute_Command("echo 'projDDD' >> data/mgithubTestOrg_repositories.txt")
        project_list = open(repo_str).read().splitlines()

        if self.skip_get_repo:
            print("\n已跳过clone仓库步骤, 本地已有的仓库将会在执行过程中更新")
        else:
            print("\n正在将本组织下的仓库clone到本地...")
            for proj in project_list:
                FILE_PATH = "data/" + organization + "/"+ proj
                if os.path.isdir(FILE_PATH):
                    print(FILE_PATH + "已存在, 可以使用option: --skip-get-repositories 跳过本步骤")
                else:
                    cmd="git clone --depth=1 https://github.com/"  + organization + "/" + proj + ".git data/" + organization + "/" + proj
                    GithubTools.execute_CommandReturn(cmd)

        product = GithubProduct(self.skip_get_repo, self.skip_broken, self.force)
        for proj in project_list:
            product.product_execute(proj, organization, product_kind, src_path, des_path, repo_str)

    # 根据organization生成最新的repository文件列表
    def create_repository(self, organization, repository_str):
        print('开始更新%s Github仓库列表...' % organization)
        GithubTools.execute_CommandWriteFile(
            'curl -s  https://api.github.com/orgs/mgithubTestOrg/repos?per_page=999999 | grep \'"name"\'|awk -F \'"\' \'{print $4}\'',
            repository_str)

