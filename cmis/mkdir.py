##
# mkdir
#
# Connect to a CMIS server and create a folder or nested folders
##

import os
from cmislib.exceptions import ContentAlreadyExistsException, UpdateConflictException
import string
import util

mkdir_cmd = util.create_command()

def mkdir_noexcl(context, name):
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

def mkdir_excl(context, name):
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

@mkdir_cmd.main('name')
def mkdir(context, name):
    if 'p' in context:
        return mkdir_noexcl(context, name)
    else:
        return mkdir_excl(context, name)

@mkdir_cmd.option('-p')
def mkdir_opt_p(context, p=True):
    context['p'] = p
