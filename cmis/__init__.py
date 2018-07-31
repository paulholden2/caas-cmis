from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding

def info(cfg):
    client = CmisClient(cfg['service_endpoint'], cfg['username'], cfg['password'], binding=AtomPubBinding())
    repo = client.defaultRepository
    info = repo.info

    for k, v in info.items():
        print '%s:%s' % (k, v)
