##
# put
#
# Upload a file to a CMIS repository
##

import os
import util

put_cmd = util.create_command()

@put_cmd.main('local [path] [type_id]')
def put(context, local, path='', type_id='cmis:document'):
    client = util.create_client(context)
    repo = client.defaultRepository

    folder = repo.getObjectByPath(util.sanitize_path(path))

    doc = open(local, 'rb')
    props = {
        'cmis:objectTypeId': type_id
    }

    folder.createDocument(os.path.basename(local), contentFile=doc, properties=props)

    doc.close()

    print(local + ' ==> ' + path)
