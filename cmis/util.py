##
# Provides some helper functions for the rest of the application
##

import yaml
from argvard import Command
from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding

# Create a CMIS client
def create_client(context):
    # Default to looking at .caas.yml in working dir
    stream = file(context.get('config', '.caas.yml'), 'r')
    cfg = yaml.load(stream)

    # Pull service endpoint and credentials
    service_endpoint = context.get('service_endpoint', cfg['service_endpoint'])
    username = context.get('username', cfg['username'])
    password = context.get('password', cfg['password'])

    return CmisClient(service_endpoint, username, password, binding=AtomPubBinding())

# Create an Argvard command with standard options
def create_command():
    cmd = Command()

    # Allow user to specify which config file to load
    @cmd.option('--config config')
    def cmd_config(context, config):
        context['config'] = config

    return cmd
