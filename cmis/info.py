##
# info
#
# Connect to a CMIS server and print some basic info about the repository
##

import util

info_cmd = util.create_command()

info_cmd.description = 'Get some basic information about the CMIS service or repositories.'

@info_cmd.main('[path]')
def info(context, path=None):
    client = util.create_client(context)
    repo = client.defaultRepository

    if path is None:
        for k, v in repo.info.items():
            print('%s = %s' % (k, v))

        for k, v in repo.getCapabilities().iteritems():
            print('%s = %s' % (k, v))

        print('propagation = %s' % repo.getPropagation())
    else:
        obj = repo.getObjectByPath(util.sanitize_path(path))

        for k, v in obj.getProperties().iteritems():
            print('%s = %s' % (k, v))
