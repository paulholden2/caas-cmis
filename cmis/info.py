import util
from argvard import Command

info = Command()

@info.option('--config config')
def info_config(context, config):
    context['config'] = config

@info.main()
def info_main(context):
    client = util.create_client(context)
    repo = client.defaultRepository

    for k, v in repo.info.items():
        print '%s:%s' % (k, v)
