##
# chmod
#
# Apply ACLs to objects in a CMIS repository
##

import re
import util
import cmislib

chmod_cmd = util.create_command()

@chmod_cmd.option('-d')
def chmod_opt_d(context, d=True):
    context['d'] = d

@chmod_cmd.main('access path principal')
def chmod(context, access, path, principal):
    res = re.match('\A(-|r|w|rw|wr|a)\Z', access)

    if not res:
        raise ValueError('Invalid access identifier: ' + access)

    s = res.group(1)
    if 'a' in s:
        acc = 'cmis:all'
    elif 'w' in s:
        acc = 'cmis:write'
    elif 'r' in s:
        acc = 'cmis:read'
    else:
        acc = None

    if 'd' in context:
        direct = 'true'
    else:
        direct = 'false'

    client = util.create_client(context)
    repo = client.defaultRepository
    obj = repo.getObjectByPath(util.sanitize_path(path))
    acl = obj.getACL()

    acl.removeEntry(principal)
    if acc is not None:
        acl.addEntry(principal, acc, direct)

    obj.applyACL(acl)
