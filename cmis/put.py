##
# put
#
# Upload a file to a CMIS repository
##

import os
import util

put = util.create_command()

@put.main('local [remote]')
def put_main(context, local, remote=''):
    client = util.create_client(context)
    repo = client.defaultRepository

    remote = '/' + remote
    folder = repo.getObjectByPath(remote)

    doc = open(local, 'rb')
    folder.createDocument(os.path.basename(local), contentFile=doc)
    doc.close()

    print(local + ' ==> ' + remote)
