##
# rm
#
# Remove files and folders
##

import util

rm_cmd = util.create_command()

@rm_cmd.main('path')
def rm(context, path):
    client = util.create_client(context)
    repo = client.defaultRepository
    obj = repo.getObjectByPath('/' + path)

    obj.delete()
