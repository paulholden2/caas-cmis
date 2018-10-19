##
# rm
#
# Remove files and folders
##

import util

rm_cmd = util.create_command()

rm_cmd.description = 'Delete a folder or document object from a repository.'

def do_rm(context, obj):
    client = util.create_client(context)
    repo = client.defaultRepository
    trash = repo.getObjectByPath('/StriaTrash')
    print(obj.id)

    props = obj.getProperties()

    if props['cmis:baseTypeId'] == 'cmis:folder':
        for c in obj.getChildren():
            do_rm(context, c)
        obj.delete()
    elif props['cmis:baseTypeId'] == 'cmis:document':
        #obj.delete()
        parents = obj.getObjectParents().getResults()
        #obj.move(parents[0], trash)
        doc = repo.getObject(obj.id)
        doc.move(repo.getObject(parents[0].id), trash)

@rm_cmd.main('path')
def rm(context, path):
    client = util.create_client(context)
    repo = client.defaultRepository
    obj = repo.getObjectByPath(util.sanitize_path(path))

    do_rm(context, obj)
