class GithubCommand:

    def configure(self, ctx):
        print("[[configure]] function is running")
        GithubCommand.debug(ctx)

    def repocache(self, ctx):
        print("[[repocache]] function is running")
        GithubCommand.debug(ctx)

    def backup(self, ctx, path):
        print("[[backup]] function is running")
        print("path is: %s" % path)
        GithubCommand.debug(ctx)

    def copy(self, ctx, src_path, des_path):
        print("[[backup]] function is running")
        print('src_path: %s' % src_path)
        print('des_path: %s' % des_path)
        GithubCommand.debug(ctx)

    def move(self, ctx, src_path, des_path):
        print("[[move]] function is running")
        print('src_path: %s' % src_path)
        print('des_path: %s' % des_path)
        GithubCommand.debug(ctx)

    def delete(self, ctx, path):
        print("[[delete]] function is running")
        print("path is: %s" % path)
        GithubCommand.debug(ctx)

    def rename(self, ctx, path, new_name):
        print("[[rename]] function is running")
        print("path is: %s" % path)
        print("new_name is: %s" % new_name)
        GithubCommand.debug(ctx)

    def replace(self, ctx, file_path, old_content, new_content):
        print("[[replace]] function is running")
        print("file_path is: %s" % file_path)
        print("old_content is: %s" % old_content)
        print("new_content is: %s" % new_content)
        if (new_content == None):
            print("Since not new_content is provided, old_content will be deleted from file_path")
        GithubCommand.debug(ctx)

    def lineinsert(self, ctx, file_path, line, content):
        print("[[lineinsert]] function is running")
        print("file_path is: %s" % file_path)
        print("line is: %s" % (line, ))
        print("content is: %s" % content)
        for li in line:
            print("insert %s into line %s of %s" % (content, li, file_path))
        GithubCommand.debug(ctx)

    def format(self, ctx, template, variable):
        print("[[format]] function is running")
        print("template is: %s" % template)
        print("variable is: %s" % variable)
        GithubCommand.debug(ctx)

    def githubcli(self, ctx, clistring):
        print("[[githubcli]] function is running")
        print("clistring is: %s" % clistring)
        print("printing log ....")
        GithubCommand.debug(ctx)

    @staticmethod
    def debug(ctx):
        print("########## debug flag check ##########")
        print("url: %s" % ctx.obj['url'])
        print("skip-get-repositories: %s" % ctx.obj['skip_get_repositories'])
        print("skip-broken: %s" % ctx.obj['skip_broken'])
        print("force: %s" % ctx.obj['force'])

