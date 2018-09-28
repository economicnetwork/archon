from distutils.core import setup
import setuptools  # noqa


setup(
    name='archon1',
    version='0.0.1',
    author='Ben',
    author_email='ben@enet.io',
    packages=['archon'],
    #scripts=['bin/example.py'],
    url='http://pypi.python.org/pypi/archon1/',
    license='LICENSE',
    description='Trading agent framework',
    long_description=open('README.md').read(),
    install_requires=[
        #"Django >= 1.1.1",
        #"caldav == 0.1.4",
    ],
)