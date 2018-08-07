##
# ls
#
# Connect to a CMIS server and create a folder
##

import string
import util

mkdir = util.create_command()

@mkdir.main('name')
def mkdir_main(context, name):
    client = util.create_client(context)
    repo = client.defaultRepository
    root = repo.getRootFolder()

    folders = string.split(name, '/')

    if len(folders) == 1:
        root.createFolder(name)
    else:
        parent = root

        for sub in folders:
            new_id = parent.createFolder(sub)
            parent = repo.getFolder(new_id)
