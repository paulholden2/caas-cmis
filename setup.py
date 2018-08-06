from setuptools import setup

setup(name='caas-cmis',
      version='0.1',
      description='CaaS CMIS tools',
      url='https://github.com/paulholden2/caas-cmis',
      author='Paul Holden',
      author_email='pholden@stria.com',
      license='MIT',
      install_requires=['PyYAML','watchtower','Argvard'],
      packages=['cmis'],
      scripts=['bin/cmis'],
      zip_safe=False)
