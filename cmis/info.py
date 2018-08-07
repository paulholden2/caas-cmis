##
# info
#
# Connect to a CMIS server and print some basic info about the repository
##

import util

info = util.create_command()

@info.main('[entity]')
def info_main(context, entity=None):
    client = util.create_client(context)
    repo = client.defaultRepository

    if entity is None:
        for k, v in repo.info.items():
            print '%s:%s' % (k, v)
    else:
        obj = repo.getObjectByPath('/' + entity)

        for k, v in obj.getProperties().iteritems():
            print('%s = %s' % (k, v))
