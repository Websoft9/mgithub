class GithubCommand:

    def repocache(self, ctx):
        print("repocache function is running")
        print("########## flag check ##########")
        print("skip-get-repositories: %s" % ctx.obj['skip_get_repositories'])
        print("skip-broken: %s" % ctx.obj['skip_broken'])
        print("force: %s" % ctx.obj['force'])


    def copy(self, src_path, des_path):
        print('GithubCommand.copy is running')
        print('src_path: %s' % src_path)
        print('des_path: %s' % des_path)