from setuptools import setup

setup(name='caas-filenet',
      version='0.1',
      description='CaaS FileNet services',
      url='https://github.com/paulholden2/caas-filenet',
      author='Paul Holden',
      author_email='pholden@stria.com',
      license='MIT',
      install_requires=['PyYAML','watchtower','cmislib'],
      packages=['filenet'],
      scripts=['bin/filenet'],
      zip_safe=False)
