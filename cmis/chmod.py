##
# chmod
#
# Apply ACLs to objects in a CMIS repository
##

import re
import util
import cmislib

chmod_cmd = util.create_command()

@chmod_cmd.main('access entity principal')
def chmod(context, access, entity, principal):
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

    client = util.create_client(context)
    repo = client.defaultRepository
    ent = repo.getObjectByPath('/' + entity)
    acl = ent.getACL()

    acl.removeEntry(principal)
    if acc is not None:
        acl.addEntry(principal, acc, 'true')

    ent.applyACL(acl)
