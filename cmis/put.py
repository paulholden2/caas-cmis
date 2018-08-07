##
# put
#
# Upload a file to a CMIS repository
##

import os
import util

put = util.create_command()

@put.main('local [remote] [type_id]')
def put_main(context, local, remote='', type_id='cmis:document'):
    client = util.create_client(context)
    repo = client.defaultRepository

    remote = '/' + remote
    folder = repo.getObjectByPath(remote)

    doc = open(local, 'rb')
    props = {
        'cmis:objectTypeId': type_id
    }

    folder.createDocument(os.path.basename(local), contentFile=doc, properties=props)

    doc.close()

    print(local + ' ==> ' + remote)
