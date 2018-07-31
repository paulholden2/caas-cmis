import sys
import yaml
from cmislib import CmisClient
from cmislib.atompub.binding import AtomPubBinding

cfg = yaml.load(file(sys.argv[1], 'r'))

client = CmisClient(cfg['service_endpoint'], cfg['username'], cfg['password'], binding=AtomPubBinding())
repo = client.defaultRepository
info = repo.info

for k, v in info.items():
    print '%s:%s' % (k, v)
