##
# Provides some helper functions for the rest of the application
##

import yaml
from argvard import Command
from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding
from cmislib.browser.binding import BrowserBinding

# Create a CMIS client
def create_client(context):
    if 'client' in context:
        return context['client']

    # Default to looking at .caas.yml in working dir
    stream = file(context.get('config', '.caas.yml'), 'r')
    cfg = yaml.load(stream)

    # Pull service endpoint and credentials
    hostname = context.get('hostname', cfg['hostname'])
    username = context.get('username', cfg['username'])
    password = context.get('password', cfg['password'])
    binding = context.get('binding', cfg.get('binding', 'atompub'))

    if binding == 'atompub':
        adapter = AtomPubBinding
    elif binding == 'browser':
        adapter = BrowserBinding
    else:
        raise Exception('Unknown binding type: ' + binding)

    client = CmisClient(hostname, username, password, binding=adapter)

    if hostname.startswith('https:'):
        adapter.ssl = True
    else:
        adapter.ssl = False

    return client

# Create an Argvard command with standard options
def create_command():
    cmd = Command()

    # Allow user to specify which config file to load
    @cmd.option('--config config')
    def cmd_config(context, config):
        context['config'] = config

    # Allow user to specify a hostname
    @cmd.option('--hostname hostname')
    def cmd_hostname(context, hostname):
        context['hostname'] = hostname

    # Allow user to specify a username
    @cmd.option('--username username')
    def cmd_username(context, username):
        context['username'] = username

    # Allow user to specify a password
    @cmd.option('--password password')
    def cmd_password(context, password):
        context['password'] = password

    # Allow user to specify a binding
    @cmd.option('--binding binding')
    def cmd_binding(context, binding):
        context['binding'] = binding

    # Add descriptions for standard options
    cmd.options['--hostname'].description = 'Hostname of the CMIS service endpoint'
    cmd.options['--username'].description = 'Username to connect to the CMIS server as'
    cmd.options['--password'].description = 'Password to authenticate with'
    cmd.options['--binding'].description = 'The API binding to use. Supported values: atompub, browser'

    return cmd

def sanitize_path(path):
    if not path.startswith('/'):
        path = '/' + path

    return path
