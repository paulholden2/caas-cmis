##
# mkdir
#
# Connect to a CMIS server and create a folder or nested folders
##

import os
from cmislib.exceptions import ContentAlreadyExistsException, UpdateConflictException
import string
import util

mkdir = util.create_command()

def mkdir_p(context, name):
    client = util.create_client(context)
    repo = client.defaultRepository
    root = repo.getRootFolder()

    folders = string.split(name, '/')

    if len(folders) == 1:
        try:
            root.createFolder(name)
        except UpdateConflictException:
            pass
    else:
        parent = root
        path = ''

        for sub in folders:
            path = path + '/' + sub

            try:
                new_id = parent.createFolder(sub)
            except UpdateConflictException:
                new_id = repo.getObjectByPath(path)

            parent = repo.getFolder(new_id)

def mkdir_nop(context, name):
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

@mkdir.main('name')
def mkdir_main(context, name):
    if 'p' in context:
        return mkdir_p(context, name)
    else:
        return mkdir_nop(context, name)

@mkdir.option('-p')
def mkdir_p(context, p=True):
    context['p'] = p
