##
# acl
#
# Print ACL information about an object
##

import util

acl_cmd = util.create_command()

acl_cmd.description = 'List ACLs on a folder object by path'

@acl_cmd.main('path')
def acl(context, path):
    client = util.create_client(context)
    repo = client.defaultRepository
    obj = repo.getObjectByPath(util.sanitize_path(path))

    for principal, ace in obj.getACL().getEntries().iteritems():
        print('%s: %s (direct=%s)' % (principal, ace.permissions, ace.direct))
