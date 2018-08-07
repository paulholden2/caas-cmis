##
# chmod
#
# Apply ACLs to objects in a CMIS repository
##

import re
import util
import cmislib

chmod = util.create_command()

@chmod.main('access entity principal')
def chmod_main(context, access, entity, principal):
    res = re.match('\A([\-\+])(r|w|rw|wr|a)\Z', access)

    if not res:
        raise ValueError('Invalid access identifier: ' + access)

    if res.group(1) == '+':
        allow = 'true'
    else:
        allow = 'false'

    s = res.group(2)
    if 'a' in s:
        a = 'cmis:all'
    elif 'w' in s:
        a = 'cmis:write'
    elif 'r' in s:
        a = 'cmis:read'

    client = util.create_client(context)
    repo = client.defaultRepository
    ent = repo.getObjectByPath('/' + entity)

    acl = ent.getACL()
    acl.addEntry(principal, a, allow)
    ent.applyACL(acl)
