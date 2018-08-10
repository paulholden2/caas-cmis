##
# mkdir
#
# Connect to a CMIS server and create a folder or nested folders
##

import os
from cmislib.exceptions import ContentAlreadyExistsException, UpdateConflictException
import string
import util
from chmod import chmod

mkdir_cmd = util.create_command()

@mkdir_cmd.option('-a access')
def mkdir_opt_a(context, access='r'):
    context['a'] = access

def mkdir_noexcl(context, name):
    client = util.create_client(context)
    repo = client.defaultRepository
    root = repo.getRootFolder()
    path = util.sanitize_path(name)
    folders = string.split(path, '/')[1:]

    if len(folders) == 1:
        try:
            new_id = root.createFolder(folders[0])

            if 'a' in context:
                # Pop access option from context for the chmod call
                access = context.pop('a')
                chmod(context, access, path, context['username'])
                context['a'] = access

            return repo.getFolder(new_id)
        except UpdateConflictException:
            return repo.getObjectByPath(path)
    else:
        parent = root
        sub_path = ''

        for sub in folders:
            sub_path = sub_path + '/' + sub

            try:
                new_id = parent.createFolder(sub)
            except UpdateConflictException:
                new_id = repo.getObjectByPath(sub_path)

            if 'a' in context:
                # Pop access option from context for the chmod call
                access = context.pop('a')
                chmod(context, access, sub_path, context['username'])
                context['a'] = access

            parent = repo.getFolder(new_id)

        return parent

def mkdir_excl(context, name):
    client = util.create_client(context)
    repo = client.defaultRepository
    root = repo.getRootFolder()
    path = util.sanitize_path(name)
    folders = string.split(path, '/')[1:]

    if len(folders) == 1:
        new_id = root.createFolder(folders[0])

        if 'a' in context:
            # Pop access option from context for the chmod call
            access = context.pop('a')
            chmod(context, access, path, context['username'])
            context['a'] = access

        return repo.getFolder(new_id)
    else:
        parent = root
        sub_path = ''

        for sub in folders:
            sub_path = sub_path + '/' + sub

            new_id = parent.createFolder(sub)

            if 'a' in context:
                # Pop access option from context for the chmod call
                access = context.pop('a')
                chmod(context, access, sub_path, context['username'])
                context['a'] = access

            parent = repo.getFolder(new_id)

        return parent

@mkdir_cmd.main('name')
def mkdir(context, name):
    if 'p' in context:
        return mkdir_noexcl(context, name)
    else:
        return mkdir_excl(context, name)

@mkdir_cmd.option('-p')
def mkdir_opt_p(context, p=True):
    context['p'] = p
