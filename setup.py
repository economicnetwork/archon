from distutils.core import setup
import setuptools  # noqa


setup(
    name='archon1',
    version='0.0.1',
    author='Ben',
    author_email='ben@enet.io',
    #packages=['archon'],
    #scripts=['bin/example.py'],
    url='http://pypi.python.org/pypi/archon1/',
    license='LICENSE',
    description='Trading agent framework',
    packages=setuptools.find_packages(exclude=('tests', 'docs'))
)
