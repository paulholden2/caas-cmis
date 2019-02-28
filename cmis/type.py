##
# type
#
# Connect to a CMIS server and list object types or definitions
##

import util

type_cmd = util.create_command()

type_cmd.description = 'List object types and definitions in a CMIS repository.'

@type_cmd.main('[type_id]')
def _type(context, type_id=None):
    client = util.create_client(context)
    repo = client.defaultRepository

    if type_id is None:
        for t in repo.getTypeDescendants():
            #print(t)
            pass
    else:
        definition = repo.getTypeDefinition(type_id)

        for prop in definition.properties:
            print('%s (%s %s)' % (prop, definition.properties[prop].cardinality, definition.properties[prop].getPropertyType()))
