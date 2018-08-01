import yaml
from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding

def create_client(context):
    stream = file(context.get('config', '.caas.yml'), 'r')
    cfg = yaml.load(stream)

    service_endpoint = context.get('service_endpoint', cfg['service_endpoint'])
    username = context.get('username', cfg['username'])
    password = context.get('password', cfg['password'])

    return CmisClient(service_endpoint, username, password, binding=AtomPubBinding())
