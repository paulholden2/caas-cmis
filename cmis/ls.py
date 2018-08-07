##
# ls
#
# Connect to a CMIS server and list content
##

import util

ls_cmd = util.create_command()

@ls_cmd.main('[path]')
def ls(context, path=None):
    client = util.create_client(context)

    if path is None:
        for repo in client.getRepositories():
            print('Repository: ' + str(repo['repositoryName']) + ' (' + str(repo['repositoryId']) + ')')

        return

    repo = client.defaultRepository
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
