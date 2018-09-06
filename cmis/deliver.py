##
# deliver
#
# Upload the contents of a folder into a CMIS repository. Requires:
#  - A load list CSV file named: load.csv
#  - 1 or more documents to deliver
#
# Load list
# ---------
# The load list is used to upload individual documents and apply mapped
# properties, e.g.
#
#  1  "caas:source","caas:destination","cmis:objectTypeId","Company Name"
#  2  "ACME Contract.pdf","/Contracts/ACME, Inc/Contracts","cmis:document","ACME, Inc"
#
# The caas:source, caas:destination, and cmis:objectTypeId columns are
# required. The first two indicate the source file path and destination
# folder path in the CMIS repository respectively. The last indiciates
# what type of object is being uploaded. See CMIS object types for more info.
#
# All other columns are treated as properties and are applied to the object
# upon upload.
#
# If the -m switch is provided, the delivery is done in module mode. In this
# mode, <directory> is treated as a collection of modules to deliver separately
# into the repository. The standard deliver command is executed for each
# module in an arbitrary order.
##

import os
import sys
import glob
import csv
import util
import cmis
from cmislib.exceptions import UpdateConflictException

deliver_cmd = util.create_command()

deliver_cmd.description = '''\
Upload a batch of files and properties to the repository. A delivery consists
of one or more files to upload and a load list in CSV format named
"load.csv".

An example of a CSV load list:

 1  "caas:source","caas:destination","cmis:objectTypeId","Company Name"
 2  "Contract.pdf","/Contracts/ACME, Inc","cmis:document","ACME, Inc"

The caas:source, caas:destination, and cmis:objectTypeId columns are
required. The first two indicate the source file path and destination folder
path in the CMIS repository respectively. The last indiciates what type of
object is being uploaded. See CMIS object types for more info.

The fourth and any additional columns describe properties for the object.
If the properties don't exist for the designated object type, the delivery
will fail. Empty property values are excluded from the uploaded document.
'''

def get_load(path):
    # List of required columns in their expected order
    required = [
        'caas:source',
        'caas:destination',
        'cmis:objectTypeId'
    ]

    # Data rows array
    data = []

    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        headers = reader.next()

        # Verify required columns are present in headers
        for key in required:
            if key not in headers:
                raise KeyError('Required column missing from load: %s' % key)

        # Row index, for reporting errors
        idx = 1

        for row in reader:
            # Assert the number of columns matches the number of values
            assert(len(row) == len(headers))

            data_row = {}

            # Build row dictionary
            for i in range(len(headers)):
                data_row[headers[i]] = row[i]

            # Append row to array
            data.append(data_row)

            # Verify we have data for required columns
            for key in required:
                if key not in data_row or data_row[key] == '':
                    raise ValueError('Required value missing from column %s at row %d' % (key, idx))

            idx += 1

    return data

def deliver_folder(context, folder):
    load_path = os.path.join(folder, 'load.csv')

    if not os.path.exists(load_path):
        print('Cannot upload %s: missing load.csv' % folder)

        return

    data = get_load(load_path)

    client = util.create_client(context)
    repo = client.defaultRepository

    # Dictionary cache of created/retrieved directories from the repository.
    #  - Key: folder path within repository
    #  - Value: CMIS folder object
    directories = {}

    # Dictionary cache of CMIS object types. Used to determine what type
    # to convert properties in the load list to (datetime, string, integer,
    # etc.)
    object_types = {}

    # For each entry in the load list
    for entry in data:
        source = entry.pop('caas:source')
        dest = entry.pop('caas:destination')
        type_id = entry['cmis:objectTypeId']

        if type_id not in object_types:
            object_types[type_id] = repo.getTypeDefinition(type_id)

        type_definition = object_types[type_id]

        pathlist = []
        dir = dest
        while dir != '/' and dir != '':
            pathlist.insert(0, dir)
            dir = os.path.dirname(dir)

        for path in pathlist:
            if path not in directories:
                parent_path = os.path.dirname(path)

                if parent_path in directories:
                    parent = directories[parent_path]
                else:
                    parent = repo.getRootFolder()

                try:
                    directories[path] = parent.createFolder(os.path.basename(path))
                except UpdateConflictException:
                    directories[path] = repo.getObjectByPath(util.sanitize_path(path))

        print('mkdir: %s' % dest)
        sys.stdout.flush()

        dest_dir = directories[dest]

        # Build properties dictionary
        props = {}
        for k, v in entry.iteritems():
            # Don't set empty properties (causes a CMIS error)
            if v == '':
                continue

            prop_type = type_definition.properties[k].propertyType

            if '|' in v:
                props[k] = []

                for i in v.split('|'):
                    if i is not None and i != '':
                        props[k].append(util.strtodata(i, prop_type))
            else:
                props[k] = util.strtodata(v, prop_type)

        # Upload the file
        with open(os.path.join(folder, source), 'rb') as source_file:
            dest_dir.createDocument(source, contentFile=source_file, properties=props)

        print('upload: %s => %s' % (source, dest))
        sys.stdout.flush()

@deliver_cmd.option('-m')
def deliver_opt_m(context, m=True):
    context['m'] = m

deliver_cmd.options['-m'].description = 'Deliver modules in <directory>'

@deliver_cmd.main('directory')
def deliver(context, directory):
    client = util.create_client(context)

    folders = []

    if 'm' in context:
        for path in glob.glob(os.path.join(os.getcwd(), directory, '*/')):
            folders.append(path)
    else:
        folders.append(directory)

    for fld in folders:
        deliver_folder(context, os.path.join(os.getcwd(), fld))
