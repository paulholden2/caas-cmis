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
# The caas:source, caas:destination, and cmis:objectTypeId columsn are
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
import glob
import csv
import util
import cmis

deliver_cmd = util.create_command()

def get_load(path):
    required = [
        'caas:source',
        'caas:destination',
        'cmis:objectTypeId'
    ]

    data = []

    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        headers = reader.next()

        # Verify required columns are present in headers
        for key in required:
            if key not in headers:
                raise KeyError('Required column missing from load: %s' % key)

        idx = 1

        for row in reader:
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
    # So we don't create new clients when running commands
    context['client'] = client

    repo = client.defaultRepository

    directories = {}

    for entry in data:
        source = entry.pop('caas:source')
        dest = entry.pop('caas:destination')
        type_id = entry.pop('cmis:objectTypeId')

        if dest not in directories:
            dest_dir = cmis.mkdir.mkdir_noexcl(context, dest)
            directories[dest] = dest_dir

            print('mkdir: %s' % dest)
        else:
            dest_dir = directories[dest]

        source_file = open(os.path.join(folder, source), 'rb')
        dest_dir.createDocument(source, contentFile=source_file, properties={'cmis:objectTypeId':'cmis:document'})
        source_file.close()

        print('upload: %s => %s' % (source, dest))

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
