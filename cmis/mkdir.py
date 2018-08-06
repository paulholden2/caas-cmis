##
# ls
#
# Connect to a CMIS server and create a folder
##

import util

mkdir = util.create_command()

@mkdir.main('name')
def mkdir_main(context, name):
    client = util.create_client(context)
    repo = client.defaultRepository
    root = repo.getRootFolder()
    folder = root.createFolder(name)

    print(folder)
