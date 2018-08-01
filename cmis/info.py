##
# info
#
# Connect to a CMIS server and print some basic info about the repository
##

import util

info = util.create_command()

@info.main()
def info_main(context):
    client = util.create_client(context)
    repo = client.defaultRepository

    for k, v in repo.info.items():
        print '%s:%s' % (k, v)
