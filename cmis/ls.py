##
# ls
#
# Connect to a CMIS server and list content
##

import util

ls = util.create_command()

@ls.main('[scope [path]]')
def ls_main(context, scope=None, path=None):
    client = util.create_client(context)

    if scope is None:
        for repo in client.getRepositories():
            print('Repository: ' + str(repo['repositoryName']) + ' (' + str(repo['repositoryId']) + ')')

        return

    repo = client.getRepository(scope)
    root = repo.getRootFolder()

    # Something is broken with the atompub binding, this corrects
    # a bad variable in the CmisObject
    repo._cmisClient = client
    root._cmisClient = client

    if path is None:
        for child in root.getChildren().getResults():
            print(child.getName())
    else:
        obj = repo.getObjectByPath('/' + path)

        for child in obj.getChildren().getResults():
            print(child.getName())
