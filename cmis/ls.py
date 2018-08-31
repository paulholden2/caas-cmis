##
# ls
#
# Connect to a CMIS server and list content
##

import util

ls_cmd = util.create_command()

ls_cmd.description = 'List repositories on a server or files and folders in a repository.'

@ls_cmd.option('--root')
def ls_opt_r(context, root=None):
    context['root'] = root

@ls_cmd.main('[path]')
def ls(context, path=None):
    client = util.create_client(context)

    if path is None and context['root'] is None:
        for repo in client.getRepositories():
            print('Repository: ' + str(repo['repositoryName']) + ' (' + str(repo['repositoryId']) + ')')

        return

    path = util.sanitize_path(path)
    repo = client.defaultRepository

    if path == '/' or context['root'] is not None:
        root = repo.getRootFolder()

        for child in root.getChildren().getResults():
            print(child.getName())
    else:
        obj = repo.getObjectByPath(path)

        for child in obj.getChildren().getResults():
            print(child.getName())
