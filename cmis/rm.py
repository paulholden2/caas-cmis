##
# rm
#
# Remove files and folders
##

import util

rm_cmd = util.create_command()

rm_cmd.description = 'Delete a folder or document object from a repository.'

def do_rm(context, obj):
    try:
        for c in obj.getChildren():
            do_rm(context, c)
    except:
        pass

    obj.delete()


@rm_cmd.main('path')
def rm(context, path):
    client = util.create_client(context)
    repo = client.defaultRepository
    obj = repo.getObjectByPath(util.sanitize_path(path))

    do_rm(context, obj)
