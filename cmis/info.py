import yaml
from argvard import Command
from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding

info = Command()

@info.option('--config config')
def info_config(context, config):
    context['config'] = config

@info.main()
def info_main(context):
    stream = file(context.get('config', '.caas.yml'), 'r')
    cfg = yaml.load(stream)

    service_endpoint = context.get('service_endpoint', cfg['service_endpoint'])
    username = context.get('username', cfg['username'])
    password = context.get('password', cfg['password'])

    client = CmisClient(service_endpoint, username, password, binding=AtomPubBinding())
    repo = client.defaultRepository

    for k, v in repo.info.items():
        print '%s:%s' % (k, v)
