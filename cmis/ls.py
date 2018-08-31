##
# ls
#
# Connect to a CMIS server and list content
##

import util

ls_cmd = util.create_command()

ls_cmd.description = 'List repositories on a server or files and folders in a repository.'

@ls_cmd.option('--root')
def ls_opt_root(context, root=None):
    context['root'] = root

@ls_cmd.main('[path]')
def ls(context, path=None):
    client = util.create_client(context)

    if path is None and 'root' not in context:
        for repo in client.getRepositories():
            print('Repository: ' + str(repo['repositoryName']) + ' (' + str(repo['repositoryId']) + ')')

        return

    repo = client.defaultRepository

    if path == '/' or 'root' in context:
        root = repo.getRootFolder()

        for child in root.getChildren().getResults():
            print(child.getName())
    else:
        path = util.sanitize_path(path)
        obj = repo.getObjectByPath(path)

        for child in obj.getChildren().getResults():
            print(child.getName())
